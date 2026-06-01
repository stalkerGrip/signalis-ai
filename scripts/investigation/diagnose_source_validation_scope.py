from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections import defaultdict


EXPECTED_STAGES = {
    "vendor_inventory_remove": ["oldInventory", "vendor", "remove"],
    "player_inventory_add": ["inventory:add", ":add(", "character inventory"],
    "item_sync": ["item:sync", ":sync(", "nutInventoryAdd"],
    "vendor_metadata_cleanup": ["vendorQty", "vendorSPrice", "vendorMQty", "vendorBPrice"],
    "item_metadata_mutation": ["setData", "ITEM:setData", "item:setData"],
    "item_metadata_client_apply": ["invData", "ItemDataChanged"],
    "ui_refresh": ["populateItems", "refresh", "grid_inventory"],
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def walk_strings(value):
    if isinstance(value, dict):
        for v in value.values():
            yield from walk_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from walk_strings(v)
    elif value is not None:
        yield str(value)


def collect_evidence_nodes(data):
    nodes = []

    def walk(value):
        if isinstance(value, dict):
            text = " ".join(walk_strings(value))
            if any(k in value for k in ("file", "path", "evidence", "snippet", "fragments", "needles_found")):
                nodes.append(value | {"__text": text})
            for v in value.values():
                walk(v)
        elif isinstance(value, list):
            for v in value:
                walk(v)

    walk(data)
    return nodes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-validation", required=True, type=Path)
    parser.add_argument("--out-json", required=True, type=Path)
    parser.add_argument("--out-md", required=True, type=Path)
    args = parser.parse_args()

    data = load_json(args.source_validation)
    nodes = collect_evidence_nodes(data)

    files = defaultdict(int)
    stage_hits = defaultdict(list)

    for i, node in enumerate(nodes):
        text = node.get("__text", "")
        text_lower = text.lower()

        file_name = node.get("file") or node.get("path") or node.get("source_file") or "unknown"
        files[file_name] += 1

        for stage, needles in EXPECTED_STAGES.items():
            hits = [n for n in needles if n.lower() in text_lower]
            if hits:
                stage_hits[stage].append({
                    "node": i,
                    "file": file_name,
                    "hits": hits,
                })

    present = [s for s in EXPECTED_STAGES if s in stage_hits]
    missing = [s for s in EXPECTED_STAGES if s not in stage_hits]

    client_only = (
        len(files) == 1
        and any("cl_networking.lua" in str(f).replace("\\", "/") for f in files)
        and "item_metadata_client_apply" in present
        and len(missing) >= 4
    )

    if client_only:
        verdict = "source_validation_scope_collapsed_to_client_apply"
    elif missing:
        verdict = "source_validation_incomplete_for_vendor_chain"
    else:
        verdict = "source_validation_covers_expected_vendor_chain"

    result = {
        "source_validation": str(args.source_validation),
        "evidence_nodes_detected": len(nodes),
        "files": dict(files),
        "present_stages": present,
        "missing_stages": missing,
        "verdict": verdict,
        "stage_hits": dict(stage_hits),
    }

    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Source Validation Scope Diagnosis",
        "",
        f"- Source validation: `{args.source_validation}`",
        f"- Evidence nodes detected: `{len(nodes)}`",
        f"- Files detected: `{len(files)}`",
        f"- Present stages: `{len(present)}`",
        f"- Missing stages: `{len(missing)}`",
        f"- Verdict: `{verdict}`",
        "",
        "## Files",
        "",
    ]

    for file_name, count in sorted(files.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"- `{file_name}`: `{count}`")

    lines += ["", "## Present Stages", ""]

    for stage in present:
        lines.append(f"### `{stage}`")
        for hit in stage_hits[stage]:
            lines.append(f"- Node `{hit['node']}` file=`{hit['file']}` hits=`{hit['hits']}`")
        lines.append("")

    lines += ["## Missing Stages", ""]

    for stage in missing:
        lines.append(f"- `{stage}`")

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Verdict: {verdict}")
    print(f"Evidence nodes: {len(nodes)}")
    print(f"Files: {len(files)}")
    print(f"Present stages: {len(present)}")
    print(f"Missing stages: {len(missing)}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")


if __name__ == "__main__":
    main()