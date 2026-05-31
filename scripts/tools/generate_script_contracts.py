#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {
    ".venv",
    "__pycache__",
    ".git",
    "temp",
    "logs",
}


def module_name(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def run_help(module: str) -> tuple[bool, str]:
    cmd = [sys.executable, "-m", module, "--help"]

    try:
        result = subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT while running --help"

    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate script CLI contract documentation from python -m <module> --help."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--scripts-dir",
        type=Path,
        default=Path("scripts"),
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=Path("docs/runtime/script_contracts.md"),
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=Path("docs/runtime/script_contracts.json"),
    )

    args = parser.parse_args()

    script_root = args.root / args.scripts_dir
    py_files = sorted(
        path.relative_to(args.root)
        for path in script_root.rglob("*.py")
        if not should_skip(path)
        and path.name != "__init__.py"
    )

    contracts = []

    for path in py_files:
        module = module_name(path)
        ok, help_text = run_help(module)

        contracts.append({
            "path": str(path).replace("\\", "/"),
            "module": module,
            "help_ok": ok,
            "help": help_text,
        })

    args.out_md.parent.mkdir(parents=True, exist_ok=True)

    args.out_json.write_text(
        json.dumps(
            {
                "schema": "signalis_script_contracts.v1",
                "scripts_checked": len(contracts),
                "contracts": contracts,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    lines = [
        "# SIGNALIS AI — Script Contracts",
        "",
        "Generated from:",
        "",
        "```text",
        "python -m <module> --help",
        "```",
        "",
        "Purpose:",
        "",
        "- prevent guessed CLI usage",
        "- preserve script interfaces across chats",
        "- document inputs/outputs for orchestration",
        "- expose older script usability issues",
        "",
        "Rule:",
        "",
        "Before wrapping or chaining a script, check this file or run the script with `--help`.",
        "",
        f"- Scripts checked: `{len(contracts)}`",
        "",
    ]

    by_group: dict[str, list[dict]] = {}

    for contract in contracts:
        group = contract["path"].split("/")[1] if "/" in contract["path"] else "root"
        by_group.setdefault(group, []).append(contract)

    for group, items in sorted(by_group.items()):
        lines += [
            f"## scripts/{group}",
            "",
        ]

        for contract in items:
            status = "OK" if contract["help_ok"] else "NO_HELP_OR_ERROR"

            lines += [
                f"### `{contract['module']}`",
                "",
                f"- Path: `{contract['path']}`",
                f"- Help status: `{status}`",
                "",
                "```text",
                contract["help"] or "(no help output)",
                "```",
                "",
            ]

    args.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote MD:   {args.out_md}")
    print(f"Wrote JSON: {args.out_json}")
    print(f"Scripts checked: {len(contracts)}")

    failed = sum(1 for c in contracts if not c["help_ok"])
    print(f"Scripts without usable --help: {failed}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())