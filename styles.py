# Theme Colors
THEME_PRIMARY = "#3b82f6"  # Brighter blue
THEME_SECONDARY = "#1d4ed8"  # Richer dark blue
THEME_BACKGROUND = "#0f172a"  # Dark navy
THEME_PANEL = "#1e293b"  # Lighter navy
THEME_TEXT = "#f8fafc"  # Off white
THEME_SUCCESS = "#22c55e"  # Brighter green
THEME_ERROR = "#ef4444"  # Brighter red
THEME_WARNING = "#f59e0b"  # Brighter orange

# Window Styles
WINDOW_STYLE = f"background-color: {THEME_BACKGROUND};"

# Heading Styles
HEADING_STYLE = f"""
    QLabel {{
        font-size: 32px;
        font-weight: bold;
        color: {THEME_TEXT};
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
"""

DESCRIPTION_STYLE = f"""
    QLabel {{
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin-bottom: 20px;
        margin-top: 5px;
    }}
"""

UPLOADED_FILE_LABEL_STYLE = f"""
    QLabel {{
        color: {THEME_TEXT}aa;
        font-size: 14px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        margin-bottom: 10px;
        margin-left: 0px;
    }}
"""

# Panel Styles
DARK_PANEL_STYLE = """
    QFrame {
        margin: 5px;
    }
"""

SCROLL_AREA_STYLE = """
    QScrollArea {
        border: none;
        background-color: transparent;
        margin-left: 10px;
    }
    QScrollBar:vertical {
        border: none;
        background-color: #444444;
        width: 10px;
        margin: 0;
    }
    QScrollBar::handle:vertical {
        background-color: #666666;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #888888;
    }
    QScrollBar::add-line:vertical {
        height: 0px;
    }
    QScrollBar::sub-line:vertical {
        height: 0px;
    }
"""

# Text Label Style
TEXT_LABEL_STYLE = f"""
    QLabel {{ 
        color: {THEME_TEXT};
        padding: 15px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        background-color: {THEME_PANEL};
        border-radius: 8px;
    }}
"""

# Button Styles
BUTTON_STYLE_BASE = f"""
    QPushButton {{
        color: {THEME_TEXT};
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 600;
        margin: 10px;
        min-width: 150px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }}
    QPushButton:hover {{
        opacity: 0.9;
    }}
"""

BUTTON_STYLE_PRIMARY = (
    BUTTON_STYLE_BASE
    + f"""
    QPushButton {{
        background-color: {THEME_PRIMARY};
    }}
    QPushButton:hover {{
        background-color: {THEME_SECONDARY};
    }}
"""
)

BUTTON_STYLE_SUCCESS = (
    BUTTON_STYLE_BASE
    + f"""
    QPushButton {{
        background-color: {THEME_SUCCESS};
    }}
    QPushButton:hover {{
        background-color: #047857;
    }}
"""
)

BUTTON_STYLE_DISABLED = (
    BUTTON_STYLE_BASE
    + """
    QPushButton {
        background-color: #475569;
        color: #94a3b8;
    }
    QPushButton:disabled {
        background-color: #475569;
        color: #94a3b8;
    }
    QPushButton:hover {
        background-color: #475569;
    }
"""
)

# Side Panel Styles
SIDE_PANEL_STYLE = f"""
    QFrame {{
        border-radius: 15px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        background-color: {THEME_PANEL};
        padding: 10px;
        margin: 10px 0;
    }}
"""

SIDE_PANEL_TITLE_STYLE = f"""
    QLabel {{
        color: {THEME_TEXT};
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 10px;
    }}
"""

CHECKBOX_STYLE = f"""
    QCheckBox {{
        background-color: transparent;
        color: {THEME_TEXT};
        font-size: 14px;
        padding: 5px 0;
    }}
"""

TOKEN_INPUT_STYLE = f"""
    QLineEdit {{
        background-color: {THEME_PANEL};
        color: {THEME_TEXT};
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        margin-right: 5px;
    }}
    QLineEdit:focus {{
        border-color: {THEME_PRIMARY};
    }}
"""

GET_TOKEN_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {THEME_PRIMARY};
        border: none;
        padding: 8px 16px;
        font-size: 14px;
        font-weight: 600;
        text-decoration: underline;
    }}
    QPushButton:hover {{
        color: {THEME_SECONDARY};
    }}
"""

SUBMIT_TOKEN_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {THEME_PRIMARY};
        color: {THEME_TEXT};
        border: none;
        border-radius: 8px;
        padding: 12px;
        font-size: 14px;
        font-weight: 600;
    }}
    QPushButton:hover {{
        background-color: {THEME_SECONDARY};
    }}
"""

TOKEN_STATUS_LABEL_STYLE = (
    lambda success: f"""
    QLabel {{
        color: {THEME_SUCCESS if success else THEME_ERROR};
        font-size: 18px;
        font-weight: bold;
        padding: 10px 10px;
        background-color: {THEME_PANEL};
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 8px;
    }}
"""
)

SEPARATOR_STYLE = "background-color: rgba(59, 130, 246, 0.2);"

SETTINGS_STYLE = """
    QFrame {
        background-color: transparent;
        border-radius: 8px;
        padding: 16px;
    }
"""

PANEL_STYLE = """
    QFrame {
        background-color: transparent;
        border-radius: 8px;
        padding: 16px;
    }
"""
