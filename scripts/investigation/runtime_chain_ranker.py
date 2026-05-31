from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


CATEGORY_WEIGHTS = {
    "inventory_membership": 90,
    "item_metadata": 90,
    "item_metadata_client_apply": 100,
    "network_send": 80,
    "network_receive": 80,
    "client_apply": 75,
    "ui_refresh": 70,
    "hook_event": 60,
    "server_mutation": 60,
    "persistence": 25,
    "incidental": -35,
}

TERM_WEIGHTS = {
    "vendorsellitem": 45,
    "vendorsprice": 45,
    "vendorqty": 30,
    "vendormqty": 30,
    "vendorbprice": 20,
    "setdata": 35,
    "item:setdata": 45,
    "function item:setdata": 45,
    "invdata": 55,
    "netstream.hook(\"invdata\"": 70,
    "itemdatachanged": 65,
    "hook.run(\"itemdatachanged\"": 70,
    "inventoryitemdatachanged": 40,
    "populateitems": 30,
    "nutinventoryadd": 40,
    "inventoryitemadded": 35,
    "syncitemadded": 40,
    "item:sync": 35,
    "getrecipients": 30,
    "netstream.start": 35,
    "netstream.hook": 45,
    "net.receive": 30,
    "net.start": 30,
    "hook.run": 25,
    "inventory:add": 35,
    "removeitem": 35,
    "additem": 30,
}


@dataclass
class RankedEvidence:
    rank: int
    score: float
    category: str
    file: str
    line: int | None
    pattern: str
    text: str
    source: str
    scope_hits: int
    reasons: list[str]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(obj: Any) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    def walk(x: Any) -> None:
        if isinstance(x, dict):
            if looks_like_evidence(x):
                out.append(x)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(obj)
    return out


def looks_like_evidence(d: dict[str, Any]) -> bool:
    keys = {k.lower() for k in d}
    return bool(
        {"file", "path", "source_file", "source"} & keys
        or {"text", "snippet", "fragment", "evidence", "content"} & keys
        or {"line", "line_start", "start_line"} & keys
        or {"pattern", "matched_terms", "needle"} & keys
    )


def pick(d: dict[str, Any], *names: str, default: Any = "") -> Any:
    for name in names:
        if name in d and d[name] not in (None, ""):
            return d[name]
    lower = {k.lower(): v for k, v in d.items()}
    for name in names:
        v = lower.get(name.lower())
        if v not in (None, ""):
            return v
    return default


def as_int(v: Any) -> int | None:
    try:
        return int(v)
    except Exception:
        return None


def norm(v: Any) -> str:
    if isinstance(v, list):
        return " ".join(str(x) for x in v)
    if isinstance(v, dict):
        return json.dumps(v, ensure_ascii=False)
    return str(v or "")


def tokenize_scope(scope: str) -> list[str]:
    return [
        t.lower()
        for t in re.split(r"[^a-zA-Z0-9_:\"]+", scope)
        if len(t.strip()) >= 3
    ]


def blob(file: str, pattern: str, text: str) -> str:
    return f"{file}\n{pattern}\n{text}".lower().replace("\\", "/")


def scope_score(b: str, terms: list[str]) -> tuple[int, float, list[str]]:
    if not terms:
        return 0, 0.0, []

    hits = 0
    bonus = 0.0
    reasons: list[str] = []

    for t in terms:
        if t in b:
            hits += 1
            bonus += 8
            reasons.append(f"scope:{t}=+8")

    if hits == 0:
        bonus -= 45
        reasons.append("off_scope_penalty=-45")
    elif hits >= 3:
        bonus += 25
        reasons.append("strong_scope_match=+25")

    return hits, bonus, reasons


def is_item_metadata_client_apply(b: str) -> bool:
    return (
        "gamemode/core/libs/item/cl_networking.lua" in b
        or (
            "netstream.hook" in b
            and "invdata" in b
            and "itemdatachanged" in b
        )
        or (
            "item.data" in b
            and "hook.run" in b
            and "itemdatachanged" in b
        )
    )


