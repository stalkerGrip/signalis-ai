import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/commands")


COMMAND_START_PATTERN = re.compile(
    r'nut\.command\.(add|Add)\s*\(\s*[\'"]([^\'"]+)[\'"]\s*,\s*\{',
    re.DOTALL
)

ADMIN_ONLY_PATTERN = re.compile(
    r'adminOnly\s*=\s*(true|false)'
)

SYNTAX_PATTERN = re.compile(
    r'syntax\s*=\s*[\'"]([^\'"]+)[\'"]'
)

ONRUN_PATTERN = re.compile(
    r'onRun\s*=\s*function\s*\((.*?)\)',
    re.DOTALL
)

ONCANRUN_PATTERN = re.compile(
    r'onCanRun\s*=\s*function\s*\((.*?)\)',
    re.DOTALL
)

ENTITY_METHOD_CALL_PATTERN = re.compile(
    r'([A-Za-z_][A-Za-z0-9_\.]*):([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

ITEM_ACTION_CALL_PATTERN = re.compile(
    r'\.functions\.([A-Za-z_][A-Za-z0-9_]*)\.onRun\s*\('
)

ITEM_HOOK_CALL_PATTERN = re.compile(
    r'\.hooks\s*\[\s*[\'"]([^\'"]+)[\'"]\s*\]\s*\('
)

NUT_CALL_PATTERN = re.compile(
    r'nut\.([A-Za-z_][A-Za-z0-9_\.]*)(?::|\.)([A-Za-z_][A-Za-z0-9_]*)\s*\('
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


def line_number_for(content, position):
    return content.count("\n", 0, position) + 1


def find_matching_command_end(content, start_index):
    depth = 0
    i = start_index

    while i < len(content):
        char = content[i]

        if char == "{":
            depth += 1

        elif char == "}":
            depth -= 1

            if depth == 0:
                closing_paren = content.find(")", i)

                if closing_paren != -1:
                    return closing_paren + 1

                return i + 1

        i += 1

    return len(content)


def extract_command_block(content, match):
    block_start = match.end() - 1
    block_end = find_matching_command_end(content, block_start)

    return content[block_start:block_end]


def detect_command_effects(block):
    return {
        "uses_trace": "GetEyeTrace" in block or "GetEyeTraceNoCursor" in block,
        "uses_inventory": "getInv()" in block or "getItems()" in block or "getItemsOfType" in block,
        "uses_find_player": "nut.command.findPlayer" in block,
        "uses_position_mutation": ":SetPos(" in block,
        "uses_entity_class_check": ":GetClass()" in block,
        "uses_print_table": "PrintTable(" in block,
        "calls_item_action": ".functions." in block and ".onRun(" in block,
        "calls_item_hook": ".hooks[" in block,
        "calls_notify": ":notify(" in block or "notifyLocalized" in block
    }


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    commands = []
    command_callbacks = []
    command_effects = []
    command_calls = []

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

                command_matches = list(COMMAND_START_PATTERN.finditer(content))

                for match in command_matches:
                    registration_method = match.group(1)
                    command_name = match.group(2)
                    block = extract_command_block(content, match)
                    start_line = line_number_for(content, match.start())

                    admin_match = ADMIN_ONLY_PATTERN.search(block)
                    syntax_match = SYNTAX_PATTERN.search(block)
                    onrun_match = ONRUN_PATTERN.search(block)
                    oncanrun_match = ONCANRUN_PATTERN.search(block)

                    admin_only = None
                    if admin_match:
                        admin_only = admin_match.group(1) == "true"

                    syntax = syntax_match.group(1) if syntax_match else None
                    effects = detect_command_effects(block)

                    commands.append({
                        "type": "nut_command",
                        "command_name": command_name,
                        "registration_method": registration_method,
                        "admin_only": admin_only,
                        "syntax": syntax,
                        "has_onRun": onrun_match is not None,
                        "has_onCanRun": oncanrun_match is not None,
                        "file": relative_path,
                        "line": start_line,
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                    command_effects.append({
                        "type": "command_effects",
                        "command_name": command_name,
                        "effects": effects,
                        "file": relative_path,
                        "line": start_line,
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                    if onrun_match:
                        command_callbacks.append({
                            "type": "command_callback",
                            "command_name": command_name,
                            "callback_name": "onRun",
                            "args": onrun_match.group(1).strip(),
                            "inferred_realm": "server",
                            "file": relative_path,
                            "line": start_line,
                            "realm": realm,
                            "framework_layer": framework_layer
                        })

                    if oncanrun_match:
                        command_callbacks.append({
                            "type": "command_callback",
                            "command_name": command_name,
                            "callback_name": "onCanRun",
                            "args": oncanrun_match.group(1).strip(),
                            "inferred_realm": "server_or_shared",
                            "file": relative_path,
                            "line": start_line,
                            "realm": realm,
                            "framework_layer": framework_layer
                        })

                    for call_match in ENTITY_METHOD_CALL_PATTERN.finditer(block):
                        command_calls.append({
                            "type": "command_method_call",
                            "command_name": command_name,
                            "receiver": call_match.group(1),
                            "method_name": call_match.group(2),
                            "file": relative_path,
                            "line": start_line + line_number_for(block, call_match.start()) - 1,
                            "realm": realm,
                            "framework_layer": framework_layer
                        })

                    for action_match in ITEM_ACTION_CALL_PATTERN.finditer(block):
                        command_calls.append({
                            "type": "command_item_action_call",
                            "command_name": command_name,
                            "action_name": action_match.group(1),
                            "file": relative_path,
                            "line": start_line + line_number_for(block, action_match.start()) - 1,
                            "realm": realm,
                            "framework_layer": framework_layer
                        })

                    for hook_match in ITEM_HOOK_CALL_PATTERN.finditer(block):
                        command_calls.append({
                            "type": "command_item_hook_call",
                            "command_name": command_name,
                            "hook_name": hook_match.group(1),
                            "file": relative_path,
                            "line": start_line + line_number_for(block, hook_match.start()) - 1,
                            "realm": realm,
                            "framework_layer": framework_layer
                        })

                    for nut_match in NUT_CALL_PATTERN.finditer(block):
                        command_calls.append({
                            "type": "command_nut_call",
                            "command_name": command_name,
                            "namespace": nut_match.group(1),
                            "method_name": nut_match.group(2),
                            "full_call": f"nut.{nut_match.group(1)}.{nut_match.group(2)}",
                            "file": relative_path,
                            "line": start_line + line_number_for(block, nut_match.start()) - 1,
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
        "commands.json": commands,
        "command_callbacks.json": command_callbacks,
        "command_effects.json": command_effects,
        "command_calls.json": command_calls
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()