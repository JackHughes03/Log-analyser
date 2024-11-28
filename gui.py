from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame, QPushButton, QFileDialog, QHBoxLayout, QComboBox, QScrollArea, QLineEdit, QCheckBox
from PySide6.QtCore import Qt
import sys
from pathlib import Path
import re
import time

# Colours
THEME_PRIMARY = "#3b82f6"  # Brighter blue
THEME_SECONDARY = "#1d4ed8"  # Richer dark blue
THEME_BACKGROUND = "#0f172a"  # Dark navy
THEME_PANEL = "#1e293b"  # Lighter navy
THEME_TEXT = "#f8fafc"  # Off white
THEME_SUCCESS = "#22c55e"  # Brighter green
THEME_ERROR = "#ef4444"  # Brighter red
THEME_WARNING = "#f59e0b"  # Brighter orange

# Functions to analyse log files
from utils import get_response_codes, get_all_ip_addresses, get_most_requested_files, get_tools_used, get_peak_traffic_times

# Global variable to store the API token
api_token = ""  # Default token

def create_app():
    return QApplication(sys.argv)

def create_window():
    window = QWidget()
    window.setWindowTitle("Log Analyser")
    window.setStyleSheet(f"background-color: {THEME_BACKGROUND};")
    window.resize(800, 600)  # Slightly larger window
    return window

def create_layout():
    layout = QVBoxLayout()
    layout.setSpacing(15)
    layout.setContentsMargins(50, 30, 50, 30)
    return layout

def create_heading():
    heading_container = QVBoxLayout()
    heading_container.setSpacing(8)  # Space between title and description
    
    # Create title
    heading = QLabel("Log Analyser")
    heading.setStyleSheet(f"""
        QLabel {{
            font-size: 32px;
            font-weight: bold;
            color: {THEME_TEXT};
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
    """)
    heading.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    # Create description
    description = QLabel("A modern tool for analysing web server logs with real-time visualisation.")
    description.setStyleSheet(f"""
        QLabel {{
            font-size: 14px;
            color: {THEME_TEXT}aa;  # Added transparency to the text
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin-bottom: 20px;
        }}
    """)
    description.setAlignment(Qt.AlignmentFlag.AlignLeft)
    
    # Add to container
    heading_container_widget = QWidget()
    heading_container_widget.setLayout(heading_container)
    heading_container.addWidget(heading)
    heading_container.addWidget(description)
    
    return heading_container_widget

