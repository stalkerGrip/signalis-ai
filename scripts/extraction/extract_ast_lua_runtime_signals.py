from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

PIPELINE_CONTRACT = {
    "script_id": "scripts.extraction.extract_ast_lua_runtime_signals",
    "purpose": "Prototype Tree-sitter Lua syntax extraction using lua_ast_syntax_alphabet declarations.",
    "pipeline_stage": "extraction",
    "input_families": ["source_file_manifest", "lua_ast_syntax_alphabet"],
    "required_input_capabilities": ["source_roots", "source_files", "file_realm_hints", "file_digests", "ast_syntax_extraction_rules"],
    "output_families": ["ast_lua_extraction"],
    "required_output_capabilities": ["source_manifest_reference", "lua_ast_syntax_alphabet_reference", "file_digest_verification", "source_range_evidence", "parser_status"],
    "output_schemas": ["ast_lua_extraction"],
    "artifact_patterns": ["manifests/extraction/ast_lua_extraction.json", "manifests/extraction/ast_lua_extraction.md"],
    "promotion_role": "intermediate_evidence",
    "canonical_status": "prototype",
}

SCRIPT_ID = "scripts.extraction.extract_ast_lua_runtime_signals"
SCHEMA = "ast_lua_extraction"
SCHEMA_VERSION = "1"
ARTIFACT_FAMILY = "ast_lua_extraction"

@dataclass
class AstAlphabet:
    path: str
    artifact_id: str | None
    content_digest: str | None
    node_families: list[dict[str, Any]]
    value_kind_rules: list[dict[str, Any]]
    glua_preprocessing: dict[str, Any]
    parser: dict[str, Any]
    mechanics: dict[str, Any]


def stable_hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_path(path: Path | str) -> str:
    return Path(path).as_posix() if isinstance(path, Path) else str(path).replace("\\", "/")


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON root must be object: {path}")
    return data


def load_alphabet(path: Path) -> AstAlphabet:
    data = load_json(path)
    if data.get("schema") != "lua_ast_syntax_alphabet" or data.get("artifact_family") != "lua_ast_syntax_alphabet":
        raise ValueError(f"Input is not lua_ast_syntax_alphabet: {path}")
    return AstAlphabet(
        path=normalize_path(path),
        artifact_id=data.get("artifact_id"),
        content_digest=data.get("content_digest"),
        node_families=list(data.get("node_families", [])),
        value_kind_rules=list(data.get("value_kind_rules", [])),
        glua_preprocessing=dict(data.get("glua_preprocessing", {})),
        parser=dict(data.get("parser", {})),
        mechanics=dict(data.get("mechanics", {})),
    )


