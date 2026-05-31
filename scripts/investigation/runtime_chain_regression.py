#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def get_chain_name(path: Path, data: dict[str, Any]) -> str:
    return (
        data.get("name")
        or data.get("chain_name")
        or data.get("title")
        or path.stem
    )

def find_first_key(data: Any, keys: set[str]) -> Any:
    if isinstance(data, dict):
        for key, value in data.items():
            if key in keys:
                return value
        for value in data.values():
            found = find_first_key(value, keys)
            if found is not None:
                return found

    if isinstance(data, list):
        for item in data:
            found = find_first_key(item, keys)
            if found is not None:
                return found

    return None

def get_confidence(data: dict[str, Any]) -> str:
    value = find_first_key(data, {
        "confidence",
        "promotion_confidence",
        "chain_confidence",
        "branch_chain_confidence",
    })
    return str(value or "unknown")


def get_score(data: dict[str, Any]) -> float:
    value = find_first_key(data, {
        "score",
        "promotion_score",
        "chain_score",
        "branch_chain_score",
    })
    try:
        return float(value)
    except Exception:
        return 0.0


def get_missing_steps(data: dict[str, Any]) -> list[str]:
    value = find_first_key(data, {
        "missing_required_steps",
        "missing_steps",
        "missing_categories",
    })

    if value in (None, "none", "None"):
        return []

    if isinstance(value, str):
        return [] if value.strip().lower() == "none" else [value]

    if isinstance(value, list):
        return [str(x) for x in value]

    return [str(value)]


def get_branches(data: dict[str, Any]) -> list[dict[str, Any]]:
    value = find_first_key(data, {
        "branches",
        "branch_topology",
    })

    if isinstance(value, dict):
        return [v for v in value.values() if isinstance(v, dict)]

    if isinstance(value, list):
        return [v for v in value if isinstance(v, dict)]

    return []


def assess_chain(path: Path, min_score: float, allow_medium: bool) -> dict[str, Any]:
    data = load_json(path)

    name = get_chain_name(path, data)
    confidence = get_confidence(data)
    score = get_score(data)
    missing_steps = get_missing_steps(data)
    branches = get_branches(data)

    failures: list[str] = []
    warnings: list[str] = []

    if confidence == "unknown":
        warnings.append("confidence_unknown")

    if not allow_medium and confidence != "high":
        failures.append(f"confidence_not_high:{confidence}")

    if allow_medium and confidence not in {"high", "medium"}:
        failures.append(f"confidence_below_medium:{confidence}")

    if score < min_score:
        failures.append(f"score_below_min:{score}<{min_score}")

    if missing_steps:
        failures.append("missing_required_steps:" + ",".join(missing_steps))

    if not branches:
        warnings.append("no_branch_data_detected")

    status = "PASS" if not failures else "FAIL"

    return {
        "path": str(path),
        "name": name,
        "status": status,
        "confidence": confidence,
        "score": score,
        "missing_steps": missing_steps,
        "branch_count": len(branches),
        "failures": failures,
        "warnings": warnings,
    }


def write_md(results: list[dict[str, Any]], out_md: Path) -> None:
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")

    lines: list[str] = [
        "# Runtime Chain Regression Report",
        "",
        f"- Chains checked: `{len(results)}`",
        f"- Passed: `{passed}`",
        f"- Failed: `{failed}`",
        "",
        "## Results",
        "",
    ]

    for r in results:
        lines += [
            f"### {r['status']} — `{r['name']}`",
            "",
            f"- Path: `{r['path']}`",
            f"- Confidence: `{r['confidence']}`",
            f"- Score: `{r['score']}`",
            f"- Branch count: `{r['branch_count']}`",
            f"- Missing steps: `{', '.join(r['missing_steps']) if r['missing_steps'] else 'none'}`",
            f"- Failures: `{', '.join(r['failures']) if r['failures'] else 'none'}`",
            f"- Warnings: `{', '.join(r['warnings']) if r['warnings'] else 'none'}`",
            "",
        ]

    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regression gate for promoted runtime-chain artifacts."
    )
    parser.add_argument(
        "--chains-dir",
        type=Path,
        default=Path("docs/runtime/runtime_chains"),
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("investigations/validation/runtime_chain_regression_report.json"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("investigations/validation/runtime_chain_regression_report.md"),
    )
    parser.add_argument("--min-score", type=float, default=0.75)
    parser.add_argument("--allow-medium", action="store_true")

    args = parser.parse_args()

    args.out_json.parent.mkdir(parents=True, exist_ok=True)

    chain_files = sorted(
        path for path in args.chains_dir.glob("*.json")
        if "not_promoted" not in path.name
    )

    results = [
        assess_chain(path, args.min_score, args.allow_medium)
        for path in chain_files
    ]

    report = {
        "schema": "runtime_chain_regression_report.v1",
        "chains_dir": str(args.chains_dir),
        "chains_checked": len(results),
        "passed": sum(1 for r in results if r["status"] == "PASS"),
        "failed": sum(1 for r in results if r["status"] == "FAIL"),
        "results": results,
    }

    args.out_json.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    write_md(results, args.out_md)

    print(f"Wrote JSON: {args.out_json}")
    print(f"Wrote MD:   {args.out_md}")
    print(f"Checked: {report['chains_checked']}")
    print(f"Passed:  {report['passed']}")
    print(f"Failed:  {report['failed']}")

    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())