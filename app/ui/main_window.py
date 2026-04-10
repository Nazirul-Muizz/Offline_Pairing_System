#print("Hello, World!")
from PySide6 import QtWidgets, QtCore
from .form_window import ConfigDialog
from db.connection import Database
from .constants import fields
from backend.config_manager import ConfigManager, CONFIG_PATH

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Pairing")
        self.db = Database()
        self.resize(1400, 900)

        config_manager = ConfigManager(CONFIG_PATH)
        print("Loaded config:", config_manager.config_data)
        dialog = ConfigDialog(fields)
        
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.project_data = {
                field['label']: (widget.currentText() if isinstance(widget, QtWidgets.QComboBox) else widget.text())
                for field, widget in zip(fields, dialog.widgets)
            }
            print("Data entered:", self.project_data)

        title = QtWidgets.QLabel(f"{config_manager.config_data['project']}_{config_manager.config_data['line']}_{config_manager.config_data['station']}", alignment=QtCore.Qt.AlignCenter)
        
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: black; border: 4px solid black; padding: 20px; background-color: yellow;")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)

        main_layout.addWidget(title)

        status_bar = QtWidgets.QLabel("Please scan the WIP", alignment=QtCore.Qt.AlignCenter)
        status_bar.setStyleSheet("font-size: 24px; color: black; background-color: lightgray; border: 2px solid white; padding: 10px;")

        input_field = QtWidgets.QLineEdit()
        input_field.setStyleSheet("font-size: 24px; color: black; background-color: white; border: 2px solid black; padding: 10px;")

        input_label = QtWidgets.QLabel("Serial Number:", alignment=QtCore.Qt.AlignCenter)
        input_label.setStyleSheet("font-size: 24px; color: black; bold: true;")

        interactive_layout = QtWidgets.QVBoxLayout()
        interactive_layout.addWidget(status_bar)
        sub_layout = QtWidgets.QHBoxLayout()
        sub_layout.addWidget(input_label)
        sub_layout.addWidget(input_field)
        interactive_layout.addLayout(sub_layout)

        content_layout = QtWidgets.QHBoxLayout()

        content1 = QtWidgets.QLabel("Content Area 1", alignment=QtCore.Qt.AlignCenter)
        content1.setStyleSheet("background-color: lightgray; color: black; font-size: 24px; border: 2px solid black; padding: 20px;")
        content2 = QtWidgets.QLabel("Content Area 2", alignment=QtCore.Qt.AlignCenter)
        content2.setStyleSheet("background-color: lightgray; color: black; font-size: 24px; border: 2px solid black; padding: 20px;")

        content_layout.addWidget(content1, stretch=2)
        content_layout.addWidget(content2, stretch=1)

        # Add horizontal layout into main layout
        main_layout.addLayout(interactive_layout, stretch=1)
        main_layout.addLayout(content_layout, stretch=5)
    
    def closeEvent(self, event):
        self.db.close_connection()
        event.accept()
        print("Database connection closed.")



        
        

        

