from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt

class SettingDialog(QDialog):
    def __init__(self, title="Settings", size=(400, 200)):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(*size)

        layout = QVBoxLayout()

        label = QLabel("This is the settings dialog.")
        layout.addWidget(label)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.register_new_wo_btn = QPushButton("Register New WO")
        self.config_btn = QPushButton("Configure Features")

        btn_layout.addWidget(self.register_new_wo_btn)
        btn_layout.addWidget(self.config_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)