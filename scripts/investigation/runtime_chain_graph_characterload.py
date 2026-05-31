#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


WORKSPACE = Path("E:/signalis_ai")

OUT_JSON = Path("investigations/validation/runtime_chain_graph_characterload_v1.json")
OUT_MD = Path("investigations/validation/runtime_chain_graph_characterload_v1.md")

SOURCE_QUERY = "CharacterLoaded PlayerLoadedChar PrePlayerLoadedChar"
TARGET_QUERY = "inventoryOpen inventorySetPanelStatus client inventory UI"


def main() -> int:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "scripts.investigation.runtime_chain_graph",
        "--workspace",
        str(WORKSPACE),
        "--source-query",
        SOURCE_QUERY,
        "--target-query",
        TARGET_QUERY,
        "--max-paths",
        "50",
        "--cutoff",
        "12",
        "--out-json",
        str(OUT_JSON),
        "--out-md",
        str(OUT_MD),
    ]

    print("[RUN]", " ".join(cmd))
    result = subprocess.run(cmd, text=True)

    if result.returncode != 0:
        return result.returncode

    print("\n[DONE] CharacterLoaded graph audit written:")
    print(f"JSON: {OUT_JSON}")
    print(f"MD:   {OUT_MD}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())