def classify(b: str) -> tuple[str, list[str]]:
    reasons: list[str] = []

    if is_item_metadata_client_apply(b):
        reasons.append("client item metadata apply boundary")
        return "item_metadata_client_apply", reasons

    if any(x in b for x in ["item:setdata", "function item:setdata", "invdata", "itemdatachanged", "vendorbprice", "vendorsprice"]):
        reasons.append("item metadata propagation")
        return "item_metadata", reasons

    if any(x in b for x in ["syncitemadded", "nutinventoryadd", "inventory:add", "additem", "removeitem", "oldinventory", "inventory.items"]):
        reasons.append("inventory membership propagation")
        return "inventory_membership", reasons

    if "net.receive" in b or "netstream.hook" in b or re.search(r"\breceive\b", b):
        reasons.append("network receive/apply boundary")
        return "network_receive", reasons

    if "net.start" in b or "netstream.start" in b or re.search(r"\bsend\b", b):
        reasons.append("network send boundary")
        return "network_send", reasons

    if "populateitems" in b or "inventoryitemdatachanged" in b or "derma" in b or "panel" in b:
        reasons.append("UI refresh boundary")
        return "ui_refresh", reasons

    if "hook.run" in b:
        reasons.append("hook event boundary")
        return "hook_event", reasons

    if any(x in b for x in ["database", "persist", "nosave"]):
        reasons.append("persistence behavior")
        return "persistence", reasons

    reasons.append("weak/incidental")
    return "incidental", reasons


def path_scope_adjustment(file: str, scope: str) -> tuple[float, list[str]]:
    f = file.lower().replace("\\", "/")
    s = scope.lower()
    score = 0.0
    reasons: list[str] = []

    preferred_paths = [
        "plugins/gridinv/sv_transfer.lua",
        "gamemode/core/meta/inventory/sv_base_inventory.lua",
        "gamemode/core/meta/inventory/cl_base_inventory.lua",
        "gamemode/core/meta/item/sv_item.lua",
        "gamemode/core/libs/item/cl_networking.lua",
        "plugins/gridinv/plugins/gridinvui/derma/cl_grid_inventory_panel.lua",
    ]

    for p in preferred_paths:
        if p in f:
            score += 35
            reasons.append(f"preferred_chain_file=+35:{p}")
            break

    if "gamemode/core/libs/item/cl_networking.lua" in f:
        score += 75
        reasons.append("preferred_item_client_apply_file=+75")

    if "vendor" in s and "plugins/vendor/" in f:
        score += 10
        reasons.append("vendor_file_weak_boost=+10")

    off_scope_paths = [
        "plugins/storage/",
        "plugins/multichar/",
        "plugins/healthproblems/",
        "plugins/needs/",
        "plugins/lightitems/",
    ]

    for p in off_scope_paths:
        if p in f and p.strip("/").split("/")[-1] not in s:
            score -= 60
            reasons.append(f"off_chain_subsystem_penalty=-60:{p}")
            break

    if "_disabled" in f or "legacy" in f:
        score -= 80
        reasons.append("legacy_disabled_penalty=-80")

    return score, reasons


def score_item(file: str, pattern: str, text: str, category: str, scope_terms: list[str], scope: str, external: Any) -> tuple[float, int, list[str]]:
    b = blob(file, pattern, text)
    score = float(CATEGORY_WEIGHTS.get(category, 0))
    reasons = [f"category={category}:{CATEGORY_WEIGHTS.get(category, 0)}"]

    hits, sb, sr = scope_score(b, scope_terms)
    score += sb
    reasons.extend(sr)

    pb, pr = path_scope_adjustment(file, scope)
    score += pb
    reasons.extend(pr)

    for term, weight in TERM_WEIGHTS.items():
        if term in b:
            score += weight
            reasons.append(f"term:{term}=+{weight}")

    if is_item_metadata_client_apply(b):
        score += 100
        reasons.append("client_item_metadata_apply_bonus=+100")

    try:
        ext = float(external)
        if ext:
            bonus = min(ext / 12.0, 35.0)
            score += bonus
            reasons.append(f"external_score_bonus={bonus:.2f}")
    except Exception:
        pass

    if len(text.strip()) < 20:
        score -= 20
        reasons.append("short_fragment_penalty=-20")

    return score, hits, reasons


