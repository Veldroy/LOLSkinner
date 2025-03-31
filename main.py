import sys
import os
import shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QLineEdit, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fantome Skin Changer")
        self.setGeometry(100, 100, 500, 250)
        self.selected_skin = ""
        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Apply Your .fantome Skin")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setStyleSheet("color: #ffffff;")
        layout.addWidget(title)

        info = QLabel("Select a .fantome skin file to apply:")
        info.setFont(QFont("Segoe UI", 12))
        info.setStyleSheet("color: #ffffff;")
        layout.addWidget(info)

        self.skin_path_edit = QLineEdit()
        self.skin_path_edit.setPlaceholderText("Path to .fantome file")
        self.skin_path_edit.setStyleSheet("background: #2c2f33; color: #ffffff; padding: 5px; border-radius: 5px;")
        layout.addWidget(self.skin_path_edit)

        browse_btn = QPushButton("Browse")
        browse_btn.setFont(QFont("Segoe UI", 12))
        browse_btn.setStyleSheet(button_stylesheet())
        browse_btn.clicked.connect(self.browse_fantome)
        layout.addWidget(browse_btn)

        apply_btn = QPushButton("Apply Skin")
        apply_btn.setFont(QFont("Segoe UI", 12))
        apply_btn.setStyleSheet(button_stylesheet())
        apply_btn.clicked.connect(self.apply_skin)
        layout.addWidget(apply_btn)

        restore_btn = QPushButton("Restore Original")
        restore_btn.setFont(QFont("Segoe UI", 12))
        restore_btn.setStyleSheet(button_stylesheet())
        restore_btn.clicked.connect(self.restore_skin)
        layout.addWidget(restore_btn)

        self.setStyleSheet("background-color: #23272a;")

    def browse_fantome(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select .fantome Skin", "", "Fantome Files (*.fantome);;All Files (*)", options=options
        )
        if file_path:
            self.skin_path_edit.setText(file_path)
            self.selected_skin = file_path

    def apply_skin(self):
        if not self.selected_skin or not os.path.exists(self.selected_skin):
            QMessageBox.warning(self, "Error", "No valid .fantome file selected.")
            return

        lol_path = QFileDialog.getExistingDirectory(
            self, "Select League of Legends Installation Directory"
        )
        if not lol_path:
            return

        target_folder = os.path.join(lol_path, "CustomSkins")
        os.makedirs(target_folder, exist_ok=True)

        try:
            shutil.copy(self.selected_skin, target_folder)
            QMessageBox.information(self, "Success", "Skin applied successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to apply skin: {e}")

    def restore_skin(self):
        lol_path = QFileDialog.getExistingDirectory(
            self, "Select League of Legends Installation Directory"
        )
        if not lol_path:
            return

        target_folder = os.path.join(lol_path, "CustomSkins")
        if os.path.exists(target_folder):
            try:
                for file in os.listdir(target_folder):
                    if file.endswith(".fantome"):
                        os.remove(os.path.join(target_folder, file))
                QMessageBox.information(self, "Restored", "Original skins restored.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to restore skins: {e}")
        else:
            QMessageBox.information(self, "Info", "No custom skins found to restore.")

def button_stylesheet():
    return """
        QPushButton {
            background-color: #7289da;
            border: none;
            border-radius: 5px;
            padding: 10px;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #5b6eae;
        }
        QPushButton:pressed {
            background-color: #4e5d94;
        }
    """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
