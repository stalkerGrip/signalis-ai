import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/timers")


TIMER_CREATE_PATTERN = re.compile(
    r'timer\.Create\s*\(\s*([\'"][^\'"]+[\'"]|[A-Za-z_][A-Za-z0-9_\.:\[\]\(\)\s"\']*)\s*,\s*([^,]+)\s*,\s*([^,]+)',
    re.DOTALL
)

TIMER_SIMPLE_PATTERN = re.compile(
    r'timer\.Simple\s*\(\s*([^,]+)\s*,',
    re.DOTALL
)

TIMER_REMOVE_PATTERN = re.compile(
    r'timer\.Remove\s*\(\s*([^\)]+)'
)

TIMER_EXISTS_PATTERN = re.compile(
    r'timer\.Exists\s*\(\s*([^\)]+)'
)

TIMER_REPS_LEFT_PATTERN = re.compile(
    r'timer\.RepsLeft\s*\(\s*([^\)]+)'
)

ENTITY_TIMER_CALL_PATTERN = re.compile(
    r':(SetSimpleTimer|SetCustomTimer|RemoveTimer|TimerExists|GetTimerFullIdentifier)\s*\('
)

PLAYER_ACTION_TIMER_PATTERN = re.compile(
    r':(setAction|setCancelAction|doStaredAction|DoingMovAction)\s*\('
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


def clean_expr(value):
    return value.strip().strip("'\"")


def classify_timer_repetition(repetitions):
    rep = repetitions.strip()

    if rep == "0":
        return "infinite"

    if rep == "1":
        return "single"

    return "finite_or_dynamic"


def classify_timer_delay(delay):
    value = delay.strip()

    try:
        numeric = float(value)

        if numeric <= 0:
            return "immediate_or_next_tick"

        if numeric < 1:
            return "subsecond"

        if numeric == 1:
            return "one_second"

        return "multi_second"

    except ValueError:
        return "dynamic"


def classify_entity_timer_method(method_name):
    if method_name == "SetSimpleTimer":
        return "entity_timer_simple"

    if method_name == "SetCustomTimer":
        return "entity_timer_create"

    if method_name == "RemoveTimer":
        return "entity_timer_remove"

    if method_name == "TimerExists":
        return "entity_timer_exists"

    if method_name == "GetTimerFullIdentifier":
        return "entity_timer_identifier"

    return "entity_timer_unknown"


def classify_player_action_method(method_name):
    if method_name == "setAction":
        return {
            "type": "player_action_timer",
            "cancelable": False,
            "uses_progress_bar": True,
            "uses_busy_state": True
        }

    if method_name == "setCancelAction":
        return {
            "type": "player_cancelable_action_timer",
            "cancelable": True,
            "uses_progress_bar": True,
            "uses_busy_state": True
        }

    if method_name == "doStaredAction":
        return {
            "type": "player_stared_action_timer",
            "cancelable": True,
            "uses_progress_bar": False,
            "uses_busy_state": False
        }

    if method_name == "DoingMovAction":
        return {
            "type": "player_action_timer_check",
            "cancelable": None,
            "uses_progress_bar": False,
            "uses_busy_state": False
        }

    return {
        "type": "player_action_timer_unknown",
        "cancelable": None,
        "uses_progress_bar": None,
        "uses_busy_state": None
    }


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    timer_creates = []
    timer_simples = []
    timer_operations = []
    entity_timer_calls = []
    player_action_timers = []

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

                create_matches = list(TIMER_CREATE_PATTERN.finditer(content))
                simple_matches = list(TIMER_SIMPLE_PATTERN.finditer(content))
                remove_matches = list(TIMER_REMOVE_PATTERN.finditer(content))
                exists_matches = list(TIMER_EXISTS_PATTERN.finditer(content))
                reps_left_matches = list(TIMER_REPS_LEFT_PATTERN.finditer(content))
                entity_timer_matches = list(ENTITY_TIMER_CALL_PATTERN.finditer(content))
                player_action_matches = list(PLAYER_ACTION_TIMER_PATTERN.finditer(content))

                for match in create_matches:
                    timer_name = clean_expr(match.group(1))
                    delay = match.group(2).strip()
                    repetitions = match.group(3).strip()

                    timer_creates.append({
                        "type": "timer_create",
                        "timer_name": timer_name,
                        "delay_expr": delay,
                        "repetitions_expr": repetitions,
                        "delay_class": classify_timer_delay(delay),
                        "repetition_class": classify_timer_repetition(repetitions),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in simple_matches:
                    delay = match.group(1).strip()

                    timer_simples.append({
                        "type": "timer_simple",
                        "delay_expr": delay,
                        "delay_class": classify_timer_delay(delay),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in remove_matches:
                    timer_operations.append({
                        "type": "timer_remove",
                        "timer_name_expr": clean_expr(match.group(1)),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in exists_matches:
                    timer_operations.append({
                        "type": "timer_exists",
                        "timer_name_expr": clean_expr(match.group(1)),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in reps_left_matches:
                    timer_operations.append({
                        "type": "timer_reps_left",
                        "timer_name_expr": clean_expr(match.group(1)),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in entity_timer_matches:
                    method_name = match.group(1)

                    entity_timer_calls.append({
                        "type": classify_entity_timer_method(method_name),
                        "method_name": method_name,
                        "scope": "entity",
                        "validity_guard_expected": True,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in player_action_matches:
                    method_name = match.group(1)
                    classification = classify_player_action_method(method_name)

                    player_action_timers.append({
                        "type": classification["type"],
                        "method_name": method_name,
                        "scope": "player",
                        "cancelable": classification["cancelable"],
                        "uses_progress_bar": classification["uses_progress_bar"],
                        "uses_busy_state": classification["uses_busy_state"],
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
        "timer_creates.json": timer_creates,
        "timer_simples.json": timer_simples,
        "timer_operations.json": timer_operations,
        "entity_timer_calls.json": entity_timer_calls,
        "player_action_timers.json": player_action_timers
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()