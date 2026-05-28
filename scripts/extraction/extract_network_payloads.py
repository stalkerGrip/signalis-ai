import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/networking")


UTIL_ADD_NETWORK_STRING_PATTERN = re.compile(
    r'util\.AddNetworkString\s*\(\s*[\'"]([^\'"]+)[\'"]'
)

NET_WRITE_PATTERN = re.compile(
    r'net\.(Write[A-Za-z0-9_]*)\s*\((.*?)\)',
    re.DOTALL
)

NET_READ_PATTERN = re.compile(
    r'net\.(Read[A-Za-z0-9_]*)\s*\((.*?)\)',
    re.DOTALL
)

NET_MESSAGE_CONTEXT_PATTERN = re.compile(
    r'net\.(Start|Receive)\s*\(\s*[\'"]([^\'"]+)[\'"]'
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


def classify_net_write(method_name):
    if method_name in {"WriteEntity", "WritePlayer"}:
        return "net_write_entity_ref"

    if method_name in {"WriteString", "WriteUInt", "WriteInt", "WriteFloat", "WriteBool"}:
        return "net_write_primitive"

    if method_name in {"WriteTable", "WriteData"}:
        return "net_write_complex_or_bulk"

    return "net_write_other"


def classify_net_read(method_name):
    if method_name in {"ReadEntity", "ReadPlayer"}:
        return "net_read_entity_ref"

    if method_name in {"ReadString", "ReadUInt", "ReadInt", "ReadFloat", "ReadBool"}:
        return "net_read_primitive"

    if method_name in {"ReadTable", "ReadData"}:
        return "net_read_complex_or_bulk"

    return "net_read_other"


def find_nearest_message_context(content, position):
    nearest = None

    for match in NET_MESSAGE_CONTEXT_PATTERN.finditer(content):
        if match.start() <= position:
            nearest = {
                "message_direction": match.group(1),
                "message_name": match.group(2),
                "message_line_offset": match.start()
            }
        else:
            break

    return nearest


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    util_add_network_strings = []
    net_writes = []
    net_reads = []
    net_messages_deep = []

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

                add_string_matches = list(UTIL_ADD_NETWORK_STRING_PATTERN.finditer(content))
                write_matches = list(NET_WRITE_PATTERN.finditer(content))
                read_matches = list(NET_READ_PATTERN.finditer(content))
                message_context_matches = list(NET_MESSAGE_CONTEXT_PATTERN.finditer(content))

                for match in add_string_matches:
                    util_add_network_strings.append({
                        "type": "util_add_network_string",
                        "message_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in message_context_matches:
                    net_messages_deep.append({
                        "type": "net_message_context",
                        "message_direction": match.group(1),
                        "message_name": match.group(2),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in write_matches:
                    method_name = match.group(1)
                    raw_args = match.group(2).strip()
                    context = find_nearest_message_context(content, match.start())

                    net_writes.append({
                        "type": classify_net_write(method_name),
                        "method_name": method_name,
                        "raw_args": raw_args,
                        "message_name": context["message_name"] if context else None,
                        "message_direction": context["message_direction"] if context else None,
                        "context_confidence": "medium" if context else "low",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in read_matches:
                    method_name = match.group(1)
                    raw_args = match.group(2).strip()
                    context = find_nearest_message_context(content, match.start())

                    net_reads.append({
                        "type": classify_net_read(method_name),
                        "method_name": method_name,
                        "raw_args": raw_args,
                        "message_name": context["message_name"] if context else None,
                        "message_direction": context["message_direction"] if context else None,
                        "context_confidence": "medium" if context else "low",
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
        "util_add_network_strings.json": util_add_network_strings,
        "net_writes.json": net_writes,
        "net_reads.json": net_reads,
        "net_messages_deep.json": net_messages_deep
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()