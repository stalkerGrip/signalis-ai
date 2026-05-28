#!/usr/bin/env python3
"""
Normalize Signalis/NutScript networking operations.

Purpose:
  - Correct netstream.Start argument semantics by realm:
      SERVER: netstream.Start(recipient, message, payload...)
      CLIENT: netstream.Start(message, payload...)
      SHARED/UNKNOWN: infer from args when possible
  - Keep raw GMod net semantics:
      net.Start(message, unreliable?)
      net.Receive(message, fn)
      util.AddNetworkString(message)
  - Resolve simple symbolic message constants, especially nut.* string constant tables.
  - Emit QA that separates likely real protocol issues from extractor/normalizer uncertainty.

Outputs:
  manifests/normalized/normalized_network_operations.json
  manifests/normalized/network_symbol_issues.json
  manifests/normalized/network_protocol_qa.md
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

MANIFEST_NETWORK_DIR = Path("manifests/networking")
NORMALIZED_DIR = Path("manifests/normalized")

RECIPIENT_LIKE = {
    "client", "ply", "player", "recipient", "receiver", "receivers", "targets",
    "target", "activator", "caller", "admin", "admins", "v", "k", "self", "item.player",
    "self.player", "self.user", "ent", "entity", "owner", "user", "char", "character",
    "nil", "NULL",
}
BAD_MESSAGE_LIKE = RECIPIENT_LIKE | {"unknown", "ents.GetByIndex", "LocalPlayer()"}
QUERY_OR_FUNC_PREFIXES = ("ents.", "player.", "Entity(", "LocalPlayer(", "table.")
STRING_RE = re.compile(r"^(['\"])(.*)\1$")
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_\.\:\[\]\(\)]*$")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def norm_path(s: str | None) -> str:
    return (s or "").replace("/", "\\")


def infer_realm(file: str, existing: str | None = None) -> str:
    if existing and existing not in ("", "unknown"):
        return existing
    p = norm_path(file).lower()
    name = Path(p.replace("\\", "/")).name
    if name.startswith("sv_") or "\\sv_" in p or "\\server\\" in p:
        return "server"
    if name.startswith("cl_") or "\\cl_" in p or "\\client\\" in p or "\\derma\\" in p:
        return "client"
    if name.startswith("sh_") or "\\sh_" in p or "\\shared\\" in p:
        return "shared"
    return existing or "shared"


def candidate_source_roots(workspace: Path, source_root: Optional[Path], nutscript_root: Optional[Path]) -> List[Path]:
    roots: List[Path] = []
    for r in [source_root, nutscript_root, workspace]:
        if r and r.exists():
            roots.append(r)
    # common workspace-local locations
    for rel in ["source", "src", "gamemode", "signalis", "nutscript"]:
        p = workspace / rel
        if p.exists():
            roots.append(p)
    # de-dupe
    out: List[Path] = []
    seen = set()
    for r in roots:
        rp = str(r.resolve()).lower()
        if rp not in seen:
            seen.add(rp)
            out.append(r)
    return out


def find_source_file(rel_file: str, roots: List[Path]) -> Optional[Path]:
    rel = Path(rel_file.replace("\\", "/"))
    for root in roots:
        p = root / rel
        if p.exists():
            return p
        # if manifest file includes gamemode-relative prefix, try suffix search cheaply
        parts = rel.parts
        for i in range(1, min(len(parts), 5)):
            q = root / Path(*parts[i:])
            if q.exists():
                return q
    return None


def strip_lua_comments(s: str) -> str:
    # Conservative single-line comment stripping, enough for call extraction.
    out = []
    in_s = in_d = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        if not in_s and not in_d and s[i:i+2] == "--":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def extract_call_at_line(path: Path, line_no: int, call_name: str) -> Optional[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return None
    start = max(0, line_no - 1)
    # Search a small window around the manifest line.
    blob = "\n".join(lines[start:min(len(lines), start + 12)])
    idx = blob.find(call_name)
    if idx < 0 and start > 0:
        blob = "\n".join(lines[max(0, start - 3):min(len(lines), start + 12)])
        idx = blob.find(call_name)
    if idx < 0:
        return None
    open_idx = blob.find("(", idx + len(call_name))
    if open_idx < 0:
        return None
    depth = 0
    in_s = in_d = False
    esc = False
    for j in range(open_idx, len(blob)):
        ch = blob[j]
        if esc:
            esc = False
            continue
        if ch == "\\" and (in_s or in_d):
            esc = True
            continue
        if ch == "'" and not in_d:
            in_s = not in_s
        elif ch == '"' and not in_s:
            in_d = not in_d
        elif not in_s and not in_d:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return blob[idx:j+1]
    return None


def split_args(arg_text: str) -> List[str]:
    args: List[str] = []
    cur: List[str] = []
    depth = 0
    in_s = in_d = False
    esc = False
    i = 0
    while i < len(arg_text):
        ch = arg_text[i]
        if esc:
            cur.append(ch)
            esc = False
            i += 1
            continue
        if ch == "\\" and (in_s or in_d):
            cur.append(ch)
            esc = True
            i += 1
            continue
        if ch == "'" and not in_d:
            in_s = not in_s
            cur.append(ch)
        elif ch == '"' and not in_s:
            in_d = not in_d
            cur.append(ch)
        elif not in_s and not in_d:
            if ch in "({[":
                depth += 1
                cur.append(ch)
            elif ch in ")}]":
                depth -= 1
                cur.append(ch)
            elif ch == "," and depth == 0:
                args.append("".join(cur).strip())
                cur = []
            else:
                cur.append(ch)
        else:
            cur.append(ch)
        i += 1
    if cur or arg_text.strip():
        args.append("".join(cur).strip())
    return [a for a in args if a != ""]


def parse_call_args(call: Optional[str], call_name: str) -> List[str]:
    if not call:
        return []
    idx = call.find(call_name)
    open_idx = call.find("(", idx + len(call_name))
    close_idx = call.rfind(")")
    if open_idx < 0 or close_idx <= open_idx:
        return []
    return split_args(call[open_idx + 1:close_idx])


def unquote(expr: str | None) -> Tuple[str | None, bool]:
    if expr is None:
        return None, False
    e = expr.strip()
    m = STRING_RE.match(e)
    if m:
        return m.group(2), True
    return e, False


def is_symbolic(expr: str | None) -> bool:
    if not expr:
        return False
    _, quoted = unquote(expr)
    return not quoted


def looks_recipient(expr: str | None) -> bool:
    if not expr:
        return False
    e = expr.strip()
    low = e.lower()
    if low in {x.lower() for x in RECIPIENT_LIKE}:
        return True
    if any(low.startswith(p.lower()) for p in QUERY_OR_FUNC_PREFIXES):
        return True
    if ":getplayer" in low or ":getowner" in low or ":getcreator" in low:
        return True
    if "player" in low or "client" in low or "receiver" in low or "target" in low:
        return True
    return False


def message_quality(message: str | None, symbolic: bool) -> Tuple[str, List[str]]:
    reasons = []
    if not message:
        return "invalid", ["missing_message"]
    low = message.strip().lower()
    if low in {x.lower() for x in BAD_MESSAGE_LIKE}:
        reasons.append("message_looks_like_recipient_or_placeholder")
    if message in {"nil", "NULL"}:
        reasons.append("nil_message")
    if symbolic:
        reasons.append("dynamic_or_symbolic_message")
    if message.startswith("nut."):
        reasons.append("nut_symbol_path")
    if any(ch in message for ch in " (){}[]") and not message.startswith("nut."):
        reasons.append("expression_like_message")
    if reasons and ("message_looks_like_recipient_or_placeholder" in reasons or "nil_message" in reasons):
        return "suspicious", reasons
    if symbolic:
        return "dynamic", reasons
    return "literal", reasons


def scan_lua_files(roots: List[Path]) -> Iterable[Path]:
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.lua"):
            sp = str(p.resolve()).lower()
            if sp not in seen:
                seen.add(sp)
                yield p


def build_string_constant_map(roots: List[Path]) -> Dict[str, str]:
    """Best-effort symbol map for nut.* string constant tables.

    Handles patterns like:
      nut.diseases.stringConsts = nut.diseases.stringConsts || {
        hudAddStatusIcon = "hudAddStatusIcon",
      }
      nut.foo.bar = "MessageName"
    """
    mapping: Dict[str, str] = {}
    direct = re.compile(r"\b(nut(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\s*=\s*(['\"])(.*?)\2")
    table_start = re.compile(r"\b(nut(?:\.[A-Za-z_][A-Za-z0-9_]*)+)\s*=\s*[^\n{]*\{")
    entry = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['\"])(.*?)\2")
    for p in scan_lua_files(roots):
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in direct.finditer(text):
            mapping[m.group(1)] = m.group(3)
        for m in table_start.finditer(text):
            prefix = m.group(1)
            # Find a conservative block after the opening brace.
            start = m.end()
            depth = 1
            i = start
            in_s = in_d = False
            while i < len(text) and depth > 0 and i - start < 20000:
                ch = text[i]
                if ch == "'" and not in_d:
                    in_s = not in_s
                elif ch == '"' and not in_s:
                    in_d = not in_d
                elif not in_s and not in_d:
                    if ch == "{": depth += 1
                    elif ch == "}": depth -= 1
                i += 1
            block = text[start:i]
            for em in entry.finditer(block):
                mapping[f"{prefix}.{em.group(1)}"] = em.group(3)
    return mapping


def resolve_message(expr: str | None, const_map: Dict[str, str]) -> Tuple[str | None, str, List[str]]:
    if expr is None:
        return None, "missing", ["missing_expr"]
    raw, quoted = unquote(expr)
    if raw is None:
        return None, "missing", ["missing_expr"]
    if quoted:
        return raw, "literal", []
    if raw in const_map:
        return const_map[raw], "symbol_constant", [f"resolved_symbol:{raw}"]
    # common table leaf fallback: nut.foo.bar.MessageName -> MessageName-ish only if leaf looks message-like
    if raw.startswith("nut.") and "." in raw:
        leaf = raw.split(".")[-1]
        if leaf:
            return leaf, "symbol_leaf_fallback", [f"unresolved_nut_symbol_leaf:{raw}"]
    return raw, "dynamic", ["unresolved_dynamic_expr"]


def protocol_guess(message: str | None) -> str:
    if not message:
        return "unknown"
    m = message.lower()
    if m.startswith("inv") or "inventory" in m or "item" in m or "storage" in m or "loot" in m:
        return "inventory_item_storage"
    if m.startswith("char") or "character" in m:
        return "character"
    if "hud" in m or "panel" in m or "menu" in m or "ui" in m or "interface" in m:
        return "ui_hud"
    if "disease" in m or "status" in m or "pain" in m or "blood" in m or "o2" in m:
        return "health_status"
    if "vendor" in m or "shop" in m:
        return "vendor"
    if "plugin" in m or "cfg" in m or "config" in m:
        return "admin_config"
    if "craft" in m or "workbench" in m:
        return "crafting"
    return "misc"


def make_op_id(kind: str, item: Dict[str, Any], idx: int) -> str:
    f = norm_path(item.get("file", "unknown"))
    line = item.get("line", "?")
    return f"network_op:{kind}:{f}:{line}:{idx}"


def normalize_netstream_start(item: Dict[str, Any], idx: int, roots: List[Path], const_map: Dict[str, str]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    issues: List[Dict[str, Any]] = []
    file = norm_path(item.get("file"))
    realm = infer_realm(file, item.get("realm"))
    src = find_source_file(file, roots)
    call = extract_call_at_line(src, int(item.get("line", 0) or 0), "netstream.Start") if src else None
    args = parse_call_args(call, "netstream.Start")
    layout = "manifest_fallback"
    recipient_expr = None
    message_expr = item.get("message_expr") or item.get("message_name")
    payload_exprs: List[str] = []

    if args:
        if realm == "server":
            layout = "server_netstream_start"
            recipient_expr = args[0] if len(args) > 0 else None
            message_expr = args[1] if len(args) > 1 else message_expr
            payload_exprs = args[2:]
        elif realm == "client":
            layout = "client_netstream_start"
            message_expr = args[0] if len(args) > 0 else message_expr
            payload_exprs = args[1:]
        else:
            # shared/unknown: infer by first arg. If it looks recipient-ish, use server layout.
            if len(args) >= 2 and looks_recipient(args[0]):
                layout = "inferred_server_netstream_start"
                recipient_expr = args[0]
                message_expr = args[1]
                payload_exprs = args[2:]
            else:
                layout = "inferred_client_netstream_start"
                message_expr = args[0] if args else message_expr
                payload_exprs = args[1:]
    else:
        issues.append({"kind": "source_call_not_found", "file": file, "line": item.get("line"), "original": item})

    # Detect older extractor issue: manifest message looked recipient-like, but source arg2 is useful.
    manifest_msg, _ = unquote(item.get("message_expr") or item.get("message_name") or "")
    if args and manifest_msg and looks_recipient(manifest_msg) and message_expr != manifest_msg:
        issues.append({
            "kind": "corrected_recipient_misread_as_message",
            "file": file,
            "line": item.get("line"),
            "manifest_message": manifest_msg,
            "corrected_message_expr": message_expr,
            "layout": layout,
        })

    message, resolution, reasons = resolve_message(message_expr, const_map)
    symbolic = resolution not in ("literal", "symbol_constant")
    quality, quality_reasons = message_quality(message, symbolic)
    if quality in ("suspicious", "invalid") or symbolic:
        issues.append({
            "kind": "netstream_message_issue",
            "file": file,
            "line": item.get("line"),
            "message": message,
            "message_expr": message_expr,
            "quality": quality,
            "reasons": reasons + quality_reasons,
            "layout": layout,
        })

    op = {
        "id": make_op_id("netstream_start", item, idx),
        "type": "network_operation",
        "operation": "send",
        "protocol": "netstream",
        "api": "netstream.Start",
        "message": message,
        "message_expr": message_expr,
        "message_resolution": resolution,
        "message_quality": quality,
        "recipient_expr": recipient_expr,
        "payload_exprs": payload_exprs,
        "payload_arg_count": len(payload_exprs),
        "layout": layout,
        "realm": realm,
        "file": file,
        "line": item.get("line"),
        "framework_layer": item.get("framework_layer"),
        "source_call": call,
        "source": "netstream_starts",
        "original": item,
    }
    return op, issues


def normalize_simple_message_op(kind: str, api: str, op_kind: str, item: Dict[str, Any], idx: int, const_map: Dict[str, str]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    file = norm_path(item.get("file"))
    realm = infer_realm(file, item.get("realm"))
    expr = item.get("message_name") or item.get("message_expr")
    message, resolution, reasons = resolve_message(expr, const_map)
    symbolic = resolution not in ("literal", "symbol_constant")
    quality, qreasons = message_quality(message, symbolic)
    issues: List[Dict[str, Any]] = []
    if quality in ("suspicious", "invalid") or symbolic:
        issues.append({
            "kind": f"{kind}_message_issue",
            "file": file,
            "line": item.get("line"),
            "message": message,
            "message_expr": expr,
            "quality": quality,
            "reasons": reasons + qreasons,
        })
    return {
        "id": make_op_id(kind, item, idx),
        "type": "network_operation",
        "operation": op_kind,
        "protocol": "gmod_net" if kind.startswith("net_") or kind.startswith("util_") else "netstream",
        "api": api,
        "message": message,
        "message_expr": expr,
        "message_resolution": resolution,
        "message_quality": quality,
        "realm": realm,
        "file": file,
        "line": item.get("line"),
        "framework_layer": item.get("framework_layer"),
        "source": kind + "s" if not kind.endswith("s") else kind,
        "original": item,
    }, issues


def load_inputs(workspace: Path) -> Dict[str, List[Dict[str, Any]]]:
    nd = workspace / MANIFEST_NETWORK_DIR
    return {
        "netstream_starts": load_json(nd / "netstream_starts.json", []),
        "netstream_hooks": load_json(nd / "netstream_hooks.json", []),
        "net_starts": load_json(nd / "net_starts.json", []),
        "net_receives": load_json(nd / "net_receives.json", []),
        "util_add_network_strings": load_json(nd / "util_add_network_strings.json", []),
        "net_reads": load_json(nd / "net_reads.json", []),
        "net_writes": load_json(nd / "net_writes.json", []),
        "net_messages_deep": load_json(nd / "net_messages_deep.json", []),
    }


def build_qa(ops: List[Dict[str, Any]], issues: List[Dict[str, Any]], inputs: Dict[str, List[Dict[str, Any]]]) -> str:
    sends = [o for o in ops if o["operation"] == "send"]
    receives = [o for o in ops if o["operation"] == "receive"]
    registers = [o for o in ops if o["operation"] == "register"]
    net_sends = [o for o in sends if o["protocol"] == "gmod_net"]
    net_receives = [o for o in receives if o["protocol"] == "gmod_net"]
    net_registers = [o for o in registers if o["protocol"] == "gmod_net"]

    sent_msgs = Counter(o.get("message") for o in sends if o.get("message"))
    recv_msgs = Counter(o.get("message") for o in receives if o.get("message"))
    reg_msgs = Counter(o.get("message") for o in registers if o.get("message"))
    net_sent = {o.get("message") for o in net_sends if o.get("message") and o.get("message_quality") != "suspicious"}
    net_recv = {o.get("message") for o in net_receives if o.get("message") and o.get("message_quality") != "suspicious"}
    net_reg = {o.get("message") for o in net_registers if o.get("message") and o.get("message_quality") != "suspicious"}

    protocols = Counter(o.get("protocol") for o in ops)
    operations = Counter(o.get("operation") for o in ops)
    realms = Counter(o.get("realm") for o in ops)
    qualities = Counter(o.get("message_quality") for o in ops if o.get("message_quality"))
    resolutions = Counter(o.get("message_resolution") for o in ops if o.get("message_resolution"))
    layouts = Counter(o.get("layout") for o in ops if o.get("layout"))
    issue_kinds = Counter(i.get("kind") for i in issues)
    protocol_groups = Counter(protocol_guess(o.get("message")) for o in ops if o.get("message"))

    raw_missing_register = sorted((net_sent | net_recv) - net_reg)
    raw_registered_unused = sorted(net_reg - (net_sent | net_recv))
    sends_no_receivers = sorted(set(sent_msgs) - set(recv_msgs))
    receivers_no_senders = sorted(set(recv_msgs) - set(sent_msgs))

    def lines_top(counter: Counter, n=30):
        return [f"- `{k}`: {v}" for k, v in counter.most_common(n)] or ["- none"]
    def lines_list(values: List[str], n=50):
        shown = values[:n]
        lines = [f"- `{v}`" for v in shown]
        if len(values) > n:
            lines.append(f"- ... {len(values)-n} more")
        return lines or ["- none"]

    corrected = [i for i in issues if i.get("kind") == "corrected_recipient_misread_as_message"]
    dynamic = [o for o in ops if o.get("message_quality") == "dynamic"]
    suspicious = [o for o in ops if o.get("message_quality") == "suspicious"]

    out: List[str] = []
    out += ["# Network operation normalization QA", "", "Schema: `normalized_network_operations.v1`", ""]
    out += ["## Inputs"]
    for k, v in inputs.items():
        out.append(f"- `{k}`: **{len(v)}**")
    out += ["", "## Totals"]
    out += [
        f"- Normalized operations: **{len(ops)}**",
        f"- Sends: **{len(sends)}**",
        f"- Receives: **{len(receives)}**",
        f"- Registrations: **{len(registers)}**",
        f"- Symbol/QA issues: **{len(issues)}**",
        f"- Corrected recipient-as-message captures: **{len(corrected)}**",
        f"- Dynamic/symbolic messages kept: **{len(dynamic)}**",
        f"- Suspicious message IDs remaining: **{len(suspicious)}**",
    ]
    out += ["", "## Protocols", *lines_top(protocols, 10)]
    out += ["", "## Operations", *lines_top(operations, 10)]
    out += ["", "## Realms", *lines_top(realms, 10)]
    out += ["", "## Message quality", *lines_top(qualities, 10)]
    out += ["", "## Message resolution", *lines_top(resolutions, 10)]
    out += ["", "## Netstream argument layouts", *lines_top(layouts, 10)]
    out += ["", "## Protocol/subsystem guesses", *lines_top(protocol_groups, 20)]
    out += ["", "## Issue kinds", *lines_top(issue_kinds, 20)]
    out += ["", "## Top sent messages", *lines_top(sent_msgs, 40)]
    out += ["", "## Top received messages", *lines_top(recv_msgs, 40)]
    out += ["", "## Raw GMod net messages missing util.AddNetworkString in manifests"]
    out += lines_list(raw_missing_register, 80)
    out += ["", "## Raw GMod net messages registered but not observed as sent/received"]
    out += lines_list(raw_registered_unused, 80)
    out += ["", "## Messages with senders but no receivers"]
    out += lines_list(sends_no_receivers, 80)
    out += ["", "## Messages with receivers but no senders"]
    out += lines_list(receivers_no_senders, 80)
    out += ["", "## Remaining suspicious message IDs"]
    for o in suspicious[:80]:
        out.append(f"- `{o.get('message')}` at `{o.get('file')}:{o.get('line')}` via `{o.get('api')}` layout=`{o.get('layout','')}` expr=`{o.get('message_expr')}`")
    if len(suspicious) > 80:
        out.append(f"- ... {len(suspicious)-80} more")
    if not suspicious:
        out.append("- none")
    out += ["", "## Dynamic/symbolic messages"]
    for o in dynamic[:80]:
        out.append(f"- `{o.get('message')}` at `{o.get('file')}:{o.get('line')}` via `{o.get('api')}` resolution=`{o.get('message_resolution')}`")
    if len(dynamic) > 80:
        out.append(f"- ... {len(dynamic)-80} more")
    if not dynamic:
        out.append("- none")
    out += ["", "## External doctrine checks"]
    out += [
        "- `net.Start(messageName, unreliable?)`: message name is arg0.",
        "- Raw GMod net messages should be pooled server-side with `util.AddNetworkString(messageName)` before use.",
        "- Raw net messages have an approximate 64 KiB/message limit; high payload arg count is only a weak static risk signal, not proof of oversize payload.",
        "- `netstream.Start` is project/library-level: server layout is recipient first, client layout is message first.",
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default=".", help="Project workspace, e.g. E:/signalis_ai")
    ap.add_argument("--source-root", default=None, help="Signalis gamemode source root for source-call recovery")
    ap.add_argument("--nutscript-root", default=None, help="NutScript gamemode source root for source-call recovery")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    workspace = Path(args.workspace)
    roots = candidate_source_roots(
        workspace,
        Path(args.source_root) if args.source_root else None,
        Path(args.nutscript_root) if args.nutscript_root else None,
    )
    inputs = load_inputs(workspace)
    const_map = build_string_constant_map(roots)

    ops: List[Dict[str, Any]] = []
    issues: List[Dict[str, Any]] = []

    for i, item in enumerate(inputs["netstream_starts"]):
        op, iss = normalize_netstream_start(item, i, roots, const_map)
        ops.append(op); issues.extend(iss)

    for source_key, kind, api, op_kind in [
        ("netstream_hooks", "netstream_hook", "netstream.Hook", "receive"),
        ("net_starts", "net_start", "net.Start", "send"),
        ("net_receives", "net_receive", "net.Receive", "receive"),
        ("util_add_network_strings", "util_add_network_string", "util.AddNetworkString", "register"),
    ]:
        for i, item in enumerate(inputs[source_key]):
            op, iss = normalize_simple_message_op(kind, api, op_kind, item, i, const_map)
            ops.append(op); issues.extend(iss)

    # payload operations are kept separate but included for downstream graph builders.
    payload_ops: List[Dict[str, Any]] = []
    for source_key, api, op_kind in [("net_reads", "net.Read*", "read_payload"), ("net_writes", "net.Write*", "write_payload")]:
        for i, item in enumerate(inputs[source_key]):
            file = norm_path(item.get("file"))
            payload_ops.append({
                "id": make_op_id(source_key[:-1], item, i),
                "type": "network_payload_operation",
                "operation": op_kind,
                "api": item.get("function") or item.get("api") or api,
                "realm": infer_realm(file, item.get("realm")),
                "file": file,
                "line": item.get("line"),
                "framework_layer": item.get("framework_layer"),
                "source": source_key,
                "original": item,
            })

    normalized = {
        "schema": "normalized_network_operations.v1",
        "inputs": {k: len(v) for k, v in inputs.items()},
        "source_roots_scanned": [str(r) for r in roots],
        "string_constants_resolved": len(const_map),
        "operations": ops,
        "payload_operations": payload_ops,
    }
    qa = build_qa(ops, issues, inputs)

    if args.write:
        out_dir = workspace / NORMALIZED_DIR
        write_json(out_dir / "normalized_network_operations.json", normalized)
        write_json(out_dir / "network_symbol_issues.json", issues)
        (out_dir / "network_protocol_qa.md").write_text(qa, encoding="utf-8")
        print(f"Wrote {out_dir / 'normalized_network_operations.json'}")
        print(f"Wrote {out_dir / 'network_symbol_issues.json'}")
        print(f"Wrote {out_dir / 'network_protocol_qa.md'}")
    else:
        print(qa)


if __name__ == "__main__":
    main()
