import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/entities")


ENT_PROPERTY_PATTERN = re.compile(
    r'ENT\.([A-Za-z_][A-Za-z0-9_]*)\s*='
)

ENT_METHOD_PATTERN = re.compile(
    r'function\s+ENT:([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

SELF_METHOD_CALL_PATTERN = re.compile(
    r'self:([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

ENTITY_CLASS_PATTERN = re.compile(
    r'ENT\.Type\s*=\s*[\'"]([^\'"]+)[\'"]'
)

ENTITY_BASE_PATTERN = re.compile(
    r'ENT\.Base\s*=\s*[\'"]([^\'"]+)[\'"]'
)


LIFECYCLE_METHODS = {
    "Initialize",
    "Think",
    "Use",
    "Touch",
    "StartTouch",
    "EndTouch",
    "OnRemove",
    "Draw",
    "DrawTranslucent",
    "PhysicsCollide",
    "SetupDataTables"
}


ENGINE_CALLS = {
    "SetModel",
    "SetMaterial",
    "SetColor",
    "SetSkin",
    "SetBodygroup",
    "PhysicsInit",
    "SetMoveType",
    "SetSolid",
    "GetPhysicsObject",
    "SetCollisionGroup",
    "SetUseType",
    "DrawModel",
    "EmitSound",
    "SetPos",
    "GetPos",
    "GetAngles",
    "SetAngles",
    "GetClass",
    "Remove",
    "Spawn",
    "Activate"
}


NETWORK_CALLS = {
    "setNetVar",
    "getNetVar",
    "SetNWBool",
    "SetNWInt",
    "SetNWString",
    "SetNWEntity",
    "GetNWBool",
    "GetNWInt",
    "GetNWString",
    "GetNWEntity"
}


TIMER_ACTION_CALLS = {
    "SetSimpleTimer",
    "SetCustomTimer",
    "RemoveTimer",
    "TimerExists",
    "GetTimerFullIdentifier",
    "setAction",
    "setCancelAction",
    "doStaredAction"
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


def detect_entity_name(relative_path):
    normalized = relative_path.replace("\\", "/")
    parts = normalized.split("/")

    if "entities" in parts:
        index = len(parts) - 1 - parts[::-1].index("entities")

        if index + 1 < len(parts):
            return parts[index + 1]

    return None


def classify_entity_method(method_name):
    if method_name in LIFECYCLE_METHODS:
        return "entity_lifecycle_method"

    return "entity_gameplay_method"


def classify_entity_call(method_name):
    if method_name in ENGINE_CALLS:
        return "entity_engine_call"

    if method_name in NETWORK_CALLS:
        return "entity_network_call"

    if method_name in TIMER_ACTION_CALLS:
        return "entity_timer_or_action_call"

    return "entity_gameplay_call"


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    entity_classes = []
    entity_properties = []
    entity_lifecycle_methods = []
    entity_gameplay_methods = []
    entity_engine_calls = []
    entity_network_calls = []
    entity_timer_calls = []
    entity_gameplay_calls = []

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

            if "/entities/" not in f"/{normalized_path}":
                continue

            try:
                content = lua_file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                realm = detect_realm(relative_path)
                framework_layer = detect_framework_layer(str(lua_file))
                entity_name = detect_entity_name(relative_path)

                property_matches = list(ENT_PROPERTY_PATTERN.finditer(content))
                method_matches = list(ENT_METHOD_PATTERN.finditer(content))
                self_call_matches = list(SELF_METHOD_CALL_PATTERN.finditer(content))
                class_matches = list(ENTITY_CLASS_PATTERN.finditer(content))
                base_matches = list(ENTITY_BASE_PATTERN.finditer(content))

                if not (
                    property_matches
                    or method_matches
                    or self_call_matches
                    or class_matches
                    or base_matches
                ):
                    continue

                entity_type = class_matches[0].group(1) if class_matches else None
                entity_base = base_matches[0].group(1) if base_matches else None

                entity_classes.append({
                    "type": "entity_class",
                    "entity_name": entity_name,
                    "entity_type": entity_type,
                    "entity_base": entity_base,
                    "file": relative_path,
                    "realm": realm,
                    "framework_layer": framework_layer,
                    "property_count": len(property_matches),
                    "method_count": len(method_matches),
                    "self_call_count": len(self_call_matches)
                })

                for match in property_matches:
                    entity_properties.append({
                        "type": "entity_property",
                        "entity_name": entity_name,
                        "property_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in method_matches:
                    method_name = match.group(1)
                    method_type = classify_entity_method(method_name)

                    entry = {
                        "type": method_type,
                        "entity_name": entity_name,
                        "method_name": method_name,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer,
                        "lifecycle": method_name in LIFECYCLE_METHODS
                    }

                    if method_type == "entity_lifecycle_method":
                        entity_lifecycle_methods.append(entry)
                    else:
                        entity_gameplay_methods.append(entry)

                for match in self_call_matches:
                    method_name = match.group(1)
                    call_type = classify_entity_call(method_name)

                    entry = {
                        "type": call_type,
                        "entity_name": entity_name,
                        "method_name": method_name,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    }

                    if call_type == "entity_engine_call":
                        entity_engine_calls.append(entry)
                    elif call_type == "entity_network_call":
                        entity_network_calls.append(entry)
                    elif call_type == "entity_timer_or_action_call":
                        entity_timer_calls.append(entry)
                    else:
                        entity_gameplay_calls.append(entry)

            except Exception as e:
                print(f"Error reading {lua_file}: {e}")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    outputs = {
        "entity_classes.json": entity_classes,
        "entity_properties.json": entity_properties,
        "entity_lifecycle_methods.json": entity_lifecycle_methods,
        "entity_gameplay_methods.json": entity_gameplay_methods,
        "entity_engine_calls.json": entity_engine_calls,
        "entity_network_calls.json": entity_network_calls,
        "entity_timer_calls.json": entity_timer_calls,
        "entity_gameplay_calls.json": entity_gameplay_calls
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()