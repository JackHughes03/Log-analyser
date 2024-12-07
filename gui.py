from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QPushButton,
    QFileDialog,
    QHBoxLayout,
    QComboBox,
    QScrollArea,
    QLineEdit,
    QCheckBox,
)
from PySide6.QtCore import Qt
import sys
from pathlib import Path
import re
import time
import keyring
import getpass
import json
from datetime import datetime
# Import styles
from styles import *

# Functions to analyse log files
from utils import (
    get_response_codes,
    get_all_ip_addresses,
    get_most_requested_files,
    get_tools_used,
    get_peak_traffic_times,
)

# Constants for keyring
KEYRING_SERVICE = "LogAnalyser"
KEYRING_USERNAME = getpass.getuser()  # Uses system username


# Replace the global api_token variable with getter/setter functions
def get_api_token():
    return keyring.get_password(KEYRING_SERVICE, KEYRING_USERNAME) or ""


def set_api_token(token):
    keyring.set_password(KEYRING_SERVICE, KEYRING_USERNAME, token)


def create_app():
    return QApplication(sys.argv)


def create_window():
    window = QWidget()
    window.setWindowTitle("Log Analyser")
    window.setStyleSheet(WINDOW_STYLE)
    window.resize(800, 600)
    return window


def create_layout():
    layout = QVBoxLayout()
    layout.setSpacing(15)
    layout.setContentsMargins(50, 30, 50, 30)
    return layout


def create_heading():
    heading_container = QVBoxLayout()
    heading_container.setSpacing(8)

    heading = QLabel("Log Analyser")
    heading.setStyleSheet(HEADING_STYLE)
    heading.setAlignment(Qt.AlignmentFlag.AlignLeft)

    description = QLabel(
        "A modern tool for analysing web server logs with real-time visualisation."
    )
    description.setStyleSheet(DESCRIPTION_STYLE)
    description.setAlignment(Qt.AlignmentFlag.AlignLeft)

    global uploaded_file_label
    uploaded_file_label = QLabel("No file uploaded")
    uploaded_file_label.setStyleSheet(UPLOADED_FILE_LABEL_STYLE)
    uploaded_file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    heading_container_widget = QWidget()
    heading_container_widget.setLayout(heading_container)
    heading_container.addWidget(heading)
    heading_container.addWidget(description)
    heading_container.addWidget(uploaded_file_label)

    return heading_container_widget


def create_dark_panel():
    dark_panel = QFrame()
    dark_panel.setStyleSheet(DARK_PANEL_STYLE)
    dark_panel.setFixedSize(700, 450)
    panel_layout = QVBoxLayout()
    dark_panel.setLayout(panel_layout)

    scroll_area = QScrollArea()
    scroll_area.setStyleSheet(SCROLL_AREA_STYLE)
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
    text_label.setStyleSheet(TEXT_LABEL_STYLE)
    text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
    text_label.setWordWrap(True)
    text_label.setTextFormat(Qt.TextFormat.RichText)  # Ensure HTML is rendered
    return text_label


def create_button_styles():
    return BUTTON_STYLE_PRIMARY, BUTTON_STYLE_SUCCESS, BUTTON_STYLE_DISABLED