def create_dark_panel():
    dark_panel = QFrame()
    dark_panel.setStyleSheet(f"""
        QFrame {{
            background-color: {THEME_PANEL};
            border-radius: 15px;
            margin: 5px;
        }}
    """)
    dark_panel.setFixedSize(700, 450)  # Slightly larger panel
    panel_layout = QVBoxLayout()
    dark_panel.setLayout(panel_layout)

    scroll_area = QScrollArea()
    scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: transparent;
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
    """)
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    content_widget = QWidget()
    content_widget.setStyleSheet("background-color: transparent;")
    content_layout = QVBoxLayout(content_widget)
    
    scroll_area.setWidget(content_widget)
    panel_layout.addWidget(scroll_area)

    return dark_panel, content_layout, scroll_area

def create_text_label():
    text_label = QLabel()
    text_label.setStyleSheet(f"""
        QLabel {{ 
            color: {THEME_TEXT};
            padding: 15px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 14px;
            line-height: 1.6;
            background-color: {THEME_PANEL};
            border-radius: 8px;
        }}
    """)
    text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
    text_label.setWordWrap(True)
    text_label.setTextFormat(Qt.TextFormat.RichText)  # Ensure HTML is rendered
    return text_label

def create_button_styles():
    button_style_base = f"""
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
    button_style_primary = button_style_base + f"""
        QPushButton {{
            background-color: {THEME_PRIMARY};
        }}
        QPushButton:hover {{
            background-color: {THEME_SECONDARY};
        }}
    """
    button_style_success = button_style_base + f"""
        QPushButton {{
            background-color: {THEME_SUCCESS};
        }}
        QPushButton:hover {{
            background-color: #047857;
        }}
    """
    button_style_disabled = button_style_base + """
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
    return button_style_primary, button_style_success, button_style_disabled

def create_buttons(window, text_label, button_style_primary, button_style_success, button_style_disabled, scroll_area):
    upload_button = QPushButton("Upload Log")
    analyse_button = QPushButton("Analyse Log")
    
    upload_button.clicked.connect(
        lambda: upload_file(window, text_label, upload_button, analyse_button, 
                          button_style_success, button_style_primary, scroll_area)
    )
    upload_button.setStyleSheet(button_style_primary)

    analyse_button.clicked.connect(lambda: analyse_log(window, text_label, scroll_area))
    analyse_button.setEnabled(False)
    analyse_button.setStyleSheet(button_style_disabled)

    return upload_button, analyse_button

def set_text_with_color(text_label, text, color, scroll_area):
    current_text = text_label.text()
    new_text = f"""
        <div style="margin: 8px 0;">
            <span style="color:{color};">{text}</span>
        </div>
    """
    if current_text:
        text_label.setText(current_text + new_text)
    else:
        text_label.setText(new_text)

    # Process events to ensure the UI updates
    QApplication.processEvents()

    # Scroll to the bottom
    scroll_area.verticalScrollBar().setValue(scroll_area.verticalScrollBar().maximum())

def upload_file(window, text_label, upload_button, analyse_button, button_style_success, button_style_primary, scroll_area):
    file_path, _ = QFileDialog.getOpenFileName(
        window,
        "Select Log File",
        "",
        "Log Files (*.log);;Text Files (*.txt);;All Files (*.*)"
    )
    if file_path:

        if api_token == "":
            set_text_with_color(text_label, "Please enter an API token", "#ff0000", scroll_area)
            return

        filename = Path(file_path).name
        set_text_with_color(text_label, f"Selected file: {filename}", "#ffcc00", scroll_area)
        window.selected_file = file_path
        analyse_button.setEnabled(True)
        analyse_button.setStyleSheet(button_style_primary)
        upload_button.setStyleSheet(button_style_success)


def generate_report(file_path):
    with open("report.txt", "w") as report:
        report.write("=== LOG ANALYSIS REPORT ===\n\n")
        
        # Response Codes
        report.write("RESPONSE CODES\n")
        report.write("--------------\n")
        response_codes = get_response_codes(file_path, full_report=True)
        for code, count in sorted(response_codes.items(), key=lambda x: x[1], reverse=True):
            report.write(f"{code} - appears {count} times\n")
        report.write("\n")
        
        # IP Addresses
        report.write("IP ADDRESSES\n")
        report.write("------------\n")
        ip_addresses = get_all_ip_addresses(file_path, full_report=True)
        for ip, count in sorted(ip_addresses.items(), key=lambda x: x[1], reverse=True):
            report.write(f"{ip} - appears {count} times\n")
        report.write("\n")
        
        # Requested Files
        report.write("REQUESTED FILES\n")
        report.write("---------------\n")
        files = get_most_requested_files(file_path, full_report=True)
        for (file, code), count in sorted(files.items(), key=lambda x: x[1], reverse=True):
            report.write(f"{file} - accessed {count} times with response code {code}\n")
        report.write("\n")
        
        # Tools Used
        report.write("TOOLS USED\n")
        report.write("----------\n")
        tools = get_tools_used(file_path, full_report=True)
        for tool, count in sorted(tools.items(), key=lambda x: x[1], reverse=True):
            report.write(f"{tool} - used {count} times\n")

def analyse_log(window, text_label, scroll_area):
    if hasattr(window, 'selected_file'):
        filename = Path(window.selected_file).name
        text_label.clear()
        set_text_with_color(text_label, f"Analysing file: {filename}", "#00ff00", scroll_area)

        # Response Codes Analysis
        if window.analysis_options['response_codes'].isChecked():
            set_text_with_color(text_label, "\nResponse Codes Analysis:", "#00ff00", scroll_area)
            get_response_codes(window.selected_file, text_label, scroll_area, set_text_with_color)
            set_text_with_color(text_label, "Successfully analysed response codes", "#00ff00", scroll_area)

        # IP Analysis
        if window.analysis_options['ip_analysis'].isChecked():
            set_text_with_color(text_label, "\nIP Address Analysis:", "#00ff00", scroll_area)
            get_all_ip_addresses(window.selected_file, text_label, scroll_area, set_text_with_color)
            set_text_with_color(text_label, "Successfully analysed IPs", "#00ff00", scroll_area)

        # Requested Files Analysis
        if window.analysis_options['file_requests'].isChecked():
            set_text_with_color(text_label, "\nRequested Files Analysis:", "#00ff00", scroll_area)
            get_most_requested_files(window.selected_file, text_label, scroll_area, set_text_with_color)
            set_text_with_color(text_label, "Successfully analysed requested files", "#00ff00", scroll_area)

        # Tools Analysis
        if window.analysis_options['tools_analysis'].isChecked():
            set_text_with_color(text_label, "\nTools Analysis:", "#00ff00", scroll_area)
            get_tools_used(window.selected_file, text_label, scroll_area, set_text_with_color)
            set_text_with_color(text_label, "Successfully analysed tools used", "#00ff00", scroll_area)

        # Traffic Analysis
        if window.analysis_options['traffic_analysis'].isChecked():
            set_text_with_color(text_label, "\nTraffic Analysis:", "#00ff00", scroll_area)
            get_peak_traffic_times(window.selected_file, text_label, scroll_area, set_text_with_color)
            set_text_with_color(text_label, "Successfully analysed traffic patterns", "#00ff00", scroll_area)

        set_text_with_color(text_label, "\nCheck out the full report located at report.txt", "#00ff00", scroll_area)
        generate_report(window.selected_file)


def update_api_token(token_input, text_label, scroll_area):
    global api_token
    api_token = token_input.text()
    print(f"API token updated to: {api_token}")
    set_text_with_color(text_label, f"API token updated to: {api_token}", "#00ff00", scroll_area)

    # save to file
    with open("api_token.txt", "w") as file:
        file.write(api_token)

def get_token(token_input):
    # take user to https://ipinfo.io/account/token
    import webbrowser
    webbrowser.open("https://ipinfo.io/account/token")

def create_side_panel(window):
    side_panel = QFrame()
    side_panel.setStyleSheet(f"""
        QFrame {{
            background-color: {THEME_PANEL};
            border-radius: 15px;
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 10px;
            margin: 10px 0;
        }}
        QCheckBox {{
            color: {THEME_TEXT};
            font-size: 14px;
            padding: 5px;
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 2px solid {THEME_PRIMARY};
        }}
        QCheckBox::indicator:unchecked {{
            background-color: transparent;
        }}
        QCheckBox::indicator:checked {{
            background-color: {THEME_PRIMARY};
            image: url(checkmark.png);
        }}
        QCheckBox::indicator:hover {{
            border-color: {THEME_SECONDARY};
        }}
    """)
    side_panel.setFixedWidth(300)  # Slightly wider
    
    # Create vertical layout for side panel
    side_layout = QVBoxLayout()
    side_layout.setSpacing(15)
    side_layout.setContentsMargins(15, 15, 15, 15)
    
    # Add title to side panel
    title = QLabel("API Token Settings")
    title.setStyleSheet(f"""
        QLabel {{
            color: {THEME_TEXT};
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
    """)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    side_layout.addWidget(title)
    
    # Create token input with status indicator
    token_container = QHBoxLayout()
    token_input = QLineEdit()
    token_input.setPlaceholderText("Enter API Token")
    token_input.setStyleSheet(f"""
        QLineEdit {{
            background-color: {THEME_PANEL};
            color: {THEME_TEXT};
            border: 2px solid rgba(59, 130, 246, 0.3);
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
        }}
        QLineEdit:focus {{
            border-color: {THEME_PRIMARY};
        }}
    """)
    
    # Check if token exists
    if Path("api_token.txt").exists() and Path("api_token.txt").stat().st_size > 0:
        has_token = True
    else:
        has_token = False

    status_label = create_token_status_label(has_token)
    
    token_container.addWidget(token_input)
    token_container.addWidget(status_label)
    side_layout.addLayout(token_container)
    
    # Add token-related buttons
    get_token_button = QPushButton("Get API Token")
    get_token_button.setStyleSheet(f"""
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
    """)
    get_token_button.setCursor(Qt.CursorShape.PointingHandCursor)
    get_token_button.clicked.connect(lambda: get_token(token_input))
    side_layout.addWidget(get_token_button)
    
    submit_token_button = QPushButton("Submit API Token")
    submit_token_button.setStyleSheet(f"""
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
    """)
    submit_token_button.clicked.connect(lambda: update_token_with_status(token_input, text_label, scroll_area))
    side_layout.addWidget(submit_token_button)
    
    # Add a separator
    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setStyleSheet(f"background-color: rgba(59, 130, 246, 0.2);")
    side_layout.addWidget(separator)
    
    # Add spacing before checkboxes
    side_layout.addStretch(1)  # Add stretch before checkboxes
    
    # Create checkboxes for each analysis feature
    analysis_options = {
        'response_codes': ('Response Codes Analysis', True),
        'ip_analysis': ('IP Address Analysis', True),
        'file_requests': ('File Request Analysis', True),
        'tools_analysis': ('Tools Analysis', True),
        'traffic_analysis': ('Traffic Analysis', True)
    }
    
    # Store checkboxes in window for access in analyse_log
    window.analysis_options = {}
    
    # Create a function to handle checkbox state changes
    def on_checkbox_change(state, key):
        print(f"{key} analysis {'enabled' if state else 'disabled'}")
    
    for key, (label, default_state) in analysis_options.items():
        checkbox = QCheckBox(label)
        checkbox.setChecked(default_state)
        checkbox.stateChanged.connect(lambda state, k=key: on_checkbox_change(state, k))
        side_layout.addWidget(checkbox)
        window.analysis_options[key] = checkbox
    
    # Add spacing after checkboxes
    side_layout.addStretch(1)  # Add stretch after checkboxes
    
    side_panel.setLayout(side_layout)
    return side_panel, side_layout, token_input

def create_token_status_label(has_token=False):
    status_label = QLabel("✓" if has_token else "✗")
    status_label.setStyleSheet(f"""
        QLabel {{
            color: {THEME_SUCCESS if has_token else THEME_ERROR};
            font-size: 18px;
            font-weight: bold;
        }}
    """)
    return status_label

def main():
    app = create_app()
    window = create_window()
    
    # Create main horizontal layout
    main_layout = QHBoxLayout()
    main_layout.setSpacing(0)
    main_layout.setContentsMargins(20, 20, 20, 20)
    
    # Create content layout (left side)
    content_layout = QVBoxLayout()
    content_layout.setSpacing(15)
    content_layout.setContentsMargins(0, 0, 20, 0)
    
    # Add existing widgets to content layout
    heading = create_heading()
    content_layout.addWidget(heading)
    content_layout.setAlignment(heading, Qt.AlignmentFlag.AlignLeft)
    
    # Add some spacing after the heading
    content_layout.addSpacing(20)
    
    dark_panel, panel_content_layout, scroll_area = create_dark_panel()
    content_layout.addWidget(dark_panel)
    content_layout.setAlignment(dark_panel, Qt.AlignmentFlag.AlignHCenter)
    
    text_label = create_text_label()
    panel_content_layout.addWidget(text_label)
    panel_content_layout.addStretch()
    
    # Add buttons
    button_layout = QHBoxLayout()
    button_style_primary, button_style_success, button_style_disabled = create_button_styles()
    upload_button, analyse_button = create_buttons(window, text_label, 
                                                 button_style_primary, 
                                                 button_style_success, 
                                                 button_style_disabled,
                                                 scroll_area)
    
    button_layout.addWidget(upload_button)
    button_layout.addWidget(analyse_button)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    content_layout.addLayout(button_layout)
    
    # Create side panel (right side)
    side_panel, side_layout, token_input = create_side_panel(window)
    
    # Add stretch to push everything to the top
    side_layout.addStretch()
    
    # Add layouts to main layout
    main_layout.addLayout(content_layout, stretch=1)
    main_layout.addWidget(side_panel)
    
    # Load existing token
    global api_token
    if Path("api_token.txt").exists():
        with open("api_token.txt", "r") as file:
            api_token = file.read().strip()
            token_input.setText(api_token)
    
    # Update main layout margins
    main_layout.setSpacing(20)
    main_layout.setContentsMargins(30, 30, 30, 30)
    
    # Update content layout margins
    content_layout.setSpacing(20)
    content_layout.setContentsMargins(0, 0, 30, 0)
    
    window.setLayout(main_layout)
    window.resize(1200, 700)  # Slightly larger window
    window.show()
    
    app.exec()

if __name__ == "__main__":
    main()

