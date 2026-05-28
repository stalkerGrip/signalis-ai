import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/persistence")


DATA_ACCESS_PATTERN = re.compile(
    r'([A-Za-z_][A-Za-z0-9_]*(?::getChar\(\))?):'
    r'(setData|getData)\s*\((.*?)\)',
    re.DOTALL
)

SELF_DATA_ACCESS_PATTERN = re.compile(
    r'self:(setData|getData)\s*\((.*?)\)',
    re.DOTALL
)

NETVAR_PATTERN = re.compile(
    r'([A-Za-z_][A-Za-z0-9_]*|self):'
    r'(setNetVar|getNetVar)\s*\((.*?)\)',
    re.DOTALL
)

DB_CALL_PATTERN = re.compile(
    r'nut\.db\.([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

SQL_CALL_PATTERN = re.compile(
    r'sql\.([A-Za-z_][A-Za-z0-9_]*)\s*\('
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

    return "unknown_file"


def extract_first_string_argument(args):
    match = re.search(
        r'[\'"]([^\'"]+)[\'"]',
        args
    )

    if match:
        return match.group(1)

    return None


def method_access_type(method_name, state_domain):
    if method_name == "setData":
        return f"{state_domain}_data_write"

    if method_name == "getData":
        return f"{state_domain}_data_read"

    return "data_access"


def infer_state_domain(receiver, file_context, char_vars, item_vars):
    if receiver.endswith(":getChar()"):
        return "character", "high", "receiver_getChar"

    if receiver in char_vars:
        return "character", "high", "loop_over_nut.char.loaded"

    if receiver in item_vars:
        return "item", "high", "loop_over_getItemsOfType"

    if receiver in {"char", "character"}:
        return "character", "medium", "receiver_name"

    if receiver in {"item"}:
        return "item", "medium", "receiver_name"

    if receiver in {"client", "player", "ply"}:
        return "player_or_character_holder", "low", "player_variable_direct_data_access"

    if receiver == "self":
        if file_context == "item_file":
            return "item", "medium", "self_inside_item_file"

        if file_context == "entity_file":
            return "entity", "medium", "self_inside_entity_file"

        return "unknown", "low", "ambiguous_self"

    return "unknown", "low", "unrecognized_receiver"


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    data_access = []
    netvars = []
    db_calls = []
    sql_calls = []

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

                data_matches = list(DATA_ACCESS_PATTERN.finditer(content))
                self_data_matches = list(SELF_DATA_ACCESS_PATTERN.finditer(content))
                netvar_matches = list(NETVAR_PATTERN.finditer(content))
                db_matches = list(DB_CALL_PATTERN.finditer(content))
                sql_matches = list(SQL_CALL_PATTERN.finditer(content))

                for match in data_matches:
                    receiver = match.group(1)
                    method_name = match.group(2)
                    args = match.group(3).strip()
                    key = extract_first_string_argument(args)

                    state_domain, confidence, evidence = infer_state_domain(
                        receiver,
                        file_context,
                        char_vars,
                        item_vars
                    )

                    data_access.append({
                        "type": method_access_type(method_name, state_domain),
                        "method_name": method_name,
                        "receiver": receiver,
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

                for match in self_data_matches:
                    receiver = "self"
                    method_name = match.group(1)
                    args = match.group(2).strip()
                    key = extract_first_string_argument(args)

                    state_domain, confidence, evidence = infer_state_domain(
                        receiver,
                        file_context,
                        char_vars,
                        item_vars
                    )

                    data_access.append({
                        "type": method_access_type(method_name, state_domain),
                        "method_name": method_name,
                        "receiver": receiver,
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

                for match in netvar_matches:
                    receiver = match.group(1)
                    method_name = match.group(2)
                    args = match.group(3).strip()
                    key = extract_first_string_argument(args)

                    netvars.append({
                        "type": "netvar_write" if method_name == "setNetVar" else "netvar_read",
                        "method_name": method_name,
                        "receiver": receiver,
                        "key": key,
                        "raw_args": args,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "file_context": file_context
                    })

                for match in db_matches:
                    db_calls.append({
                        "type": "nut_db_call",
                        "method_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in sql_matches:
                    sql_calls.append({
                        "type": "sql_call",
                        "method_name": match.group(1),
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
        "data_access.json": data_access,
        "netvars.json": netvars,
        "db_calls.json": db_calls,
        "sql_calls.json": sql_calls
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()