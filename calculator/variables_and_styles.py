from pathlib import Path
import qdarktheme




# Diretórios
ROOT_DIR = Path(__file__).parent
FILES_DIR = ROOT_DIR / "files"
WINDOW_ICON_PATH = FILES_DIR / "icon.png"

#COLORS
PRIMARY_COLOR = "#1e81b0"
DARKER_PRIMARY_COLOR = "#16658a"
DARKEST_PRIMARY_COLOR = "#115270"

# Tamanhos
BIG_FONT_SIZE = 40
MEDIUM_FONT_SIZE = 24
SMALL_FONT_SIZE = 18
TEXT_MARGIN = 15
MINIMUN_WIDTH = 450

qss = f"""
    PushButton[cssClass="specialButton"] {{
        color: white;
        background-color: {PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:hover {{
        color: white;
        background-color: {DARKER_PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:pressed {{
        color: white;
        background-color: {DARKEST_PRIMARY_COLOR};
    }}
"""


def setupTheme():
    qdarktheme.setup_theme(
        theme="dark",
        corner_shape="rounded",
        custom_colors={
            '[dark]': {
                "primary": "#1e81b0",
            },
            "[light]": {
                "primary": "#1e81b0",
            },
        },
        additional_qss= qss
    )
