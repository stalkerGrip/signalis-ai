import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/items")


ITEM_PROPERTY_PATTERN = re.compile(
    r'ITEM\.([A-Za-z_][A-Za-z0-9_]*)\s*='
)

ITEM_METHOD_PATTERN = re.compile(
    r'function\s+ITEM:([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

SELF_METHOD_CALL_PATTERN = re.compile(
    r'self:([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

ITEM_FUNCTION_PATTERN = re.compile(
    r'ITEM\.functions\.([A-Za-z_][A-Za-z0-9_]*)\s*='
)

ITEM_ACTION_CALLBACK_PATTERN = re.compile(
    r'(onRun|onCanRun|onClick|onSelect)\s*=\s*function\s*\('
)

ITEM_HOOK_PATTERN = re.compile(
    r'ITEM:hook\s*\(\s*[\'"]([^\'"]+)[\'"]'
)

ITEM_DATA_ACCESS_PATTERN = re.compile(
    r'(self|item|ITEM):'
    r'(setData|getData|setQuantity|getQuantity)'
    r'\s*\((.*?)\)',
    re.DOTALL
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


def detect_item_kind(relative_path):
    lowered = relative_path.lower().replace("\\", "/")

    if "gamemode/core/meta/sh_item.lua" in lowered:
        return "framework_metaclass"

    if "/items/base/" in lowered or lowered.startswith("items/base/"):
        return "domain_item_base"

    if "/items/" in lowered or lowered.startswith("items/"):
        return "domain_item_class"

    return "unknown"


def classify_data_access(method_name):
    if method_name == "setData":
        return "item_data_write"

    if method_name == "getData":
        return "item_data_read"

    if method_name == "setQuantity":
        return "item_quantity_write"

    if method_name == "getQuantity":
        return "item_quantity_read"

    return "unknown"


def guess_callback_realm(callback_name):
    if callback_name == "onRun":
        return "server"

    if callback_name == "onCanRun":
        return "client_or_shared"

    return "unknown"


def extract_first_string_argument(args):
    match = re.search(
        r'[\'"]([^\'"]+)[\'"]',
        args
    )

    if match:
        return match.group(1)

    return None


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    item_classes = []
    item_properties = []
    item_methods = []
    item_calls = []
    item_actions = []
    item_action_callbacks = []
    item_hooks = []
    item_data_access = []

    for root in workspace["source_roots"]:
        root_path = Path(root)

        print(f"\nScanning root: {root_path}")

        if not root_path.exists():
            print("PATH DOES NOT EXIST")
            continue

        lua_files = list(root_path.rglob("*.lua"))
        print(f"Lua files found: {len(lua_files)}")

        for lua_file in lua_files:
            relative_path = str(lua_file.relative_to(root_path))
            normalized_path = relative_path.lower().replace("\\", "/")

            if (
                "/items/" not in f"/{normalized_path}"
                and "gamemode/core/meta/sh_item.lua" not in normalized_path
            ):
                continue

            try:
                content = lua_file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                realm = detect_realm(relative_path)
                framework_layer = detect_framework_layer(str(lua_file))
                item_kind = detect_item_kind(relative_path)

                property_matches = list(ITEM_PROPERTY_PATTERN.finditer(content))
                method_matches = list(ITEM_METHOD_PATTERN.finditer(content))
                self_call_matches = list(SELF_METHOD_CALL_PATTERN.finditer(content))
                action_matches = list(ITEM_FUNCTION_PATTERN.finditer(content))
                action_callback_matches = list(ITEM_ACTION_CALLBACK_PATTERN.finditer(content))
                item_hook_matches = list(ITEM_HOOK_PATTERN.finditer(content))
                data_access_matches = list(ITEM_DATA_ACCESS_PATTERN.finditer(content))

                if not (
                    property_matches
                    or method_matches
                    or self_call_matches
                    or action_matches
                    or action_callback_matches
                    or item_hook_matches
                    or data_access_matches
                ):
                    continue

                item_classes.append({
                    "type": "item_class",
                    "file": relative_path,
                    "realm": realm,
                    "framework_layer": framework_layer,
                    "item_kind": item_kind,
                    "property_count": len(property_matches),
                    "method_count": len(method_matches),
                    "self_call_count": len(self_call_matches),
                    "action_count": len(action_matches),
                    "action_callback_count": len(action_callback_matches),
                    "hook_count": len(item_hook_matches),
                    "data_access_count": len(data_access_matches)
                })

                for match in property_matches:
                    item_properties.append({
                        "type": "item_property",
                        "property_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

                for match in method_matches:
                    item_methods.append({
                        "type": "item_method",
                        "method_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

                for match in self_call_matches:
                    item_calls.append({
                        "type": "item_self_call",
                        "method_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

                for match in action_matches:
                    item_actions.append({
                        "type": "item_action",
                        "action_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": "compound",
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

                for match in action_callback_matches:
                    callback_name = match.group(1)

                    item_action_callbacks.append({
                        "type": "item_action_callback",
                        "callback_name": callback_name,
                        "inferred_realm": guess_callback_realm(callback_name),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

                for match in item_hook_matches:
                    item_hooks.append({
                        "type": "item_hook",
                        "hook_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

                for match in data_access_matches:
                    receiver = match.group(1)
                    method_name = match.group(2)
                    args = match.group(3).strip()
                    key = extract_first_string_argument(args)

                    item_data_access.append({
                        "type": classify_data_access(method_name),
                        "receiver": receiver,
                        "method_name": method_name,
                        "key": key,
                        "raw_args": args,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "item_kind": item_kind
                    })

            except Exception as e:
                print(f"Error reading {lua_file}: {e}")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    outputs = {
        "item_classes.json": item_classes,
        "item_properties.json": item_properties,
        "item_methods.json": item_methods,
        "item_calls.json": item_calls,
        "item_actions.json": item_actions,
        "item_action_callbacks.json": item_action_callbacks,
        "item_hooks.json": item_hooks,
        "item_data_access.json": item_data_access
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()