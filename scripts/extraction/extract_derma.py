import re
import json
import yaml

from pathlib import Path


CONFIG_PATH = Path("config/workspace.yaml")
OUTPUT_DIR = Path("manifests/derma")


VGUI_CREATE_PATTERN = re.compile(
    r'vgui\.Create\s*\(\s*[\'"]([^\'"]+)[\'"]'
)

PANEL_METHOD_PATTERN = re.compile(
    r'function\s+PANEL:([A-Za-z_][A-Za-z0-9_]*)\s*\('
)

DERMA_PANEL_REGISTER_PATTERN = re.compile(
    r'vgui\.Register\s*\(\s*[\'"]([^\'"]+)[\'"]'
)

DERMA_MENU_PATTERN = re.compile(
    r'DermaMenu\s*\('
)

BUTTON_DOCLICK_PATTERN = re.compile(
    r'\.DoClick\s*=\s*function\s*\('
)

PAINT_CALLBACK_PATTERN = re.compile(
    r'\.(Paint|PaintOver|Think|PerformLayout)\s*=\s*function\s*\('
)

NETSTREAM_UI_PATTERN = re.compile(
    r'netstream\.Hook\s*\(\s*[\'"]([^\'"]+)[\'"]'
)


HOT_UI_CALLBACKS = {
    "Paint",
    "PaintOver",
    "Think",
    "PerformLayout"
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


def classify_ui_callback(name):
    if name in HOT_UI_CALLBACKS:
        return "ui_hotpath_callback"

    return "ui_callback"


def line_number_for(content, match):
    return content.count("\n", 0, match.start()) + 1


def load_workspace():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    workspace = load_workspace()

    vgui_creates = []
    panel_methods = []
    panel_registers = []
    derma_menus = []
    button_callbacks = []
    ui_hot_callbacks = []
    netstream_ui_hooks = []

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

                create_matches = list(VGUI_CREATE_PATTERN.finditer(content))
                panel_method_matches = list(PANEL_METHOD_PATTERN.finditer(content))
                register_matches = list(DERMA_PANEL_REGISTER_PATTERN.finditer(content))
                menu_matches = list(DERMA_MENU_PATTERN.finditer(content))
                button_matches = list(BUTTON_DOCLICK_PATTERN.finditer(content))
                paint_matches = list(PAINT_CALLBACK_PATTERN.finditer(content))
                netstream_matches = list(NETSTREAM_UI_PATTERN.finditer(content))

                if not (
                    create_matches
                    or panel_method_matches
                    or register_matches
                    or menu_matches
                    or button_matches
                    or paint_matches
                    or netstream_matches
                ):
                    continue

                for match in create_matches:
                    vgui_creates.append({
                        "type": "vgui_create",
                        "panel_class": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in panel_method_matches:
                    method_name = match.group(1)

                    panel_methods.append({
                        "type": classify_ui_callback(method_name),
                        "method_name": method_name,
                        "hotpath": method_name in HOT_UI_CALLBACKS,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in register_matches:
                    panel_registers.append({
                        "type": "vgui_register",
                        "panel_name": match.group(1),
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in menu_matches:
                    derma_menus.append({
                        "type": "derma_menu",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in button_matches:
                    button_callbacks.append({
                        "type": "ui_button_callback",
                        "callback": "DoClick",
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in paint_matches:
                    callback_name = match.group(1)

                    ui_hot_callbacks.append({
                        "type": classify_ui_callback(callback_name),
                        "callback": callback_name,
                        "hotpath": callback_name in HOT_UI_CALLBACKS,
                        "file": relative_path,
                        "line": line_number_for(content, match),
                        "realm": realm,
                        "framework_layer": framework_layer
                    })

                for match in netstream_matches:
                    netstream_ui_hooks.append({
                        "type": "netstream_ui_hook",
                        "message_name": match.group(1),
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
        "vgui_creates.json": vgui_creates,
        "panel_methods.json": panel_methods,
        "panel_registers.json": panel_registers,
        "derma_menus.json": derma_menus,
        "button_callbacks.json": button_callbacks,
        "ui_hot_callbacks.json": ui_hot_callbacks,
        "netstream_ui_hooks.json": netstream_ui_hooks
    }

    for filename, data in outputs.items():
        output_path = OUTPUT_DIR / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved {len(data)} entries -> {output_path}")


if __name__ == "__main__":
    main()