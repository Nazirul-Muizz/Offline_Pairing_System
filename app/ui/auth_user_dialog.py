from PySide6 import QtWidgets
from .constants import password

class AuthorizeUser(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(200, 100)

        layout = QtWidgets.QVBoxLayout()

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(QtWidgets.QLabel("Enter Password:"))
        layout.addWidget(self.password_input)

        button_layout = QtWidgets.QHBoxLayout()
        self.login_button = QtWidgets.QPushButton("Login")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.check_password)
        self.cancel_button.clicked.connect(self.reject)

    def check_password(self):
        if self.password_input.text() == password:
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Incorrect password!")