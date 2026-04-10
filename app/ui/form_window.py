from PySide6.QtWidgets import (QDialog, QLabel, QComboBox, QLineEdit,
                               QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt
import sys
from backend.validation import validate_wo_number


class ConfigDialog(QDialog):
    """
    A reusable mandatory dialog:
    - Fields are provided in order
    - Dropdowns have predefined options
    - Text fields are open input
    - Fields are enabled only in order
    - Confirm validates all entries
    """
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
        
        for i, widget in enumerate(self.widgets[:-1]):
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
    
    def _on_field_changed(self, index, text):
        widget = self.widgets[index]

        # Special case: WO validation
        if index == self.wo_index:
            valid, msg = validate_wo_number(text)

            if valid:
                widget.setStyleSheet("border: 2px solid green;")
                self.confirm_btn.setEnabled(True)
            else:
                widget.setStyleSheet("border: 2px solid red;")
                self.confirm_btn.setEnabled(False)
                return  # block progression if invalid

        # Enable next field
        self._enable_next(index)

    # ---------------------------
    # Enable next field
    # ---------------------------
    def _enable_next(self, index):
        if index + 1 < len(self.widgets):
            self.widgets[index + 1].setEnabled(True)

            
    def confirm(self):
        self.accept()

    def cancel(self):
        sys.exit(0)

    def closeEvent(self, event):
        sys.exit(0)