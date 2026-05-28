import re
import json
import yaml

from pathlib import Path

# ----------------------------------------
# Load workspace config
# ----------------------------------------

def detect_realm(path_str):
    lowered = path_str.lower()

    # Explicit prefixes
    if "\\cl_" in lowered or "/cl_" in lowered:
        return "client"

    if "\\sv_" in lowered or "/sv_" in lowered:
        return "server"

    if "\\sh_" in lowered or "/sh_" in lowered:
        return "shared"

    # Entity/init conventions
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

HOT_HOOKS = {
    "Think": "per_frame",
    "Tick": "tick",
    "HUDPaint": "render_frame",
    "PostDrawOpaqueRenderables": "render_frame"
}

HIGH_RISK_HOOKS = {
    "Think",
    "Tick",
    "HUDPaint",
    "PostDrawOpaqueRenderables"
}

CONFIG_PATH = Path("config/workspace.yaml")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

workspace = config

print("\n=== SOURCE ROOTS ===")
print(workspace)

# ----------------------------------------
# Hook extraction regex
# ----------------------------------------

NET_RECEIVE_PATTERN = re.compile(
    r'net\.Receive\s*\(\s*[\'"]([^\'"]+)[\'"]'
)
NET_START_PATTERN = re.compile(
    r'net\.Start\s*\(\s*[\'"]([^\'"]+)[\'"]'
)
NETSTREAM_HOOK_PATTERN = re.compile(
    r'netstream\.Hook\s*\(\s*[\'"]([^\'"]+)[\'"]'
)
PLUGIN_METHOD_PATTERN = re.compile(
    r'function\s+PLUGIN:([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

HOOK_ADD_PATTERN = re.compile(
    r'hook\.Add\s*\(\s*'
    r'([\'"][^\'"]+[\'"]|[A-Za-z_][A-Za-z0-9_\.]*)'
    r'\s*,\s*'
    r'([\'"][^\'"]+[\'"]|[A-Za-z_][A-Za-z0-9_\.]*)',
    re.DOTALL
)
HOOK_RUN_PATTERN = re.compile(
    r'hook\.(Run|Call)\s*\(\s*'
    r'([\'"][^\'"]+[\'"]|[A-Za-z_][A-Za-z0-9_\.]*)',
    re.DOTALL
)
NETSTREAM_START_PATTERN = re.compile(
    r'netstream\.Start\s*\(\s*(?:(?:client|ply|player|recipient|receivers)\s*,\s*)?([A-Za-z_][A-Za-z0-9_\.]*|[\'"][^\'"]+[\'"])'
)

def clean_lua_expr(value):
    value = value.strip()

    if len(value) >= 2 and value[0] in {"'", '"'} and value[-1] == value[0]:
        return value[1:-1], "literal"

    return value, "symbol"

hook_data = []
hook_buckets = {
    "client": [],
    "server": [],
    "shared": [],
    "unknown": []
}
net_receives = []
net_starts = []
plugin_methods = []
hook_runs = []
netstream_starts = []
netstream_hooks = []

# ----------------------------------------
# Scan source roots
# ----------------------------------------

for root in workspace["source_roots"]:
    root_path = Path(root)

    print(f"\nScanning root: {root_path}")

    if not root_path.exists():
        print("PATH DOES NOT EXIST")
        continue

    lua_files = list(root_path.rglob("*.lua"))

    print(f"Lua files found: {len(lua_files)}")

    for lua_file in lua_files:

        print(f"Reading: {lua_file}")

        try:
            content = lua_file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
            relative_path = str(lua_file.relative_to(root_path))
            realm = detect_realm(relative_path)
            framework_layer = detect_framework_layer(str(lua_file))
            plugin_method_matches = list(
                PLUGIN_METHOD_PATTERN.finditer(content)
            )

            for match in plugin_method_matches:
                method_name = match.group(1)

                line_number = content.count("\n", 0, match.start()) + 1

                plugin_methods.append({
                    "type": "plugin_method",
                    "method_name": method_name,
                    "file": relative_path,
                    "line": line_number,
                    "realm": realm,
                    "framework_layer": framework_layer
                })

            hook_run_matches = list(HOOK_RUN_PATTERN.finditer(content))

            for match in hook_run_matches:
                call_type = match.group(1)
                hook_expr = match.group(2)

                hook_value, resolution = clean_lua_expr(hook_expr)

                hook_runs.append({
                    "type": "hook_run",
                    "call_type": call_type,
                    "hook_name": hook_value if resolution == "literal" else None,
                    "symbol": hook_value if resolution == "symbol" else None,
                    "resolution": resolution,
                    "file": relative_path,
                    "line": content.count("\n", 0, match.start()) + 1,
                    "realm": realm,
                    "framework_layer": framework_layer
                })

            receive_matches = list(
                NET_RECEIVE_PATTERN.finditer(content)
            )

            for match in receive_matches:
                message_name = match.group(1)

                line_number = content.count(
                    "\n",
                    0,
                    match.start()
                ) + 1

                relative_path = str(
                    lua_file.relative_to(root_path)
                )

                net_receives.append({
                    "type": "net_receive",
                    "message_name": message_name,
                    "file": relative_path,
                    "line": line_number,
                    "realm": detect_realm(relative_path),
                    "framework_layer": detect_framework_layer(
                        str(lua_file)
                    )
                })

            start_matches  = list(
                NET_START_PATTERN.finditer(content)
            )

            for match in start_matches:
                message_name = match.group(1)

                line_number = content.count(
                    "\n",
                    0,
                    match.start()
                ) + 1

                relative_path = str(
                    lua_file.relative_to(root_path)
                )

                net_starts.append({
                    "type": "net_start",
                    "message_name": message_name,
                    "file": relative_path,
                    "line": line_number,
                    "realm": detect_realm(relative_path),
                    "framework_layer": detect_framework_layer(
                        str(lua_file)
                    )
                })

            netstreamhook_matches = list(
                NETSTREAM_HOOK_PATTERN.finditer(content)
            )

            for match in netstreamhook_matches:
                message_name = match.group(1)

                line_number = content.count(
                    "\n",
                    0,
                    match.start()
                ) + 1

                relative_path = str(
                    lua_file.relative_to(root_path)
                )

                netstream_hooks.append({
                    "type": "netstream_hook",
                    "message_name": message_name,
                    "file": relative_path,
                    "line": line_number,
                    "realm": detect_realm(relative_path),
                    "framework_layer": detect_framework_layer(
                        str(lua_file)
                    )
                })

            netstream_start_matches = list(
                NETSTREAM_START_PATTERN.finditer(content)
            )

            for match in netstream_start_matches:
                message_expr = match.group(1).strip("'\"")

                line_number = content.count("\n", 0, match.start()) + 1

                netstream_starts.append({
                    "type": "netstream_start",
                    "message_expr": message_expr,
                    "resolution": "literal" if "." not in message_expr else "unresolved_symbol",
                    "file": relative_path,
                    "line": line_number,
                    "realm": realm,
                    "framework_layer": framework_layer
                })

            matches = list(HOOK_ADD_PATTERN.finditer(content))

            if matches:
                print(f"HOOKS FOUND in {lua_file}")

            for match in matches:
                hook_expr = match.group(1)
                identifier_expr = match.group(2)

                hook_name, hook_resolution = clean_lua_expr(hook_expr)
                identifier, identifier_resolution = clean_lua_expr(identifier_expr)

                line_number = content.count("\n", 0, match.start()) + 1

                relative_path = str(lua_file.relative_to(root_path))

                realm = detect_realm(relative_path)

                framework_layer = detect_framework_layer(str(lua_file))

                frequency_class = HOT_HOOKS.get(
                    hook_name,
                    "event"
                )

                risk_class = (
                    "hotpath"
                    if hook_name in HIGH_RISK_HOOKS
                    else "normal"
                )

                hook_entry = {
                    "type": "hook",
                    "hook_name": hook_name,
                    "hook_resolution": hook_resolution,
                    "identifier": identifier,
                    "identifier_resolution": identifier_resolution,
                    "file": relative_path,
                    "line": line_number,
                    "realm": realm,
                    "framework_layer": framework_layer,
                    "frequency_class": frequency_class,
                    "risk_class": risk_class
                }

                hook_data.append(hook_entry)
                hook_buckets[realm].append(hook_entry)
        except Exception as e:

            print(f"Error reading {lua_file}: {e}")

# ----------------------------------------
# Final output
# ----------------------------------------

print("\n=== RESULTS ===")
OUTPUT_DIR = Path("manifests/hooks")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

output_files = {
    "client": "cl_hooks.json",
    "server": "sv_hooks.json",
    "shared": "sh_hooks.json",
    "unknown": "unknown_hooks.json"
}

for realm, hooks in hook_buckets.items():

    output_path = OUTPUT_DIR / output_files[realm]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(hooks, f, indent=2)

    print(
        f"Saved {len(hooks)} hooks -> {output_path}"
    )
NETWORKING_OUTPUT_DIR = Path("manifests/networking")

NETWORKING_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

networking_outputs = {
    "net_receives.json": net_receives,
    "net_starts.json": net_starts,
    "netstream_hooks.json": netstream_hooks,
    "netstream_starts.json": netstream_starts
}

for filename, data in networking_outputs.items():
    output_path = NETWORKING_OUTPUT_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} entries -> {output_path}")

CUSTOM_HOOKS_OUTPUT_DIR = Path("manifests/custom_hooks")

CUSTOM_HOOKS_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

custom_hook_outputs = {
    "plugin_methods.json": plugin_methods,
    "hook_runs.json": hook_runs,
}

for filename, data in custom_hook_outputs.items():
    output_path = CUSTOM_HOOKS_OUTPUT_DIR / filename

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} entries -> {output_path}")