def read_text_lossless(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return raw.decode("utf-8", errors="replace"), "utf-8-replace"


def line_starts(text: str) -> list[int]:
    starts = [0]
    for m in re.finditer("\n", text):
        starts.append(m.end())
    return starts


def line_for_offset(starts: list[int], offset: int) -> int:
    lo, hi = 0, len(starts)
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if starts[mid] <= offset:
            lo = mid
        else:
            hi = mid
    return lo + 1


def source_slice(text: str, start: int, end: int, limit: int = 240) -> str:
    s = text[start:end]
    return s[:limit]


def transform_glua(text: str, alphabet: AstAlphabet) -> tuple[str, list[int], list[dict[str, Any]]]:
    if not alphabet.glua_preprocessing.get("enabled", True):
        return text, list(range(len(text) + 1)), []
    out: list[str] = []
    mapping: list[int] = []
    changes: list[dict[str, Any]] = []
    i = 0
    in_s = in_d = esc = False
    in_line_comment = False
    while i < len(text):
        ch = text[i]
        nx = text[i + 1] if i + 1 < len(text) else ""
        if in_line_comment:
            out.append(ch); mapping.append(i)
            if ch == "\n": in_line_comment = False
            i += 1; continue
        if esc:
            out.append(ch); mapping.append(i); esc = False; i += 1; continue
        if ch == "\\" and (in_s or in_d):
            out.append(ch); mapping.append(i); esc = True; i += 1; continue
        if ch == "'" and not in_d:
            in_s = not in_s; out.append(ch); mapping.append(i); i += 1; continue
        if ch == '"' and not in_s:
            in_d = not in_d; out.append(ch); mapping.append(i); i += 1; continue
        if not in_s and not in_d and ch == "-" and nx == "-":
            out.append(ch); mapping.append(i); out.append(nx); mapping.append(i + 1); i += 2; in_line_comment = True; continue
        if not in_s and not in_d and text.startswith("!=", i):
            out.extend("~="); mapping.extend([i, i + 1]); changes.append({"rule_id":"not_equal_operator","start_offset":i,"end_offset":i+2}); i += 2; continue
        if not in_s and not in_d and text.startswith("&&", i):
            repl = " and "
            out.extend(repl); mapping.extend([i] * len(repl)); changes.append({"rule_id":"and_operator","start_offset":i,"end_offset":i+2}); i += 2; continue
        if not in_s and not in_d and text.startswith("||", i):
            repl = " or "
            out.extend(repl); mapping.extend([i] * len(repl)); changes.append({"rule_id":"or_operator","start_offset":i,"end_offset":i+2}); i += 2; continue
        if not in_s and not in_d and ch == "!" and nx != "=":
            repl = "not "
            out.extend(repl); mapping.extend([i] * len(repl)); changes.append({"rule_id":"not_operator","start_offset":i,"end_offset":i+1}); i += 1; continue
        if not in_s and not in_d and text.startswith("continue", i):
            before = text[i-1] if i > 0 else " "
            after = text[i+8] if i + 8 < len(text) else " "
            if not (before.isalnum() or before == "_") and not (after.isalnum() or after == "_"):
                repl = "do end"
                out.extend(repl); mapping.extend([i] * len(repl)); changes.append({"rule_id":"continue_keyword","start_offset":i,"end_offset":i+8}); i += 8; continue
        out.append(ch); mapping.append(i); i += 1
    mapping.append(len(text))
    return "".join(out), mapping, changes


def load_tree_sitter_parser(alphabet: AstAlphabet):
    package_errors = []
    try:
        from tree_sitter import Language, Parser  # type: ignore
    except Exception as ex:
        return None, {"status":"missing_dependency", "message":"Python package tree_sitter is not installed", "errors":[str(ex)]}

    def build_parser_from_language(raw: Any):
        """Return a Parser for both old and new py-tree-sitter APIs.

        Supported shapes seen in current packages:
        - tree_sitter_lua.language() returns a PyCapsule; newer py-tree-sitter
          needs Language(capsule).
        - helper packages may already return a Language.
        - newer Parser may accept Parser(language); older Parser needs
          parser.set_language(language); intermediate versions expose
          parser.language = language.
        """
        lang = raw if isinstance(raw, Language) else Language(raw)
        errors: list[str] = []
        try:
            return Parser(lang)
        except Exception as ex:
            errors.append(f"Parser(lang): {type(ex).__name__}: {ex}")
        try:
            parser = Parser()
            if hasattr(parser, "set_language"):
                parser.set_language(lang)
            else:
                parser.language = lang
            return parser
        except Exception as ex:
            errors.append(f"Parser()+set language: {type(ex).__name__}: {ex}")
            raise RuntimeError("; ".join(errors))

    packages = alphabet.parser.get("accepted_python_packages") or ["tree_sitter_language_pack", "tree_sitter_lua", "tree_sitter_languages"]
    for pkg in packages:
        try:
            if pkg == "tree_sitter_language_pack":
                mod = importlib.import_module(pkg)
                # Prefer package-native parser loader when available because it
                # handles py-tree-sitter API changes internally.
                if hasattr(mod, "get_parser"):
                    return mod.get_parser("lua"), {"status":"ok", "package":pkg, "loader":"get_parser"}
                lang = mod.get_language("lua")
                parser = build_parser_from_language(lang)
                return parser, {"status":"ok", "package":pkg, "loader":"get_language"}
            elif pkg == "tree_sitter_lua":
                mod = importlib.import_module(pkg)
                raw_lang = mod.language() if callable(getattr(mod, "language", None)) else getattr(mod, "language")
                parser = build_parser_from_language(raw_lang)
                return parser, {"status":"ok", "package":pkg, "loader":"language"}
            elif pkg == "tree_sitter_languages":
                mod = importlib.import_module(pkg)
                if hasattr(mod, "get_parser"):
                    return mod.get_parser("lua"), {"status":"ok", "package":pkg, "loader":"get_parser"}
                lang = mod.get_language("lua")
                parser = build_parser_from_language(lang)
                return parser, {"status":"ok", "package":pkg, "loader":"get_language"}
            else:
                continue
        except Exception as ex:
            package_errors.append({"package":pkg,"error_type":type(ex).__name__,"message":str(ex)})
    return None, {"status":"missing_lua_language", "message":"No supported Tree-sitter Lua language package loaded", "package_errors":package_errors}

def node_text(node: Any, original: str, transformed_mapping: list[int]) -> str:
    start = transformed_mapping[min(node.start_byte, len(transformed_mapping)-1)]
    end = transformed_mapping[min(node.end_byte, len(transformed_mapping)-1)]
    if end < start: end = start
    return original[start:end]


def node_range_payload(node: Any, original: str, transformed_mapping: list[int]) -> dict[str, Any]:
    starts = line_starts(original)
    start = transformed_mapping[min(node.start_byte, len(transformed_mapping)-1)]
    end = transformed_mapping[min(node.end_byte, len(transformed_mapping)-1)]
    if end < start: end = start
    return {"start_offset":start,"end_offset":end,"start_line":line_for_offset(starts,start),"end_line":line_for_offset(starts,end)}


def family_for_node(node_type: str, alphabet: AstAlphabet) -> dict[str, Any] | None:
    for fam in alphabet.node_families:
        if node_type in set(fam.get("node_types", [])):
            return fam
    return None


def value_kind_for_node(node_type: str, alphabet: AstAlphabet) -> str:
    for rule in alphabet.value_kind_rules:
        if node_type in set(rule.get("node_types", [])):
            return str(rule.get("value_kind"))
    for rule in alphabet.value_kind_rules:
        if rule.get("fallback"):
            return str(rule.get("value_kind"))
    return "expression"


def child_texts(node: Any, original: str, mapping: list[int]) -> list[str]:
    return [node_text(c, original, mapping).strip() for c in getattr(node, "children", []) if node_text(c, original, mapping).strip()]


def alphabet_mechanics(alphabet: AstAlphabet) -> dict[str, Any]:
    return dict(getattr(alphabet, "mechanics", {}) or {})


def node_parent_type(node: Any) -> str | None:
    parent = getattr(node, "parent", None)
    return getattr(parent, "type", None) if parent is not None else None


def should_suppress_node(node: Any, fam: dict[str, Any], alphabet: AstAlphabet) -> bool:
    mech = alphabet_mechanics(alphabet)
    if not mech.get("suppress_assignment_statement_child_inside_local_declaration", False):
        return False
    parent_type = node_parent_type(node)
    suppressed_parents = set(str(x) for x in fam.get("duplicate_child_node_types_suppressed_when_parent_type_in", []))
    return parent_type in suppressed_parents


def is_single_assignment_operator(text: str, pos: int) -> bool:
    if pos < 0 or pos >= len(text) or text[pos] != "=":
        return False
    prev = text[pos - 1] if pos > 0 else ""
    nxt = text[pos + 1] if pos + 1 < len(text) else ""
    return prev not in "<>~=" and nxt != "="


def find_top_level_single_equals(text: str) -> int | None:
    par = br = brace = 0
    ins = ind = esc = False
    for i, ch in enumerate(text):
        if esc:
            esc = False; continue
        if ch == "\\" and (ins or ind):
            esc = True; continue
        if ch == "'" and not ind:
            ins = not ins; continue
        if ch == '"' and not ins:
            ind = not ind; continue
        if ins or ind:
            continue
        if ch == "(": par += 1
        elif ch == ")" and par > 0: par -= 1
        elif ch == "[": br += 1
        elif ch == "]" and br > 0: br -= 1
        elif ch == "{": brace += 1
        elif ch == "}" and brace > 0: brace -= 1
        elif ch == "=" and par == 0 and br == 0 and brace == 0 and is_single_assignment_operator(text, i):
            return i
    return None


def split_top_level_csv(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    par = br = brace = 0
    ins = ind = esc = False
    for i, ch in enumerate(text):
        if esc:
            esc = False; continue
        if ch == "\\" and (ins or ind):
            esc = True; continue
        if ch == "'" and not ind:
            ins = not ins; continue
        if ch == '"' and not ins:
            ind = not ind; continue
        if ins or ind:
            continue
        if ch == "(": par += 1
        elif ch == ")" and par > 0: par -= 1
        elif ch == "[": br += 1
        elif ch == "]" and br > 0: br -= 1
        elif ch == "{": brace += 1
        elif ch == "}" and brace > 0: brace -= 1
        elif ch == "," and par == 0 and br == 0 and brace == 0:
            parts.append(text[start:i].strip()); start = i + 1
    tail = text[start:].strip()
    if tail or text.strip():
        parts.append(tail)
    return parts


def balanced_call_parts(text: str) -> tuple[str, str, list[str]]:
    ins = ind = esc = False
    open_idx = None
    for i, ch in enumerate(text):
        if esc:
            esc = False; continue
        if ch == "\\" and (ins or ind):
            esc = True; continue
        if ch == "'" and not ind:
            ins = not ins; continue
        if ch == '"' and not ins:
            ind = not ind; continue
        if ins or ind:
            continue
        if ch == "(":
            open_idx = i; break
    if open_idx is None:
        return text.strip(), "", []
    depth = 0
    ins = ind = esc = False
    close_idx = None
    for i in range(open_idx, len(text)):
        ch = text[i]
        if esc:
            esc = False; continue
        if ch == "\\" and (ins or ind):
            esc = True; continue
        if ch == "'" and not ind:
            ins = not ins; continue
        if ch == '"' and not ins:
            ind = not ind; continue
        if ins or ind:
            continue
        if ch == "(": depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                close_idx = i; break
    if close_idx is None:
        args_text = text[open_idx + 1:]
    else:
        args_text = text[open_idx + 1:close_idx]
    return text[:open_idx].strip(), args_text.strip(), split_top_level_csv(args_text)


def parameters_from_function_text(text: str) -> list[str]:
    symbol_part, args_text, args = balanced_call_parts(text)
    if "function" not in symbol_part:
        return []
    return [x for x in args if x]


def symbol_from_function_text(text: str) -> str | None:
    before_paren, _, _ = balanced_call_parts(text)
    before = before_paren.strip()
    if before.startswith("local function "):
        return before[len("local function "):].strip() or None
    if before.startswith("function "):
        return before[len("function "):].strip() or None
    return None


def classify_text_value(text: str, alphabet: AstAlphabet) -> str:
    s = text.strip()
    if not s:
        return "empty"
    if s.startswith("{"):
        return "table_literal"
    if s.startswith("function"):
        return "function_literal"
    if s in {"true", "false"}:
        return "boolean_literal"
    if s == "nil":
        return "nil_literal"
    if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", s):
        return "number_literal"
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        return "string_literal"
    return "expression"


def negative_number_text_if_owned(node: Any, original: str, mapping: list[int]) -> str | None:
    rg = node_range_payload(node, original, mapping)
    start = int(rg["start_offset"])
    if start <= 0 or original[start - 1] != "-":
        return None
    before = original[start - 2] if start >= 2 else " "
    if before.isalnum() or before == "_":
        return None
    return "-" + node_text(node, original, mapping).strip()


def payload_allowed_fields(fam: dict[str, Any]) -> set[str]:
    return {str(x) for x in fam.get("allowed_fields", [])}


def enforce_allowed_payload(payload: dict[str, Any], fam: dict[str, Any], alphabet: AstAlphabet) -> dict[str, Any]:
    mech = alphabet_mechanics(alphabet)
    allowed = payload_allowed_fields(fam)
    if not allowed or not mech.get("enforce_allowed_fields", False):
        return payload
    always = {"ast_node_type", "source_preview", "source_truncated", "child_previews"}
    allowed = allowed | always
    return {k: v for k, v in payload.items() if k in allowed}


def assignment_payload_from_text(node: Any, txt: str, fam: dict[str, Any], alphabet: AstAlphabet) -> dict[str, Any]:
    local_types = set(str(x) for x in fam.get("local_node_types", []))
    is_local = getattr(node, "type", "") in local_types
    local_prefix = str(alphabet_mechanics(alphabet).get("local_declaration_prefix", "local"))
    working = txt.strip()
    if working.startswith(local_prefix + " "):
        is_local = True
        working = working[len(local_prefix):].strip()
    eq = find_top_level_single_equals(working)
    lhs = working[:eq].strip() if eq is not None else working.strip()
    rhs = working[eq + 1:].strip() if eq is not None else ""
    payload: dict[str, Any] = {"lhs": lhs or None, "is_local": bool(is_local), "rhs_kind": classify_text_value(rhs, alphabet), "rhs_preview": rhs[:240]}
    lhs_parts = split_top_level_csv(lhs)
    rhs_parts = split_top_level_csv(rhs)
    if len(lhs_parts) > 1:
        payload["multi_assignment_group"] = "ast_lua_multi_assignment:" + stable_hash({"lhs": lhs_parts, "rhs": rhs_parts, "text": txt})[:16]
    return payload


def call_payload_from_text(txt: str) -> tuple[str, dict[str, Any]]:
    symbol, args_text, args = balanced_call_parts(txt)
    kind = "lua_method_call_expression" if ":" in symbol else "lua_call_expression"
    return kind, {"symbol": symbol, "arguments_preview": args_text[:240], "argument_count": len(args), "argument_kinds": [classify_text_value(x, None) for x in args]}


def table_field_payload_from_text(txt: str, alphabet: AstAlphabet) -> dict[str, Any]:
    eq = find_top_level_single_equals(txt)
    if eq is None:
        return {"key_syntax":"positional_field","key_text":None,"key_expression":None,"value_kind":classify_text_value(txt, alphabet),"value_preview":txt[:240],"context_path":[]}
    key = txt[:eq].strip()
    val = txt[eq + 1:].strip().rstrip(",").strip()
    return {"key_syntax":"computed_key" if key.startswith("[") else "identifier_key","key_text":key,"key_expression":key[1:-1].strip() if key.startswith("[") and key.endswith("]") else key,"value_kind":classify_text_value(val, alphabet),"value_preview":val[:240],"context_path":[]}


def literal_payload_from_node(node: Any, txt: str, alphabet: AstAlphabet, original: str, mapping: list[int]) -> dict[str, Any]:
    node_type = getattr(node, "type", "unknown")
    val = negative_number_text_if_owned(node, original, mapping) if node_type == "number" else None
    if val is None:
        val = txt[:240]
    return {"literal_kind":value_kind_for_node(node_type, alphabet),"literal_form":"ast_literal","value":val}


def function_payload_from_text(node: Any, txt: str, original: str, mapping: list[int], anonymous: bool = False) -> dict[str, Any]:
    rg = node_range_payload(node, original, mapping)
    payload = {"parameters": parameters_from_function_text(txt), "body_span":{"start_line":rg["start_line"],"end_line":rg["end_line"],"complete":True}}
    if not anonymous:
        payload["symbol"] = symbol_from_function_text(txt)
    return payload

def emit(kind: str, file_record: dict[str, Any], node: Any, original: str, mapping: list[int], payload: dict[str, Any]) -> dict[str, Any]:
    rg = node_range_payload(node, original, mapping)
    starts = line_starts(original)
    line = rg["start_line"]
    line_start = starts[line-1]
    line_end = original.find("\n", line_start)
    if line_end < 0: line_end = len(original)
    evidence = {"file_id":file_record.get("file_id"),"source_root_index":file_record.get("source_root_index"),"relative_path":file_record.get("relative_path"),"absolute_path":file_record.get("absolute_path"),"realm_hint":file_record.get("realm_hint"),"line":line,"text":original[line_start:line_end]}
    base = {"kind":kind,"range":rg,"evidence":evidence}
    base.update(payload)
    base["evidence_id"] = "ast_lua_evidence:" + stable_hash({"kind":kind,"file_id":file_record.get("file_id"),"range":rg,"payload":payload})[:16]
    return base


def extract_node_payload(node: Any, fam: dict[str, Any], original: str, mapping: list[int], alphabet: AstAlphabet) -> tuple[str, dict[str, Any]]:
    txt = node_text(node, original, mapping).strip()
    node_type = getattr(node, "type", "unknown")
    strategy = str(fam.get("payload_strategy", "generic_node_preview"))
    kind = str(fam.get("evidence_kind", "lua_ast_node"))
    payload: dict[str, Any] = {"ast_node_type":node_type,"source_preview":txt[:240],"source_truncated":len(txt)>240}
    if strategy == "assignment_from_statement_text":
        payload.update(assignment_payload_from_text(node, txt, fam, alphabet))
    elif strategy == "call_from_statement_text":
        call_kind, call_payload = call_payload_from_text(txt)
        if call_kind == "lua_method_call_expression" and fam.get("method_evidence_kind"):
            kind = str(fam["method_evidence_kind"])
        else:
            kind = str(fam.get("evidence_kind", call_kind))
        payload.update(call_payload)
    elif strategy == "table_field_from_field_text":
        payload.update(table_field_payload_from_text(txt, alphabet))
    elif strategy == "literal_from_node_text":
        payload.update(literal_payload_from_node(node, txt, alphabet, original, mapping))
    elif strategy == "function_definition_from_statement_text":
        payload.update(function_payload_from_text(node, txt, original, mapping, anonymous=False))
    elif strategy == "anonymous_function_from_statement_text":
        payload.update(function_payload_from_text(node, txt, original, mapping, anonymous=True))
    payload["child_previews"] = child_texts(node, original, mapping)[:12]
    payload = enforce_allowed_payload(payload, fam, alphabet)
    return str(kind), payload


def walk(node: Any) -> Iterable[Any]:
    yield node
    for child in getattr(node, "children", []):
        yield from walk(child)


def count_by(items: Iterable[dict[str, Any]], key: str) -> dict[str, int]:
    out: dict[str, int] = {}
    for item in items:
        v = str(item.get(key, "unknown"))
        out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items()))


