from PySide6.QtWidgets import (QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt
from .auth_user import AuthorizeUser
from .register_wo_dialog import RegisterDialog
from .constants import fields, project, line, station
from db.connection import Database

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

        self.register_new_wo_btn.clicked.connect(self.create_new_wo)

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

    def create_new_wo(self):
        # Placeholder for config logic
        dialog = RegisterDialog(fields)
        if dialog.exec() == QDialog.Accepted:
            self.project_data = {
                field['label']: (widget.currentText() if isinstance(widget, QComboBox) else widget.text())
                for field, widget in zip(fields, dialog.widgets)
            }
            print("Data entered:", self.project_data)
            db = Database()
            db.insert_config_data(
                project,
                line,
                station,
                self.project_data['WO Number'],
                int(self.project_data['WO Quantity'])
            )
            QMessageBox.information(self, "Success", "WO registered successfully!")
        else:
            print("WO registration cancelled.")
            
    
    def configure_pairing_data(self):
        # Placeholder for config logic
        pass
        