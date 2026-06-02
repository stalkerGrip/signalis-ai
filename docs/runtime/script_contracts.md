# SIGNALIS AI — Script CLI Contracts

Generated from:

```text
python -m <module> --help
```

Purpose:

- prevent guessed CLI usage
- preserve script interfaces across chats
- expose scripts without usable command-line help

- Scripts checked: `3`

## extraction

### `scripts.extraction.discover_lua_sources`

- Path: `scripts/extraction/discover_lua_sources.py`
- Help status: `OK`

```text
usage: discover_lua_sources.py [-h] --workspace WORKSPACE
                               [--out-json OUT_JSON] [--out-md OUT_MD]

Discover Lua source files from config/workspace.yaml and build
source_file_manifest artifacts.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root containing config/workspace.yaml.
  --out-json OUT_JSON   Output JSON path. Defaults to
                        manifests/extraction/source_file_manifest.json.
  --out-md OUT_MD       Output Markdown path. Defaults to
                        manifests/extraction/source_file_manifest.md.
```

## tools

### `scripts.tools.build_pipeline_contract_registry`

- Path: `scripts/tools/build_pipeline_contract_registry.py`
- Help status: `OK`

```text
usage: build_pipeline_contract_registry.py [-h] --workspace WORKSPACE
                                           [--out-json OUT_JSON]
                                           [--out-md OUT_MD]
                                           [--cli-out-json CLI_OUT_JSON]
                                           [--cli-out-md CLI_OUT_MD]
                                           [--script-root SCRIPT_ROOT]
                                           [--artifact-root ARTIFACT_ROOT]
                                           [--include-missing-artifacts]
                                           [--skip-cli-help]
                                           [--help-timeout HELP_TIMEOUT]
                                           [--fail-on-error]

Build generic SIGNALIS AI pipeline artifact + script CLI contract registries.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
                        Workspace root, e.g. E:/signalis_ai
  --out-json OUT_JSON
  --out-md OUT_MD
  --cli-out-json CLI_OUT_JSON
  --cli-out-md CLI_OUT_MD
  --script-root SCRIPT_ROOT
                        Optional scan root for Python scripts. Repeatable.
                        Defaults to the workspace root.
  --artifact-root ARTIFACT_ROOT
                        Optional scan root for artifacts. Repeatable. Defaults
                        to the workspace root.
  --include-missing-artifacts
                        Also include JSON/JSONL/MD files without explicit
                        artifact metadata.
  --skip-cli-help       Do not run python -m <module> --help.
  --help-timeout HELP_TIMEOUT
  --fail-on-error
```

### `scripts.tools.generate_project_structure`

- Path: `scripts/tools/generate_project_structure.py`
- Help status: `OK`

```text
usage: generate_project_structure.py [-h] --workspace WORKSPACE
                                     [--output OUTPUT] [--max-depth MAX_DEPTH]

Generate SIGNALIS AI project structure manifest.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --output OUTPUT
  --max-depth MAX_DEPTH
```