def extract_from_file(file_record: dict[str, Any], parser: Any, alphabet: AstAlphabet) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    path = Path(str(file_record["absolute_path"]))
    expected = str(file_record.get("sha256", ""))
    actual = file_sha256(path)
    original, enc = read_text_lossless(path)
    transformed, mapping, changes = transform_glua(original, alphabet)
    tree = parser.parse(transformed.encode("utf-8"))
    root = tree.root_node
    items: list[dict[str, Any]] = []
    unsupported: dict[str, int] = {}
    for node in walk(root):
        nt = getattr(node, "type", "unknown")
        fam = family_for_node(nt, alphabet)
        if not fam:
            unsupported[nt] = unsupported.get(nt, 0) + 1
            continue
        if should_suppress_node(node, fam, alphabet):
            continue
        kind, payload = extract_node_payload(node, fam, original, mapping, alphabet)
        items.append(emit(kind, file_record, node, original, mapping, payload))
    has_error = bool(getattr(root, "has_error", False))
    summary = {"file_id":file_record.get("file_id"),"relative_path":file_record.get("relative_path"),"absolute_path":file_record.get("absolute_path"),"realm_hint":file_record.get("realm_hint"),"expected_sha256":expected,"actual_sha256":actual,"digest_status":"match" if expected == actual else "mismatch","encoding":enc,"parse_status":"parsed_with_errors" if has_error else "parsed","syntax_error_count":unsupported.get("ERROR", 0),"transformation_count":len(changes),"transformations":changes[:50],"evidence_total":len(items),"evidence_kind_counts":count_by(items,"kind"),"unsupported_node_type_counts":dict(sorted(unsupported.items()))}
    return items, summary


