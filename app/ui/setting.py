from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt
from .auth_user import AuthorizeUser
from .form_window import ConfigDialog
from .constants import fields

class SettingDialog(QDialog):
    def __init__(self, title="Settings", size=(300, 150)):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(*size)

        self.build_ui()
        self.run_auth()

    def build_ui(self):
        self.layout = QVBoxLayout()

        self.label = QLabel("This is the settings dialog.")
        self.layout.addWidget(self.label)

        btn_layout = QHBoxLayout()

        self.register_new_wo_btn = QPushButton("Register New WO")
        self.config_btn = QPushButton("Configure Features")

        btn_layout.addWidget(self.register_new_wo_btn)
        btn_layout.addWidget(self.config_btn)

        self.layout.addLayout(btn_layout)
        self.setLayout(self.layout)
    
    def run_auth(self):
        auth = AuthorizeUser()

        if auth.exec() != QDialog.Accepted:
            self.block_access()
    
    def block_access(self):
        self.register_new_wo_btn.setEnabled(False)
        self.config_btn.setEnabled(False)

        self.label.setText("Access Denied")

    def run_config(self):
        # Placeholder for config logic
        dialog = ConfigDialog(fields)

        