def dedupe_key(file: str, line: int | None, pattern: str, text: str) -> str:
    f = file.lower().replace("\\", "/")
    p = re.sub(r"\s+", " ", pattern.lower()).strip()
    t = re.sub(r"\s+", " ", text.lower()).strip()[:120]
    return f"{f}:{line}:{p}:{t}"


def cluster_key(file: str, line: int | None) -> str:
    f = file.lower().replace("\\", "/")
    if line is None:
        return f"{f}:unknown"
    bucket = int(line / 10) * 10
    return f"{f}:{bucket}"


def rank(paths: list[Path], scope: str, max_per_cluster: int) -> list[RankedEvidence]:
    scope_terms = tokenize_scope(scope)
    items: list[RankedEvidence] = []

    for path in paths:
        data = load_json(path)
        for ev in flatten(data):
            file = str(pick(ev, "file", "path", "source_file", "source", default=""))
            line = as_int(pick(ev, "line", "line_start", "start_line", default=None))
            pattern = norm(pick(ev, "pattern", "matched_terms", "needle", default=""))
            text = norm(pick(ev, "text", "snippet", "fragment", "evidence", "content", default=""))
            external = pick(ev, "score", "weight", default=0)

            b = blob(file, pattern, text)
            category, class_reasons = classify(b)
            score, hits, score_reasons = score_item(file, pattern, text, category, scope_terms, scope, external)

            items.append(
                RankedEvidence(
                    rank=0,
                    score=score,
                    category=category,
                    file=file,
                    line=line,
                    pattern=pattern,
                    text=text[:3000],
                    source=path.as_posix(),
                    scope_hits=hits,
                    reasons=class_reasons + score_reasons,
                )
            )

    best_by_key: dict[str, RankedEvidence] = {}
    for item in items:
        key = dedupe_key(item.file, item.line, item.pattern, item.text)
        old = best_by_key.get(key)
        if old is None or item.score > old.score:
            best_by_key[key] = item

    sorted_items = sorted(best_by_key.values(), key=lambda x: x.score, reverse=True)

    cluster_counts: dict[str, int] = {}
    filtered: list[RankedEvidence] = []

    for item in sorted_items:
        ck = cluster_key(item.file, item.line)
        cluster_counts[ck] = cluster_counts.get(ck, 0) + 1
        if cluster_counts[ck] <= max_per_cluster:
            filtered.append(item)

    for i, item in enumerate(filtered, 1):
        item.rank = i

    return filtered


def write_md(items: list[RankedEvidence], out: Path, top_n: int, scope: str) -> None:
    lines = [
        "# Runtime Chain Ranked Evidence",
        "",
        f"Scope: `{scope}`",
        f"Total ranked evidence: **{len(items)}**",
        "",
    ]

    for item in items[:top_n]:
        lines.extend(
            [
                f"## {item.rank}. {item.category} — score {item.score:.2f}",
                "",
                f"- File: `{item.file}`",
                f"- Line: `{item.line}`",
                f"- Pattern: `{item.pattern}`",
                f"- Scope hits: `{item.scope_hits}`",
                f"- Source: `{item.source}`",
                f"- Reasons: `{', '.join(item.reasons)}`",
                "",
                "```text",
                item.text.strip()[:2000],
                "```",
                "",
            ]
        )

    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Rank validated evidence for runtime-chain reconstruction.")
    ap.add_argument("--input", nargs="+", required=True, type=Path)
    ap.add_argument("--scope", required=True)
    ap.add_argument("--out-json", required=True, type=Path)
    ap.add_argument("--out-md", required=True, type=Path)
    ap.add_argument("--top-n", type=int, default=50)
    ap.add_argument("--max-per-cluster", type=int, default=3)
    args = ap.parse_args()

    ranked = rank(args.input, args.scope, args.max_per_cluster)

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(
            {
                "schema": "runtime_chain_ranked_evidence.v3",
                "scope": args.scope,
                "inputs": [p.as_posix() for p in args.input],
                "total_ranked": len(ranked),
                "ranked_evidence": [asdict(x) for x in ranked],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    write_md(ranked, args.out_md, args.top_n, args.scope)

    print(f"Ranked evidence: {len(ranked)}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()