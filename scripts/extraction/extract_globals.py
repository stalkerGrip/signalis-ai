import re
import json
import yaml

from pathlib import Path

IMPORTANT_NUT_ROOTS = {
    "diseases",
    "item",
    "char",
    "inventory",
    "plugin",
    "traits",
    "biorez",
    "attrib",
    "faction",
    "class",
    "command",
    "db"
}


def is_important_nut_namespace(namespace):
    root = namespace.split(".")[0]
    return root in IMPORTANT_NUT_ROOTS

CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/globals")


NUT_METHOD_CALL_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*):([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

NUT_FUNCTION_CALL_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)\.([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

NUT_WRITE_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)\s*='
)

# Only important registry-like reads, not every nut.*
NUT_IMPORTANT_REF_PATTERN = re.compile(
    r'nut\.('
    r'item\.list|'
    r'item\.instances|'
    r'char\.loaded|'
    r'diseases\.[A-Za-z_][A-Za-z0-9_\.]*|'
    r'traits\.[A-Za-z_][A-Za-z0-9_\.]*|'
    r'biorez\.[A-Za-z_][A-Za-z0-9_\.]*|'
    r'inventory\.[A-Za-z_][A-Za-z0-9_\.]*|'
    r'plugin\.list|'
    r'plugin\.stored'
    r')'
)

IGNORED_READ_ROOTS = {
    "util",
    "log",
    "lang",
    "config",
    "currency",
    "menu",
    "option"
}


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


def classify_nut_namespace(namespace):
    root = namespace.split(".")[0]

    if namespace in {"item.list", "item.instances"}:
        return "item_runtime_registry"

    if namespace == "char.loaded":
        return "character_runtime_registry"

    if root == "diseases":
        return "disease_subsystem"

    if root == "traits":
        return "traits_subsystem"

    if root == "biorez":
        return "biorez_subsystem"

    if root == "inventory":
        return "inventory_subsystem"

    if root == "plugin":
        return "plugin_registry"

    known_nutscript_roots = {
        "item",
        "char",
        "command",
        "plugin",
        "db",
        "class",
        "attrib",
        "faction",
        "flag",
        "meta"
    }

    if root in known_nutscript_roots:
        return "nutscript_core"

    if root in IGNORED_READ_ROOTS:
        return "utility_or_framework_noise"

    return "custom_or_domain"


def is_noisy_function_call(namespace):
    root = namespace.split(".")[0]
    return root in IGNORED_READ_ROOTS


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    nut_method_calls = []
    nut_function_calls = []
    nut_writes = []
    nut_important_refs = []

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

                method_matches = list(NUT_METHOD_CALL_PATTERN.finditer(content))
                function_matches = list(NUT_FUNCTION_CALL_PATTERN.finditer(content))
                write_matches = list(NUT_WRITE_PATTERN.finditer(content))
                important_ref_matches = list(NUT_IMPORTANT_REF_PATTERN.finditer(content))

                for match in method_matches:
                    namespace = match.group(1)
                    method_name = match.group(2)

                    if not is_important_nut_namespace(namespace):
                        continue

                    nut_method_calls.append({
                        "type": "nut_method_call",
                        "namespace": namespace,
                        "method_name": method_name,
                        "full_call": f"nut.{namespace}:{method_name}",
                        "namespace_class": classify_nut_namespace(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in function_matches:
                    namespace = match.group(1)
                    function_name = match.group(2)

                    if not is_important_nut_namespace(namespace):
                        continue

                    if is_noisy_function_call(namespace):
                        continue

                    nut_function_calls.append({
                        "type": "nut_function_call",
                        "namespace": namespace,
                        "function_name": function_name,
                        "full_call": f"nut.{namespace}.{function_name}",
                        "namespace_class": classify_nut_namespace(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in write_matches:
                    namespace = match.group(1)

                    if not is_important_nut_namespace(namespace):
                        continue

                    nut_writes.append({
                        "type": "nut_write",
                        "namespace": namespace,
                        "full_name": f"nut.{namespace}",
                        "namespace_class": classify_nut_namespace(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                seen_refs = set()

                for match in important_ref_matches:
                    namespace = match.group(1)

                    if not is_important_nut_namespace(namespace):
                        continue

                    key = (
                        namespace,
                        relative_path,
                        line_number_for(content, match)
                    )

                    if key in seen_refs:
                        continue

                    seen_refs.add(key)

                    nut_important_refs.append({
                        "type": "nut_important_ref",
                        "namespace": namespace,
                        "full_name": f"nut.{namespace}",
                        "namespace_class": classify_nut_namespace(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

            except Exception as e:
                print(f"Error reading {lua_file}: {e}")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    outputs = {
        "nut_method_calls.json": nut_method_calls,
        "nut_function_calls.json": nut_function_calls,
        "nut_writes.json": nut_writes,
        "nut_important_refs.json": nut_important_refs
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()