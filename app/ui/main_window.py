#print("Hello, World!")
from PySide6 import QtWidgets, QtCore, QtGui
from .form_window import ConfigDialog
from db.connection import Database
from .constants import fields, stations
from backend.config_manager import ConfigManager, CONFIG_PATH
from .category import motor_pairing, pump_pairing, carton_pairing
from .setting import SettingDialog
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Pairing")
        self.db = Database()
        self.db.create_config_table()
        self.resize(1400, 900)

        config_manager = ConfigManager(CONFIG_PATH)
        print("Loaded config:", config_manager.config_data)
        dialog = ConfigDialog(fields)
        
        """
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            self.project_data = {
                field['label']: (widget.currentText() if isinstance(widget, QtWidgets.QComboBox) else widget.text())
                for field, widget in zip(fields, dialog.widgets)
            }
            print("Data entered:", self.project_data)
        """

        project = config_manager.config_data['project']
        line = config_manager.config_data['line']
        station = config_manager.config_data['station']

        title = QtWidgets.QLabel(
            f"{project}_{line}_{stations.get(station, station)}", 
            alignment=QtCore.Qt.AlignCenter
        )
        
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go up from ui/
        setting_img_path = os.path.join(BASE_DIR, "asset", "setting_button.jpg")
        setting_btn = QtWidgets.QPushButton("Settings")

        icon = QtGui.QIcon(setting_img_path)
        print(icon.isNull())
        setting_btn.setIcon(icon)

        setting_btn.setIconSize(QtCore.QSize(30, 30))

        setting_btn.clicked.connect(lambda: SettingDialog().exec())

        if station == "Motor_Pairing":
            pairing = motor_pairing.MotorPairing()
        elif station == "Pump_Pairing":
            pairing = pump_pairing.PumpPairing()
        elif station == "Carton_Pairing":
            pairing = carton_pairing.CartonPairing()

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main_layout = QtWidgets.QVBoxLayout(central)

        top_container = QtWidgets.QWidget()
        top_container.setObjectName("top_container")
        top_container.setStyleSheet("""
            QWidget#top_container {
                border: 4px solid black; 
                padding: 20px; 
                background-color: yellow;
            }""")
        
        top_container.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        top_layout = QtWidgets.QHBoxLayout(top_container)

        top_layout.setContentsMargins(10, 10, 10, 10)
        top_layout.setSpacing(10)

        top_layout.addWidget(setting_btn, alignment=QtCore.Qt.AlignLeft, stretch=1)
        top_layout.addWidget(title, alignment=QtCore.Qt.AlignCenter, stretch=10)
        top_layout.addWidget(QtWidgets.QWidget(), stretch=1)  # empty space on the right

        #top_layout.setStyleSheet("border: 4px solid black; padding: 20px; background-color: yellow;")

        #main_layout.addLayout(top_layout)
        main_layout.addWidget(top_container)

        # Interactive Layout

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



        
        

        

