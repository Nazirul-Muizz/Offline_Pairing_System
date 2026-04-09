from PySide6.QtWidgets import (QDialog, QLabel, QComboBox, QLineEdit,
                               QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QWidget)
from PySide6.QtCore import Qt
import sys

class ConfigDialog(QDialog):
    """
    A reusable mandatory dialog:
    - Fields are provided in order
    - Dropdowns have predefined options
    - Text fields are open input
    - Fields are enabled only in order
    - Confirm validates all entries
    """
    def __init__(self, fields, title="Software Configuration", size=(700, 350)):
        
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(*size)

        self.fields = fields
        self.widgets = []  # list of widgets in order

        # --- Layout ---
        layout = QVBoxLayout()

        for field in self.fields:
            label = QLabel(f"{field['label']}:")
            layout.addWidget(label)
            
            if field['type'] == 'dropdown':
                widget = QComboBox()
                widget.addItem("Select...")
                widget.addItems(field.get('options', []))
            elif field['type'] == 'text':
                widget = QLineEdit()
            else:
                raise ValueError(f"Unknown field type: {field['type']}")
            
            layout.addWidget(widget)
            widget.setEnabled(False)  # initially all disabled
            self.widgets.append(widget)

        # Enable first field
        self.widgets[0].setEnabled(True)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.confirm_btn = QPushButton("Confirm")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # --- Signals ---
        for i, widget in enumerate(self.widgets[:-1]):
            if isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(lambda idx, i=i: self._enable_next(i))
            elif isinstance(widget, QLineEdit):
                widget.textChanged.connect(lambda text, i=i: self._enable_next(i))
        
        self.confirm_btn.clicked.connect(self.confirm)
        self.cancel_btn.clicked.connect(self.cancel)

    def _enable_next(self, index):
        """Enable the next field only if current is filled/selected"""
        widget = self.widgets[index]
        next_widget = self.widgets[index + 1]
        if isinstance(widget, QComboBox):
            next_widget.setEnabled(widget.currentIndex() > 0)
        elif isinstance(widget, QLineEdit):
            next_widget.setEnabled(bool(widget.text().strip()))

    def confirm(self):
        """Check all fields in order and show warnings if missing"""
        for i, (field, widget) in enumerate(zip(self.fields, self.widgets)):
            if isinstance(widget, QComboBox) and widget.currentIndex() == 0:
                QMessageBox.warning(self, "Warning", f"SELECT {field['label'].upper()} FIRST")
                return
            if isinstance(widget, QLineEdit) and not widget.text().strip():
                QMessageBox.warning(self, "Warning", f"ENTER {field['label'].upper()}")
                return

        #QMessageBox.information(self, "Success", "All data entered correctly!")
        self.accept()

    def cancel(self):
        sys.exit(0)

    def closeEvent(self, event):
        sys.exit(0)