def create_buttons(
    window,
    text_label,
    button_style_primary,
    button_style_success,
    button_style_disabled,
    scroll_area,
):
    upload_button = QPushButton("Upload Log")
    analyse_button = QPushButton("Analyse Log")

    upload_button.clicked.connect(
        lambda: upload_file(
            window,
            text_label,
            upload_button,
            analyse_button,
            button_style_success,
            button_style_primary,
            scroll_area,
        )
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


def upload_file(
    window,
    text_label,
    upload_button,
    analyse_button,
    button_style_success,
    button_style_primary,
    scroll_area,
):
    file_path, _ = QFileDialog.getOpenFileName(
        window,
        "Select Log File",
        "",
        "Log Files (*.log);;Text Files (*.txt);;All Files (*.*)",
    )
    if file_path:
        token = get_api_token()

        filename = Path(file_path).name
        set_text_with_color(
            text_label, f"Selected file: {filename}", "#ffcc00", scroll_area
        )
        window.selected_file = file_path
        analyse_button.setEnabled(True)
        analyse_button.setStyleSheet(button_style_primary)
        upload_button.setStyleSheet(button_style_success)

        # Update uploaded file label
        uploaded_file_label.setText(f"Uploaded file: {filename}")
        uploaded_file_label.setStyleSheet(f"color: {THEME_TEXT};")


def generate_report(file_path):
    with open("report.txt", "w") as report:
        report.write("=== LOG ANALYSIS REPORT ===\n\n")

        # Response Codes
        report.write("RESPONSE CODES\n")
        report.write("--------------\n")
        response_codes = get_response_codes(file_path, full_report=True)
        for code, count in sorted(
            response_codes.items(), key=lambda x: x[1], reverse=True
        ):
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
        for (file, code), count in sorted(
            files.items(), key=lambda x: x[1], reverse=True
        ):
            report.write(f"{file} - accessed {count} times with response code {code}\n")
        report.write("\n")

        # Tools Used
        report.write("TOOLS USED\n")
        report.write("----------\n")
        tools = get_tools_used(file_path, full_report=True)
        for tool, count in sorted(tools.items(), key=lambda x: x[1], reverse=True):
            report.write(f"{tool} - used {count} times\n")

    # Get IP data
    ip_addresses = get_all_ip_addresses(file_path, full_report=True)
    
    # Create stats.json with the counts
    stats = {
        "ip_count": len(ip_addresses),
        "request_count": sum(ip_addresses.values()),
        "error_count": len(get_response_codes(file_path, full_report=True)),
        "asset_count": len(get_most_requested_files(file_path, full_report=True)),
        "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    with open("stats.json", "w") as f:
        json.dump(stats, f)
    
    # Create ips.json with IPs and their request counts
    ip_list = [{"ip": ip, "requests": count} for ip, count in ip_addresses.items()]
    # Sort by request count in descending order
    ip_list.sort(key=lambda x: x["requests"], reverse=True)
    
    with open("ips.json", "w") as f:
        json.dump(ip_list, f)


def analyse_log(window, text_label, scroll_area):
    if hasattr(window, "selected_file"):
        filename = Path(window.selected_file).name
        text_label.clear()
        set_text_with_color(
            text_label, f"Analysing file: {filename}", "#00ff00", scroll_area
        )

        # Response Codes Analysis
        if window.analysis_options["response_codes"].isChecked():
            set_text_with_color(
                text_label, "\nResponse Codes Analysis:", "#00ff00", scroll_area
            )
            get_response_codes(
                window.selected_file, text_label, scroll_area, set_text_with_color
            )
            set_text_with_color(
                text_label,
                "Successfully analysed response codes",
                "#00ff00",
                scroll_area,
            )

        # IP Analysis
        if window.analysis_options["ip_analysis"].isChecked():
            set_text_with_color(
                text_label, "\nIP Address Analysis:", "#00ff00", scroll_area
            )
            get_all_ip_addresses(
                window.selected_file, text_label, scroll_area, set_text_with_color
            )
            set_text_with_color(
                text_label, "Successfully analysed IPs", "#00ff00", scroll_area
            )

        # Requested Files Analysis
        if window.analysis_options["file_requests"].isChecked():
            set_text_with_color(
                text_label, "\nRequested Files Analysis:", "#00ff00", scroll_area
            )
            get_most_requested_files(
                window.selected_file, text_label, scroll_area, set_text_with_color
            )
            set_text_with_color(
                text_label,
                "Successfully analysed requested files",
                "#00ff00",
                scroll_area,
            )

        # Tools Analysis
        if window.analysis_options["tools_analysis"].isChecked():
            set_text_with_color(text_label, "\nTools Analysis:", "#00ff00", scroll_area)
            get_tools_used(
                window.selected_file, text_label, scroll_area, set_text_with_color
            )
            set_text_with_color(
                text_label, "Successfully analysed tools used", "#00ff00", scroll_area
            )

        # Traffic Analysis
        if window.analysis_options["traffic_analysis"].isChecked():
            set_text_with_color(
                text_label, "\nTraffic Analysis:", "#00ff00", scroll_area
            )
            get_peak_traffic_times(
                window.selected_file, text_label, scroll_area, set_text_with_color
            )
            set_text_with_color(
                text_label,
                "Successfully analysed traffic patterns",
                "#00ff00",
                scroll_area,
            )

        set_text_with_color(
            text_label,
            "\nCheck out the full report located at report.txt",
            "#00ff00",
            scroll_area,
        )
        generate_report(window.selected_file)


def update_api_token(token_input, text_label, scroll_area, status_label):
    token = token_input.text()
    try:
        # Store in keychain
        set_api_token(token)
        print(f"API token updated successfully")
        set_text_with_color(
            text_label, "API token updated successfully", "#00ff00", scroll_area
        )

        # Update status label
        status_label.setText("✓")
        status_label.setStyleSheet(TOKEN_STATUS_LABEL_STYLE(True))
    except Exception as e:
        print(f"Error storing API token: {e}")
        set_text_with_color(
            text_label, f"Error storing API token: {e}", "#ff0000", scroll_area
        )
        status_label.setText("✗")
        status_label.setStyleSheet(TOKEN_STATUS_LABEL_STYLE(False))


def get_token(token_input):
    # take user to https://ipinfo.io/account/token
    import webbrowser

    webbrowser.open("https://ipinfo.io/account/token")


def toggle_rate_limiting(rate_limit_switch, api_widgets):
    is_checked = rate_limit_switch.isChecked()

    # Show/hide all API-related widgets
    for widget in api_widgets:
        widget.setVisible(is_checked)


def create_side_panel(window, text_label, scroll_area):
    side_panel = QFrame()
    side_layout = QVBoxLayout()
    side_layout.setSpacing(15)
    side_layout.setContentsMargins(15, 15, 15, 15)

    side_panel.setStyleSheet(SIDE_PANEL_STYLE)

    title = QLabel("Analysis Settings")
    title.setStyleSheet(SIDE_PANEL_TITLE_STYLE)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    side_layout.addWidget(title)

    # Create checkboxes for each analysis feature first
    analysis_options = {
        "response_codes": ("Response Codes Analysis", True),
        "ip_analysis": ("IP Address Analysis", True),
        "file_requests": ("File Request Analysis", True),
        "tools_analysis": ("Tools Analysis", True),
        "traffic_analysis": ("Traffic Analysis", True),
    }

    # Store checkboxes in window for access in analyse_log
    window.analysis_options = {}

    for key, (label, default_state) in analysis_options.items():
        checkbox = QCheckBox(label)
        checkbox.setChecked(default_state)
        checkbox.setStyleSheet(CHECKBOX_STYLE)
        side_layout.addWidget(checkbox)
        window.analysis_options[key] = checkbox

    separator = QFrame()
    separator.setFrameShape(QFrame.Shape.HLine)
    separator.setStyleSheet(SEPARATOR_STYLE)
    side_layout.addWidget(separator)

    rate_limit_switch = QCheckBox("I got rate limited")
    rate_limit_switch.setChecked(False)
    rate_limit_switch.setStyleSheet(CHECKBOX_STYLE)
    side_layout.addWidget(rate_limit_switch)

    # Create API token widgets
    api_widget_container = QWidget()
    api_layout = QVBoxLayout(api_widget_container)
    api_layout.setContentsMargins(0, 0, 0, 0)
    api_layout.setSpacing(10)

    # Create token input with status in a horizontal layout
    token_container = QHBoxLayout()
    token_container.setSpacing(0)  # Reduce spacing between input and status

    token_input = QLineEdit()
    token_input.setPlaceholderText("Enter API Token")
    token_input.setStyleSheet(TOKEN_INPUT_STYLE)

    # Add existing token if available
    token = get_api_token()
    if token:
        token_input.setText(token)

    status_label = create_token_status_label(bool(token))
    token_container.addWidget(token_input, stretch=1)  # Give input field more space
    token_container.addWidget(status_label)
    api_layout.addLayout(token_container)

    # Add token-related buttons
    get_token_button = QPushButton("Get API Token")
    get_token_button.setStyleSheet(GET_TOKEN_BUTTON_STYLE)
    get_token_button.setCursor(Qt.CursorShape.PointingHandCursor)
    get_token_button.clicked.connect(lambda: get_token(token_input))
    api_layout.addWidget(get_token_button)

    submit_token_button = QPushButton("Submit API Token")
    submit_token_button.setStyleSheet(SUBMIT_TOKEN_BUTTON_STYLE)
    submit_token_button.clicked.connect(
        lambda: update_api_token(token_input, text_label, scroll_area, status_label)
    )
    api_layout.addWidget(submit_token_button)

    # Initially hide the API widget container
    api_widget_container.setVisible(False)
    side_layout.addWidget(api_widget_container)

    # Connect the rate limit switch to toggle API widgets visibility
    rate_limit_switch.stateChanged.connect(
        lambda: api_widget_container.setVisible(rate_limit_switch.isChecked())
    )

    # Add stretch to push everything to the top
    side_layout.addStretch()

    side_panel.setLayout(side_layout)
    return side_panel, side_layout, token_input


def create_token_status_label(has_token=False):
    token = get_api_token()
    status_label = QLabel("✓" if token else "✗")
    status_label.setStyleSheet(TOKEN_STATUS_LABEL_STYLE(bool(token)))
    return status_label


def safe_get_api_token():
    try:
        return get_api_token()
    except Exception as e:
        print(f"Error accessing keychain: {e}")
        return ""


def safe_set_api_token(token):
    try:
        set_api_token(token)
        return True
    except Exception as e:
        print(f"Error storing in keychain: {e}")
        return False


def clear_api_token():
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_USERNAME)
        return True
    except Exception as e:
        print(f"Error clearing token: {e}")
        return False


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
    button_style_primary, button_style_success, button_style_disabled = (
        create_button_styles()
    )
    upload_button, analyse_button = create_buttons(
        window,
        text_label,
        button_style_primary,
        button_style_success,
        button_style_disabled,
        scroll_area,
    )

    button_layout.addWidget(upload_button)
    button_layout.addWidget(analyse_button)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    content_layout.addLayout(button_layout)

    # Create side panel (right side)
    side_panel, side_layout, token_input = create_side_panel(
        window, text_label, scroll_area
    )

    # Add stretch to push everything to the top
    side_layout.addStretch()

    # Add layouts to main layout
    main_layout.addLayout(content_layout, stretch=1)
    main_layout.addWidget(side_panel)

    # Load existing token
    token = get_api_token()
    if token:
        token_input.setText(token)

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
