import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/plugins")


PLUGIN_PROPERTY_PATTERN = re.compile(
    r'PLUGIN\.([A-Za-z_][A-Za-z0-9_]*)\s*='
)

PLUGIN_METHOD_PATTERN = re.compile(
    r'function\s+PLUGIN:([A-Za-z_][A-Za-z0-9_]*)\s*\((.*?)\)',
    re.DOTALL
)

HOOK_RUN_LITERAL_PATTERN = re.compile(
    r'hook\.(Run|Call)\s*\(\s*[\'"]([^\'"]+)[\'"]'
)

HOOK_RUN_SYMBOL_PATTERN = re.compile(
    r'hook\.(Run|Call)\s*\(\s*([A-Za-z_][A-Za-z0-9_\.]*)'
)

PLUGIN_REF_PATTERN = re.compile(
    r'nut\.plugin\.([A-Za-z_][A-Za-z0-9_\.]*)'
)


def detect_realm(path_str):
    lowered = path_str.lower()

    if "\\cl_" in lowered or "/cl_" in lowered:
        return "client"

    if "\\sv_" in lowered or "/sv_" in lowered:
        return "server"

    if "\\sh_" in lowered or "/sh_" in lowered:
        return "shared"

    if lowered.endswith("cl_init.lua"):
        return "client"

    if lowered.endswith("init.lua"):
        return "server"

    if lowered.endswith("shared.lua"):
        return "shared"

    return "unknown"


def detect_framework_layer(path_str):
    lowered = path_str.lower()

    if "nutscript" in lowered:
        return "framework"

    if "signalis" in lowered:
        return "domain"

    return "unknown"


def detect_plugin_context(relative_path):
    lowered = relative_path.lower().replace("\\", "/")

    if "/plugins/" in f"/{lowered}":
        return "plugin_file"

    return "unknown_file"


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    plugin_properties = []
    plugin_methods = []
    hook_runs = []
    plugin_refs = []

    for root in workspace["source_roots"]:
        root_path = Path(root)

        print(f"\nScanning root: {root_path}")

        if not root_path.exists():
            print("PATH DOES NOT EXIST")
            continue

        lua_files = list(root_path.rglob("*.lua"))
        print(f"Lua files found: {len(lua_files)}")

        for lua_file in lua_files:
            try:
                content = lua_file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                relative_path = str(lua_file.relative_to(root_path))
                realm = detect_realm(relative_path)
                framework_layer = detect_framework_layer(str(lua_file))
                plugin_context = detect_plugin_context(relative_path)

                property_matches = list(PLUGIN_PROPERTY_PATTERN.finditer(content))
                method_matches = list(PLUGIN_METHOD_PATTERN.finditer(content))
                hook_literal_matches = list(HOOK_RUN_LITERAL_PATTERN.finditer(content))
                hook_symbol_matches = list(HOOK_RUN_SYMBOL_PATTERN.finditer(content))
                plugin_ref_matches = list(PLUGIN_REF_PATTERN.finditer(content))

                if not (
                    property_matches
                    or method_matches
                    or hook_literal_matches
                    or hook_symbol_matches
                    or plugin_ref_matches
                ):
                    continue

                for match in property_matches:
                    plugin_properties.append({
                        "type": "plugin_property",
                        "property_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "plugin_context": plugin_context
                    })

                for match in method_matches:
                    plugin_methods.append({
                        "type": "plugin_method",
                        "method_name": match.group(1),
                        "args": match.group(2).strip(),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "plugin_context": plugin_context
                    })

                for match in hook_literal_matches:
                    hook_runs.append({
                        "type": "hook_run",
                        "call_type": match.group(1),
                        "hook_name": match.group(2),
                        "symbol": None,
                        "resolution": "literal",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "plugin_context": plugin_context
                    })

                for match in hook_symbol_matches:
                    symbol = match.group(2)

                    if symbol.startswith(("'", '"')):
                        continue

                    hook_runs.append({
                        "type": "hook_run",
                        "call_type": match.group(1),
                        "hook_name": None,
                        "symbol": symbol,
                        "resolution": "unresolved_symbol",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "plugin_context": plugin_context
                    })

                for match in plugin_ref_matches:
                    plugin_refs.append({
                        "type": "plugin_ref",
                        "reference": f"nut.plugin.{match.group(1)}",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "plugin_context": plugin_context
                    })

            except Exception as e:
                print(f"Error reading {lua_file}: {e}")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    outputs = {
        "plugin_properties.json": plugin_properties,
        "plugin_methods.json": plugin_methods,
        "hook_runs.json": hook_runs,
        "plugin_refs.json": plugin_refs
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()