def validate_manifest(manifest: dict[str, Any], path: Path) -> None:
    if manifest.get("schema") != "source_file_manifest" or manifest.get("artifact_family") != "source_file_manifest":
        raise ValueError(f"Input is not source_file_manifest: {path}")
    if not isinstance(manifest.get("source_files"), list):
        raise ValueError("source_files must be list")


def build_artifact(workspace: Path, input_manifest_path: Path, alphabet_path: Path, fail_on_digest_mismatch: bool) -> dict[str, Any]:
    manifest = load_json(input_manifest_path); validate_manifest(manifest, input_manifest_path)
    alphabet = load_alphabet(alphabet_path)
    parser, parser_info = load_tree_sitter_parser(alphabet)
    items: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    if parser is None:
        errors.append({"error_type":"ParserUnavailable","message":parser_info.get("message"),"parser_info":parser_info})
    else:
        for rec in manifest["source_files"]:
            try:
                ev, sm = extract_from_file(rec, parser, alphabet)
                items.extend(ev); summaries.append(sm)
            except Exception as ex:
                errors.append({"file_id":rec.get("file_id"),"relative_path":rec.get("relative_path"),"absolute_path":rec.get("absolute_path"),"error_type":type(ex).__name__,"message":str(ex)})
    mismatches = [x for x in summaries if x.get("digest_status") != "match"]
    if fail_on_digest_mismatch and mismatches:
        raise ValueError(f"Digest mismatch in {len(mismatches)} files")
    content_digest = stable_hash({"source_manifest":manifest.get("artifact_id"),"ast_alphabet":alphabet.artifact_id,"parser_info":parser_info,"summaries":summaries,"errors":errors,"evidence_ids":[x.get("evidence_id") for x in items]})
    return {"schema":SCHEMA,"schema_version":SCHEMA_VERSION,"artifact_family":ARTIFACT_FAMILY,"artifact_id":f"{ARTIFACT_FAMILY}:{content_digest[:16]}","producer_script":SCRIPT_ID,"pipeline_stage":"extraction","canonical_status":"prototype","promotion_role":"intermediate_evidence","generated_at":datetime.utcnow().replace(microsecond=0).isoformat()+"Z","required_capabilities":PIPELINE_CONTRACT["required_output_capabilities"],"content_digest":content_digest,"workspace":normalize_path(workspace),"parser":parser_info,"source_manifest":{"path":normalize_path(input_manifest_path),"artifact_id":manifest.get("artifact_id"),"content_digest":manifest.get("content_digest"),"schema":manifest.get("schema"),"schema_version":manifest.get("schema_version")},"lua_ast_syntax_alphabet":{"path":alphabet.path,"artifact_id":alphabet.artifact_id,"content_digest":alphabet.content_digest},"summary":{"files_total":len(manifest["source_files"]),"files_extracted":len(summaries),"files_failed":len(errors),"digest_mismatch_files":len(mismatches),"evidence_total":len(items),"evidence_kind_counts":count_by(items,"kind"),"realm_hint_counts":count_by(summaries,"realm_hint")},"file_summaries":summaries,"evidence_items":items,"errors":errors,"lineage":{"input_kind":"pipeline_artifact","input_artifacts":[normalize_path(input_manifest_path),normalize_path(alphabet_path)],"parent_artifact_id":manifest.get("artifact_id"),"regenerates":None,"regeneration_inputs":{"producer_script":SCRIPT_ID,"schema":SCHEMA,"schema_version":SCHEMA_VERSION,"source_file_manifest":normalize_path(input_manifest_path),"lua_ast_syntax_alphabet":normalize_path(alphabet_path)}}}


