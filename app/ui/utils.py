from PySide6 import QtWidgets

def show_error(message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowTitle("Error")
    msg.setText(message)
    msg.exec()