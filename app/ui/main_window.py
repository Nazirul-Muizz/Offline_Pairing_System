#print("Hello, World!")
from PySide6 import QtWidgets, QtCore, QtGui
from db.connection import Database
from .constants import stations, project, line, station
from .category import motor_pairing, pump_pairing, carton_pairing
from .setting_dialog import SettingDialog
from backend.main_validation import validate_wip_number
import os

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Offline Pairing")
        self.db = Database()
        self.db.create_config_table()
        self.setMinimumSize(1400, 900)

        title = QtWidgets.QLabel(
            f"{project}_{line}_{stations.get(station, station)}", 
            alignment=QtCore.Qt.AlignCenter
        )
        
        title.setStyleSheet("font-size: 32px; font-weight: bold;")

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # go up from ui/
        setting_img_path = os.path.join(BASE_DIR, "asset", "setting_button.jpg")
        refresh_img_path = os.path.join(BASE_DIR, "asset", "refresh_img.png")
        info_img_path = os.path.join(BASE_DIR, "asset", "info_icon.png")
        setting_btn = QtWidgets.QPushButton("Settings")
        refresh_btn = QtWidgets.QPushButton("Refresh")
        info_btn = QtWidgets.QPushButton("Info")

        setting_icon = QtGui.QIcon(setting_img_path)
        refresh_icon = QtGui.QIcon(refresh_img_path)
        info_icon = QtGui.QIcon(info_img_path)
        print(setting_icon.isNull())
        setting_btn.setIcon(setting_icon)
        refresh_btn.setIcon(refresh_icon)
        info_btn.setIcon(info_icon)

        setting_btn.setIconSize(QtCore.QSize(30, 30))
        refresh_btn.setIconSize(QtCore.QSize(30, 30))
        info_btn.setIconSize(QtCore.QSize(30, 30))

        setting_btn.clicked.connect(lambda: SettingDialog().exec())
        refresh_btn.clicked.connect(lambda: self.refresh_current_scan(table))
        # add info button functionality

        refresh_btn.setIcon(refresh_icon)
        refresh_btn.setIconSize(QtCore.QSize(30, 30))
        refresh_btn.clicked.connect(lambda: self.refresh_current_scan(table))

        if station == "MTRP":
            pairing = motor_pairing.MotorPairing()
            input_labels = pairing.label_array
            print(f"station: {station}")
        elif station == "PUMP":
            pairing = pump_pairing.PumpPairing()
            input_labels = pairing.label_array
            print(f"data: {input_labels[0]}")
        elif station == "PRPP":
            pairing = carton_pairing.CartonPairing()
            input_labels = pairing.label_array
            print(f"station: {station}")

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

        main_layout.addWidget(top_container)

        # Interactive Layout
        status_bar = QtWidgets.QLabel("Please scan the WIP", alignment=QtCore.Qt.AlignCenter)
        status_bar.setStyleSheet("font-size: 24px; color: black; background-color: lightgray; border: 2px solid white; padding: 10px; margin-top:10px")

        input_field = QtWidgets.QLineEdit()
        input_field.setStyleSheet("font-size: 18px; color: black; background-color: white; border: 2px solid black; padding: 10px; margin-top:10px")
        input_field.returnPressed.connect(lambda: self.handle_scan(status_bar, input_field, table))

        input_label = QtWidgets.QLabel("Serial Number:", alignment=QtCore.Qt.AlignCenter)
        input_label.setStyleSheet("font-size: 18px; color: black; bold: true; margin-left: 10px")

        interactive_layout = QtWidgets.QVBoxLayout()
        interactive_layout.addWidget(status_bar)
        sub_layout = QtWidgets.QHBoxLayout()
        sub_layout.addWidget(input_label, stretch=1)
        sub_layout.addWidget(input_field, stretch=10)
        sub_layout.addWidget(info_btn, stretch=1)
        interactive_layout.addLayout(sub_layout)

        content_container = QtWidgets.QWidget()
        content_container.setObjectName("content_container")
        content_container.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        content_container.setContentsMargins(5, 10, 10, 5)

        content_layout = QtWidgets.QHBoxLayout(content_container)

        prev_scan_layout = QtWidgets.QVBoxLayout()

        current_scan_btn = QtWidgets.QPushButton("Current Scan")
        current_scan_btn.setStyleSheet("font-size: 18px; padding: 5px; margin-bottom: 5px; margin-top: 10px;")
        past_scan_btn = QtWidgets.QPushButton("Past Scans")
        past_scan_btn.setStyleSheet("font-size: 18px; padding: 5px; margin-bottom: 5px; margin-top: 10px;")
        refresh_btn.setStyleSheet("font-size: 18px; padding: 5px; margin-bottom: 5px; margin-top: 10px;")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(current_scan_btn, alignment=QtCore.Qt.AlignLeft, stretch=1)
        button_layout.addWidget(past_scan_btn, alignment=QtCore.Qt.AlignLeft, stretch=1)
        button_layout.addWidget(QtWidgets.QWidget(), stretch=10)  # empty space on the right
        button_layout.addWidget(refresh_btn, alignment=QtCore.Qt.AlignRight, stretch=1)

        table = QtWidgets.QTableWidget()
        table.setRowCount(len(input_labels))
        table.setColumnCount(2)

        table.setVerticalHeaderLabels(input_labels)
        table.setHorizontalHeaderLabels(["Value", "Timestamp"])

        horizontal_header = table.horizontalHeader()
        vertical_header = table.verticalHeader()

        horizontal_header.setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        vertical_header.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.verticalHeader().setDefaultSectionSize(50)

        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        table.setStyleSheet("""
        QTableWidget {
            font-size: 20px;
            padding: 10px;
        }

        QHeaderView::section {
            border: 1px solid lightgray;
            background-color: #f0f0f0;
            padding: 5px;
            font-size: 18px;
        }
        """)

        prev_scan_layout.addLayout(button_layout)
        prev_scan_layout.addWidget(table, stretch=10)

        recent_scan_layout = QtWidgets.QVBoxLayout()

        recent_scan_title = QtWidgets.QLabel("Recent Scan")
        recent_scan_title.setStyleSheet("font-size: 20px; font-weight: bold; padding-top: 5px; margin-left: 20px; margin-bottom: 10px")

        self.recent_inputs = {}

        recent_scan_list = QtWidgets.QFormLayout()

        recent_scan_list.addRow(recent_scan_title)

        sku_label = QtWidgets.QLabel("SKU: ")
        sku_label.setStyleSheet("font-size: 18px; margin-left: 20px;")
        sku_input = QtWidgets.QLineEdit()
        sku_input.setReadOnly(True)
        sku_input.setStyleSheet("font-size: 18px; margin: 5px")
        recent_scan_list.addRow(sku_label, sku_input)

        wo_label = QtWidgets.QLabel("W/O: ")
        wo_label.setStyleSheet("font-size: 18px; margin-left: 20px;")
        wo_input = QtWidgets.QLineEdit()
        wo_input.setReadOnly(True)
        wo_input.setStyleSheet("font-size: 18px; margin: 5px")
        recent_scan_list.addRow(wo_label, wo_input)

        for label in input_labels:
            lbl = QtWidgets.QLabel(f"{label}: ")
            lbl.setStyleSheet("font-size: 18px; margin-left: 20px;")

            field = QtWidgets.QLineEdit()
            field.setReadOnly(True)
            field.setStyleSheet("font-size: 18px; margin: 5px")

            recent_scan_list.addRow(lbl, field)

            self.recent_inputs[label] = field  # store reference
        
        status_label = QtWidgets.QLabel("Status: ")
        status_label.setStyleSheet("font-size: 18px; margin-left: 20px;")
        status_input = QtWidgets.QLineEdit()
        status_input.setReadOnly(True)
        status_input.setStyleSheet("font-size: 18px; margin: 5px")
        recent_scan_list.addRow(status_label, status_input)

        timestamp_label = QtWidgets.QLabel("Timestamp: ")
        timestamp_label.setStyleSheet("font-size: 18px; margin-left: 20px;")
        timestamp_input = QtWidgets.QLineEdit()
        timestamp_input.setReadOnly(True)
        timestamp_input.setStyleSheet("font-size: 18px; margin: 5px")
        recent_scan_list.addRow(timestamp_label, timestamp_input)


        container = QtWidgets.QWidget()
        container.setLayout(recent_scan_list)
        container.setObjectName("list_container")
        container.setStyleSheet("""
            QWidget#list_container {
                border: 1px solid black;
                margin-left: 20px;
            }
        """)
        
        #recent_scan_layout.addWidget(recent_scan_title, alignment=QtCore.Qt.AlignLeft, stretch=1)
        recent_scan_layout.addWidget(container, stretch=10)

        content_layout.addLayout(prev_scan_layout, stretch=3)
        content_layout.addLayout(recent_scan_layout, stretch=2)

        # Add horizontal layout into main layout
        main_layout.addLayout(interactive_layout, stretch=1)
        main_layout.addWidget(content_container, stretch=5)
    
    def close_event(self, event):
        self.db.close_connection()
        event.accept()
        print("Database connection closed.")

    def handle_scan(self, status_bar, input_field, table):
        print("Scanned")
        
        validate_wip_number(input_field.text())
        print("Validation result:", validate_wip_number(input_field.text()))

        if validate_wip_number(input_field.text())[0] == True:
            status_bar.setText(f"PASS: {input_field.text()}")
            status_bar.setStyleSheet("font-size: 24px; color: white; background-color: green; border: 2px solid white; padding: 10px;")
            table.setItem(0, 0, QtWidgets.QTableWidgetItem(input_field.text()))
        else:
            status_bar.setText("FAILED: Invalid WIP")
            status_bar.setStyleSheet("font-size: 24px; color: white; background-color: red; border: 2px solid white; padding: 10px;")
        input_field.clear()

        QtCore.QTimer.singleShot(2000, lambda: self.reset_status_bar(status_bar))
    
    def refresh_current_scan(self, table):
        table.setItem(0, 0, QtWidgets.QTableWidgetItem(""))
    
    def reset_status_bar(self, status_bar):
        status_bar.setText(f"Please scan the WIP") 
        status_bar.setStyleSheet("font-size: 24px; color: black; background-color: lightgray; border: 2px solid white; padding: 10px;")
        



        
        

        

