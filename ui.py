from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel,
    QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from skin_manager import SkinManager

class SkinChangerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("League of Legends Skin Changer")
        self.setGeometry(100, 100, 700, 500)
        self.skin_manager = SkinManager()
        self.setStyleSheet(self.load_stylesheet())

        # Central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Title label
        self.title_label = QLabel("Select a Skin to Apply")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.layout.addWidget(self.title_label)

        # Skin list
        self.skin_list = QListWidget()
        self.skin_list.addItems(self.skin_manager.get_available_skins())
        self.skin_list.setFont(QFont("Segoe UI", 12))
        self.skin_list.setStyleSheet("QListWidget { background: #2c2f33; color: #ffffff; border-radius: 5px; padding: 5px; }"
                                     "QListWidget::item:selected { background: #7289da; }")
        self.layout.addWidget(self.skin_list)

        # Buttons
        self.apply_button = QPushButton("Apply Skin")
        self.apply_button.setFont(QFont("Segoe UI", 12))
        self.apply_button.clicked.connect(self.apply_skin)
        self.layout.addWidget(self.apply_button)

        self.restore_button = QPushButton("Restore Original")
        self.restore_button.setFont(QFont("Segoe UI", 12))
        self.restore_button.clicked.connect(self.restore_original)
        self.layout.addWidget(self.restore_button)

    def load_stylesheet(self):
        # Returns a stylesheet string for a modern dark-themed UI.
        return """
        QMainWindow {
            background-color: #23272a;
        }
        QLabel {
            color: #ffffff;
        }
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
        QFileDialog {
            background-color: #2c2f33;
            color: #ffffff;
        }
        """

    def apply_skin(self):
        selected = self.skin_list.currentItem()
        if selected:
            skin_name = selected.text()
            skin_path = self.skin_manager.get_skin_path(skin_name)
            # Ask user for the League installation directory.
            lol_path = QFileDialog.getExistingDirectory(
                self, "Select League of Legends Installation Directory"
            )
            if lol_path:
                success = self.skin_manager.apply_skin(skin_name, skin_path, lol_path)
                if success:
                    QMessageBox.information(
                        self, "Success", f"Skin '{skin_name}' applied successfully."
                    )
                else:
                    QMessageBox.warning(
                        self, "Error", "Failed to apply skin. Check logs for details."
                    )
        else:
            QMessageBox.warning(
                self, "No selection", "Please select a skin from the list."
            )

    def restore_original(self):
        lol_path = QFileDialog.getExistingDirectory(
            self, "Select League of Legends Installation Directory"
        )
        if lol_path:
            success = self.skin_manager.restore_skin(lol_path)
            if success:
                QMessageBox.information(
                    self, "Success", "Original skins restored successfully."
                )
            else:
                QMessageBox.warning(
                    self, "Error", "Failed to restore skins. Check logs for details."
                )
