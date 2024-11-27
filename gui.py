from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFrame, QPushButton, QFileDialog, QHBoxLayout
from PySide6.QtCore import Qt
import sys
from pathlib import Path

def create_app():
    return QApplication(sys.argv)

def create_window():
    window = QWidget()
    window.setWindowTitle("Log Analyser")
    window.setStyleSheet("background-color: #1a1a1a;")
    window.resize(700, 500)
    return window

def create_layout():
    layout = QVBoxLayout()
    layout.setSpacing(15)
    layout.setContentsMargins(50, 30, 50, 30)
    return layout

def create_heading():
    heading = QLabel("Log Analyser")
    heading.setStyleSheet("""
        QLabel {
            font-size: 28px;
            font-weight: bold;
            color: #ffffff;
            margin: 20px 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
    """)
    heading.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    return heading

def create_dark_panel():
    dark_panel = QFrame()
    dark_panel.setStyleSheet("""
        QFrame {
            background-color: #222222;
            border-radius: 15px;
        }
    """)
    dark_panel.setFixedSize(600, 300)
    panel_layout = QVBoxLayout()
    dark_panel.setLayout(panel_layout)
    return dark_panel, panel_layout

def create_text_label():
    text_label = QLabel()
    text_label.setStyleSheet("""
        QLabel { 
            color: #ffffff;
            padding: 10px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
    """)
    text_label.setAlignment(Qt.AlignmentFlag.AlignTop)
    text_label.setWordWrap(True)
    return text_label

def create_button_styles():
    button_style_base = """
        QPushButton {
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: 600;
            margin: 0px;
            min-width: 150px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        QPushButton:hover {
            background-color: #4a4a4a;
        }
    """
    button_style_primary = button_style_base + """
        QPushButton {
            background-color: #333333;
        }
    """
    button_style_success = button_style_base + """
        QPushButton {
            background-color: #2d5a27;
        }
        QPushButton:hover {
            background-color: #366c2f;
        }
    """
    button_style_disabled = button_style_base + """
        QPushButton {
            background-color: #2a2a2a;
            color: #666666;
        }
        QPushButton:disabled {
            background-color: #2a2a2a;
            color: #666666;
        }
        QPushButton:hover {
            background-color: #2a2a2a;
        }
    """
    return button_style_primary, button_style_success, button_style_disabled

def create_buttons(window, text_label, button_style_primary, button_style_success, button_style_disabled):
    upload_button = QPushButton("Upload Log")
    analyse_button = QPushButton("Analyse Log")
    
    upload_button.clicked.connect(
        lambda: upload_file(window, text_label, upload_button, analyse_button, 
                          button_style_success, button_style_primary)
    )
    upload_button.setStyleSheet(button_style_primary)

    analyse_button.clicked.connect(lambda: analyse_log(window, text_label))
    analyse_button.setEnabled(False)
    analyse_button.setStyleSheet(button_style_disabled)

    return upload_button, analyse_button

def upload_file(window, text_label, upload_button, analyse_button, button_style_success, button_style_primary):
    file_path, _ = QFileDialog.getOpenFileName(
        window,
        "Select Log File",
        "",
        "Log Files (*.log);;Text Files (*.txt);;All Files (*.*)"
    )
    if file_path:
        filename = Path(file_path).name
        current_text = text_label.text()
        new_text = f"Selected file: {filename}\n"
        text_label.setText(current_text + new_text)
        window.selected_file = file_path
        analyse_button.setEnabled(True)
        analyse_button.setStyleSheet(button_style_primary)
        upload_button.setStyleSheet(button_style_success)

def analyse_log(window, text_label):
    if hasattr(window, 'selected_file'):
        filename = Path(window.selected_file).name
        current_text = text_label.text()
        new_text = f"Analysing file: {filename}\n"
        text_label.setText(current_text + new_text)

def main():
    app = create_app()
    window = create_window()
    layout = create_layout()

    heading = create_heading()
    layout.addWidget(heading)

    dark_panel, panel_layout = create_dark_panel()
    layout.addWidget(dark_panel)
    layout.setAlignment(dark_panel, Qt.AlignmentFlag.AlignHCenter)

    text_label = create_text_label()
    panel_layout.addWidget(text_label)

    button_layout = QHBoxLayout()
    button_style_primary, button_style_success, button_style_disabled = create_button_styles()
    upload_button, analyse_button = create_buttons(window, text_label, button_style_primary, button_style_success, button_style_disabled)
    
    button_layout.addWidget(upload_button)
    button_layout.addWidget(analyse_button)
    button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    
    layout.addLayout(button_layout)

    window.setLayout(layout)
    window.show()

    app.exec()

if __name__ == "__main__":
    main()

