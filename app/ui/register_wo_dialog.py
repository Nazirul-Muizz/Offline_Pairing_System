from PySide6.QtWidgets import (QDialog, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt
import sys
from backend.form_validation import VALIDATORS
from db.connection import Database

class RegisterDialog(QDialog):

    def __init__(self, fields, title="Software Configuration", size=(300, 150)):
        
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(*size)

        self.fields = fields
        self.widgets = []  # list of widgets in order

        self.wo_index = None

        # --- Layout ---
        layout = QVBoxLayout()

        for i, field in enumerate(self.fields):
            label = QLabel(f"{field['label']}:")
            layout.addWidget(label)

            widget = QLineEdit()

            layout.addWidget(widget)
            widget.setEnabled(False)

            self.widgets.append(widget)

            # Track WO field index
            if field['label'] == "WO Number":
                self.wo_index = i

        # Enable first field
        if self.widgets:
            self.widgets[0].setEnabled(True)
        
        for i, widget in enumerate(self.widgets):
            widget.textChanged.connect(
                lambda text, i=i: self._on_field_changed(i, text)
            )

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.confirm_btn = QPushButton("Confirm")
        self.cancel_btn = QPushButton("Cancel")

        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.cancel_btn)

        self.confirm_btn.setEnabled(False)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.confirm_btn.clicked.connect(self.confirm)
        self.cancel_btn.clicked.connect(self.cancel)
    
    def _check_all_valid(self):
        for i, field in enumerate(self.fields):
            widget = self.widgets[i]
            value = widget.text()

            validator_key = field.get("validator")

            if validator_key:
                validator = VALIDATORS.get(validator_key)
                if validator:
                    valid, _ = validator(value)
                    if not valid:
                        return False

        return True
    
    def _on_field_changed(self, index, text):
        field = self.fields[index]
        widget = self.widgets[index]

        value = text

        if field["type"] == "int":
            # block invalid typing early
            if not value.isdigit() and value != "":
                widget.setStyleSheet("border: 2px solid red;")
                return

        elif field["type"] == "str":
            value = value.strip()

        validator_key = field.get("validator")
        valid, msg = True, ""

        if validator_key:
            validator = VALIDATORS.get(validator_key)
            if validator:
                valid, msg = validator(value)
        
        if valid:
            widget.setStyleSheet("border: 2px solid green;")
            self._enable_next(index)
        else:
            widget.setStyleSheet("border: 2px solid red;")

        if self._check_all_valid():
            self.confirm_btn.setEnabled(True)
        else:
            self.confirm_btn.setEnabled(False)

    def _enable_next(self, index):
        if index + 1 < len(self.widgets):
            self.widgets[index + 1].setEnabled(True)
    
    def insert_new_wo(self, project, line, station, wo_number, wo_quantity):
        # Placeholder for database insertion logic
        print(f"Inserting WO: {wo_number} with Quantity: {wo_quantity}")
        db = Database()
        db.insert_config_data(project, line, station, wo_number, wo_quantity)
        

    def confirm(self):
        self.accept()

    def cancel(self):
        self.reject()

    def close_event(self, event):
        self.reject()