def write_json(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, artifact: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# AST Lua Extraction", "", f"- Artifact ID: `{artifact['artifact_id']}`", f"- Producer: `{artifact['producer_script']}`", f"- Parser status: `{artifact.get('parser',{}).get('status')}`", f"- Source manifest: `{artifact['source_manifest']['path']}`", f"- Lua AST syntax alphabet: `{artifact['lua_ast_syntax_alphabet']['path']}`", "", "## Summary"]
    for k, v in artifact["summary"].items():
        lines.append(f"- `{k}`: `{v}`")
    if artifact.get("errors"):
        lines.extend(["", "## Errors"])
        for err in artifact["errors"][:20]:
            lines.append(f"- `{err.get('error_type')}`: {err.get('message')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prototype Tree-sitter Lua AST syntax extraction.")
    p.add_argument("--workspace", required=True)
    p.add_argument("--input-manifest")
    p.add_argument("--lua-ast-syntax-alphabet")
    p.add_argument("--out-json")
    p.add_argument("--out-md")
    p.add_argument("--fail-on-digest-mismatch", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    ws = Path(args.workspace).resolve()
    if not ws.is_dir():
        raise NotADirectoryError(f"Workspace is not a directory: {ws}")
    im = Path(args.input_manifest) if args.input_manifest else ws / "manifests" / "extraction" / "source_file_manifest.json"
    al = Path(args.lua_ast_syntax_alphabet) if args.lua_ast_syntax_alphabet else ws / "manifests" / "alphabet" / "lua_ast_syntax_alphabet.json"
    im = (ws / im).resolve() if not im.is_absolute() else im.resolve()
    al = (ws / al).resolve() if not al.is_absolute() else al.resolve()
    artifact = build_artifact(ws, im, al, args.fail_on_digest_mismatch)
    oj = Path(args.out_json) if args.out_json else ws / "manifests" / "extraction" / "ast_lua_extraction.json"
    om = Path(args.out_md) if args.out_md else ws / "manifests" / "extraction" / "ast_lua_extraction.md"
    oj = (ws / oj).resolve() if not oj.is_absolute() else oj.resolve()
    om = (ws / om).resolve() if not om.is_absolute() else om.resolve()
    write_json(oj, artifact); write_md(om, artifact)
    print(f"Parser status: {artifact.get('parser',{}).get('status')}")
    print(f"AST Lua evidence: {artifact['summary']['evidence_total']}")
    print(f"Files extracted: {artifact['summary']['files_extracted']}")
    print(f"Digest mismatches: {artifact['summary']['digest_mismatch_files']}")
    print(f"Wrote JSON: {oj}")
    print(f"Wrote MD: {om}")


if __name__ == "__main__":
    main()
