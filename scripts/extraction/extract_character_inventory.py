import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/character_inventory")


CHARACTER_CALL_PATTERN = re.compile(
    r'([A-Za-z_][A-Za-z0-9_]*(?::getChar\(\))?):'
    r'(getChar|getID|getName|getData|setData|getAttrib|updateAttrib|getInv)\s*\((.*?)\)',
    re.DOTALL
)

INVENTORY_CALL_PATTERN = re.compile(
    r'([A-Za-z_][A-Za-z0-9_]*(?::getChar\(\))?(?::getInv\(\))?):'
    r'(getInv|getItems|getItemsOfType|add|remove|transfer|hasItem|getFirstItemOfType)\s*\((.*?)\)',
    re.DOTALL
)

GETCHAR_GETINV_CHAIN_PATTERN = re.compile(
    r'([A-Za-z_][A-Za-z0-9_]*):getChar\(\):getInv\(\)'
)

GET_ITEMS_OF_TYPE_PATTERN = re.compile(
    r':getItemsOfType\s*\(\s*[\'"]([^\'"]+)[\'"]'
)

CHAR_LOOP_PATTERN = re.compile(
    r'for\s+[^,]+,\s*([A-Za-z_][A-Za-z0-9_]*)\s+in\s+pairs\s*\(\s*nut\.char\.loaded\s*\)'
)

ITEM_LOOP_PATTERN = re.compile(
    r'for\s+[^,]+,\s*([A-Za-z_][A-Za-z0-9_]*)\s+in\s+pairs\s*\(.*?:getItemsOfType\s*\(',
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


def detect_file_context(relative_path):
    lowered = relative_path.lower().replace("\\", "/")

    if "/items/" in f"/{lowered}":
        return "item_file"
    if "/entities/" in f"/{lowered}":
        return "entity_file"
    if "/plugins/" in f"/{lowered}":
        return "plugin_file"
    if "commands" in lowered or "command" in lowered:
        return "command_file"

    return "unknown_file"


def extract_first_string_argument(args):
    match = re.search(r'[\'"]([^\'"]+)[\'"]', args)

    if match:
        return match.group(1)

    return None


def infer_character_receiver(receiver, file_context, char_vars):
    if receiver.endswith(":getChar()"):
        return "character", "high", "receiver_chain_getChar"

    if receiver in char_vars:
        return "character", "high", "loop_over_nut.char.loaded"

    if receiver in {"char", "character"}:
        return "character", "medium", "receiver_name_char"

    if receiver in {"client", "player", "ply", "target"}:
        return "player", "medium", "receiver_name_player"

    if receiver == "self":
        if file_context == "entity_file":
            return "entity_or_player", "low", "ambiguous_self_entity_file"

        return "unknown", "low", "ambiguous_self"

    return "unknown", "low", "unrecognized_receiver"


def infer_inventory_receiver(receiver, file_context, char_vars):
    if receiver.endswith(":getChar():getInv()"):
        return "inventory", "high", "receiver_chain_getChar_getInv"

    if receiver.endswith(":getChar()"):
        return "character", "high", "receiver_chain_getChar"

    if receiver in {"inv", "inventory"}:
        return "inventory", "medium", "receiver_name_inventory"

    if receiver in char_vars:
        return "character_inventory", "high", "loop_over_nut.char.loaded"

    if receiver in {"char", "character"}:
        return "character_inventory", "medium", "receiver_name_char"

    if receiver in {"client", "player", "ply", "target"}:
        return "player_inventory_or_character_holder", "low", "player_receiver_inventory_call"

    if receiver == "self":
        if file_context == "item_file":
            return "item_or_inventory_context", "low", "ambiguous_self_item_file"

        if file_context == "entity_file":
            return "entity_or_player_inventory_context", "low", "ambiguous_self_entity_file"

        return "unknown", "low", "ambiguous_self"

    return "unknown", "low", "unrecognized_receiver"


def classify_character_call(method_name):
    if method_name in {"getData", "setData"}:
        return "character_data_access"

    if method_name in {"getAttrib", "updateAttrib"}:
        return "character_attribute_access"

    if method_name == "getInv":
        return "character_inventory_access"

    if method_name == "getChar":
        return "player_character_access"

    return "character_call"


def classify_inventory_call(method_name):
    if method_name in {"getItems", "getItemsOfType", "getFirstItemOfType", "hasItem"}:
        return "inventory_query"

    if method_name in {"add", "remove", "transfer"}:
        return "inventory_mutation"

    if method_name == "getInv":
        return "inventory_access"

    return "inventory_call"


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    character_calls = []
    inventory_calls = []
    character_inventory_chains = []
    inventory_item_queries = []

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
                file_context = detect_file_context(relative_path)

                char_vars = set()
                item_vars = set()

                for match in CHAR_LOOP_PATTERN.finditer(content):
                    char_vars.add(match.group(1))

                for match in ITEM_LOOP_PATTERN.finditer(content):
                    item_vars.add(match.group(1))

                character_matches = list(CHARACTER_CALL_PATTERN.finditer(content))
                inventory_matches = list(INVENTORY_CALL_PATTERN.finditer(content))
                chain_matches = list(GETCHAR_GETINV_CHAIN_PATTERN.finditer(content))
                item_query_matches = list(GET_ITEMS_OF_TYPE_PATTERN.finditer(content))

                for match in character_matches:
                    receiver = match.group(1)
                    method_name = match.group(2)
                    args = match.group(3).strip()
                    key = extract_first_string_argument(args)

                    state_domain, confidence, evidence = infer_character_receiver(
                        receiver,
                        file_context,
                        char_vars
                    )

                    character_calls.append({
                        "type": classify_character_call(method_name),
                        "receiver": receiver,
                        "method_name": method_name,
                        "key": key,
                        "raw_args": args,
                        "state_domain": state_domain,
                        "confidence": confidence,
                        "evidence": evidence,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "file_context": file_context
                    })

                for match in inventory_matches:
                    receiver = match.group(1)
                    method_name = match.group(2)
                    args = match.group(3).strip()
                    item_type = extract_first_string_argument(args)

                    state_domain, confidence, evidence = infer_inventory_receiver(
                        receiver,
                        file_context,
                        char_vars
                    )

                    inventory_calls.append({
                        "type": classify_inventory_call(method_name),
                        "receiver": receiver,
                        "method_name": method_name,
                        "item_type": item_type,
                        "raw_args": args,
                        "state_domain": state_domain,
                        "confidence": confidence,
                        "evidence": evidence,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "file_context": file_context
                    })

                for match in chain_matches:
                    receiver = match.group(1)

                    character_inventory_chains.append({
                        "type": "character_inventory_chain",
                        "receiver": receiver,
                        "chain": f"{receiver}:getChar():getInv()",
                        "state_domain": "inventory",
                        "confidence": "high",
                        "evidence": "explicit_getChar_getInv_chain",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "file_context": file_context
                    })

                for match in item_query_matches:
                    inventory_item_queries.append({
                        "type": "inventory_item_type_query",
                        "item_type": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "file_context": file_context
                    })

            except Exception as e:
                print(f"Error reading {lua_file}: {e}")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    outputs = {
        "character_calls.json": character_calls,
        "inventory_calls.json": inventory_calls,
        "character_inventory_chains.json": character_inventory_chains,
        "inventory_item_queries.json": inventory_item_queries
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()