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
OUTPUT_DIR = Path("manifests/registries")


NUT_TABLE_ASSIGN_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)\s*=\s*nut\.\1\s*\|\|\s*\{'
)

NUT_DIRECT_TABLE_ASSIGN_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)\s*=\s*\{'
)

NUT_STRING_CONST_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)\.([A-Za-z_][A-Za-z0-9_]*)\s*=\s*[\'"]([^\'"]+)[\'"]'
)

NUT_REF_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)'
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


def classify_registry(namespace):
    if namespace.startswith("diseases.stringConsts"):
        return "symbolic_constant_registry"

    if namespace.startswith("diseases.stringConstsLocalization"):
        return "localization_registry"

    if namespace.startswith("item.list"):
        return "item_class_registry"

    if namespace.startswith("item.instances"):
        return "item_instance_registry"

    return "generic_nut_registry"


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    nut_table_assignments = []
    nut_string_constants = []
    nut_registry_refs = []

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

                table_assign_matches = list(NUT_TABLE_ASSIGN_PATTERN.finditer(content))
                direct_table_assign_matches = list(NUT_DIRECT_TABLE_ASSIGN_PATTERN.finditer(content))
                string_const_matches = list(NUT_STRING_CONST_PATTERN.finditer(content))
                nut_ref_matches = list(NUT_REF_PATTERN.finditer(content))

                for match in table_assign_matches:
                    namespace = match.group(1)

                    if not is_important_nut_namespace(namespace):
                        continue

                    nut_table_assignments.append({
                        "type": "nut_table_assignment",
                        "namespace": namespace,
                        "full_name": f"nut.{namespace}",
                        "assignment_style": "preserve_or_create",
                        "registry_class": classify_registry(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in direct_table_assign_matches:
                    namespace = match.group(1)

                    if not is_important_nut_namespace(namespace):
                        continue

                    nut_table_assignments.append({
                        "type": "nut_table_assignment",
                        "namespace": namespace,
                        "full_name": f"nut.{namespace}",
                        "assignment_style": "direct_table",
                        "registry_class": classify_registry(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in string_const_matches:
                    namespace = match.group(1)
                    key = match.group(2)
                    value = match.group(3)

                    if not is_important_nut_namespace(namespace):
                        continue

                    nut_string_constants.append({
                        "type": "nut_string_constant",
                        "namespace": namespace,
                        "key": key,
                        "value": value,
                        "symbol": f"nut.{namespace}.{key}",
                        "registry_class": classify_registry(namespace),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in nut_ref_matches:
                    namespace = match.group(1)

                    if not is_important_nut_namespace(namespace):
                        continue

                    nut_registry_refs.append({
                        "type": "nut_registry_ref",
                        "namespace": namespace,
                        "full_name": f"nut.{namespace}",
                        "registry_class": classify_registry(namespace),
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
        "nut_table_assignments.json": nut_table_assignments,
        "nut_string_constants.json": nut_string_constants,
        "nut_registry_refs.json": nut_registry_refs
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()