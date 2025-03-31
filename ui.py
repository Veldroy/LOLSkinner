from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel,
    QFileDialog, QMessageBox
)
from skin_manager import SkinManager

class SkinChangerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("League of Legends Skin Changer")
        self.setGeometry(100, 100, 600, 400)
        self.skin_manager = SkinManager()

        # Set up the main UI components.
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.label = QLabel("Select a skin to apply:")
        self.layout.addWidget(self.label)

        self.skin_list = QListWidget()
        self.skin_list.addItems(self.skin_manager.get_available_skins())
        self.layout.addWidget(self.skin_list)

        self.apply_button = QPushButton("Apply Skin")
        self.apply_button.clicked.connect(self.apply_skin)
        self.layout.addWidget(self.apply_button)

        self.restore_button = QPushButton("Restore Original")
        self.restore_button.clicked.connect(self.restore_original)
        self.layout.addWidget(self.restore_button)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

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
