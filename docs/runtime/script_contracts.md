# SIGNALIS AI — Script Contracts

Generated from:

```text
python -m <module> --help
```

Purpose:

- prevent guessed CLI usage
- preserve script interfaces across chats
- document inputs/outputs for orchestration
- expose older script usability issues

Rule:

Before wrapping or chaining a script, check this file or run the script with `--help`.

- Scripts checked: `8`

## scripts/diagnostics

### `scripts.diagnostics.test_embeddings`

- Path: `scripts/diagnostics/test_embeddings.py`
- Help status: `OK`

```text
Loading embedding model...
Generating embedding...
Vector size: 384
Success.
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.

Loading weights:   0%|          | 0/199 [00:00<?, ?it/s]
Loading weights: 100%|##########| 199/199 [00:00<00:00, 8649.04it/s]
```

## scripts/investigation

### `scripts.investigation.build_orchestration_entrypoint`

- Path: `scripts/investigation/build_orchestration_entrypoint.py`
- Help status: `OK`

```text
usage: build_orchestration_entrypoint.py [-h] --workspace WORKSPACE --request
                                         REQUEST [--input-kind INPUT_KIND]
                                         [--user-constraint USER_CONSTRAINT]
                                         [--source-preference SOURCE_PREFERENCE]
                                         [--input-artifact INPUT_ARTIFACT]
                                         [--parent-artifact-id PARENT_ARTIFACT_ID]
                                         [--regenerates REGENERATES]
                                         [--out OUT]

Build a normalization-only orchestration_request artifact.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --request REQUEST
  --input-kind INPUT_KIND
  --user-constraint USER_CONSTRAINT
  --source-preference SOURCE_PREFERENCE
  --input-artifact INPUT_ARTIFACT
  --parent-artifact-id PARENT_ARTIFACT_ID
  --regenerates REGENERATES
  --out OUT
```

### `scripts.investigation.build_orchestration_index`

- Path: `scripts/investigation/build_orchestration_index.py`
- Help status: `OK`

```text
usage: build_orchestration_index.py [-h] [--workspace WORKSPACE]
                                    [--evidence-artifact EVIDENCE_ARTIFACT]
                                    [--out-json OUT_JSON] [--out-md OUT_MD]

Build orchestration_index from explicit upstream scope-signal artifacts. No
request-text routing or hidden keyword maps are used.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --evidence-artifact EVIDENCE_ARTIFACT
                        JSON artifact or directory containing JSON artifacts
                        with explicit scope signals.
  --out-json OUT_JSON
  --out-md OUT_MD
```

### `scripts.investigation.build_orchestration_scope`

- Path: `scripts/investigation/build_orchestration_scope.py`
- Help status: `OK`

```text
usage: build_orchestration_scope.py [-h] --orchestration-request
                                    ORCHESTRATION_REQUEST
                                    [--orchestration-index ORCHESTRATION_INDEX]
                                    [--out-dir OUT_DIR] [--out-json OUT_JSON]
                                    [--out-md OUT_MD]

Build canonical orchestration_scope from orchestration_request. Optional scope
evidence must come from a contract-valid orchestration_index.

options:
  -h, --help            show this help message and exit
  --orchestration-request ORCHESTRATION_REQUEST
                        Path to an orchestration_request JSON artifact.
  --orchestration-index ORCHESTRATION_INDEX
                        Optional contract-valid orchestration_index JSON
                        artifact. Must use artifact_family=orchestration_index
                        and required_capabilities including scope_entries.
  --out-dir OUT_DIR     Output directory. Defaults to
                        investigations/orchestration.
  --out-json OUT_JSON   Explicit JSON output path.
  --out-md OUT_MD       Explicit Markdown output path.
```

## scripts/tools

### `scripts.tools.build_pipeline_contract_registry`

- Path: `scripts/tools/build_pipeline_contract_registry.py`
- Help status: `OK`

```text
usage: build_pipeline_contract_registry.py [-h] [--workspace WORKSPACE]
                                           [--existing-contract EXISTING_CONTRACT]
                                           [--out-json OUT_JSON]
                                           [--out-md OUT_MD]
                                           [--script-dir SCRIPT_DIR]
                                           [--artifact-dir ARTIFACT_DIR]
                                           [--no-merge-existing]

Build fire-and-forget SIGNALIS pipeline script/artifact contract registry.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --existing-contract EXISTING_CONTRACT
  --out-json OUT_JSON
  --out-md OUT_MD
  --script-dir SCRIPT_DIR
                        Script directory to scan, relative to workspace unless
                        absolute. Can be repeated. Defaults to canonical
                        script roots.
  --artifact-dir ARTIFACT_DIR
                        Artifact directory to scan, relative to workspace
                        unless absolute. Can be repeated. Defaults to
                        canonical artifact roots.
  --no-merge-existing   Do not preserve manual curations from existing
                        contract.
```

### `scripts.tools.check_pipeline_contracts`

- Path: `scripts/tools/check_pipeline_contracts.py`
- Help status: `OK`

```text
usage: check_pipeline_contracts.py [-h] [--workspace WORKSPACE]
                                   [--contract CONTRACT] [--out-json OUT_JSON]
                                   [--out-md OUT_MD] [--script-dir SCRIPT_DIR]
                                   [--artifact-dir ARTIFACT_DIR]
                                   [--init-contract] [--fail-on-error]

Check SIGNALIS AI script/artifact contracts against actual repository state.

options:
  -h, --help            show this help message and exit
  --workspace WORKSPACE
  --contract CONTRACT
  --out-json OUT_JSON
  --out-md OUT_MD
  --script-dir SCRIPT_DIR
                        Additional or replacement script directory to scan.
                        Repeatable. Defaults to canonical script dirs.
  --artifact-dir ARTIFACT_DIR
                        Additional or replacement artifact directory to scan.
                        Repeatable. Defaults to canonical artifact dirs.
  --init-contract       Create a starter contract if missing.
  --fail-on-error       Exit non-zero when ERROR findings exist.
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

### `scripts.tools.generate_script_contracts`

- Path: `scripts/tools/generate_script_contracts.py`
- Help status: `OK`

```text
usage: generate_script_contracts.py [-h] [--root ROOT]
                                    [--scripts-dir SCRIPTS_DIR]
                                    [--out-md OUT_MD] [--out-json OUT_JSON]

Generate script CLI contract documentation from python -m <module> --help.

options:
  -h, --help            show this help message and exit
  --root ROOT
  --scripts-dir SCRIPTS_DIR
  --out-md OUT_MD
  --out-json OUT_JSON
```
