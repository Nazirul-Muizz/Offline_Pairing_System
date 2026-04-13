
from backend.config_manager import CONFIG_PATH, ConfigManager


fields = [
    {'label': 'WO Number', 'type': 'text', 'validator': 'wo_number'},
    {'label': 'WO Quantity', 'type': 'int', 'validator': 'wo_quantity'},
]

config = [
    {
        'motor_pairing': {
            'motor_sn_prefix': '',
        },
        'pump_pairing': {
            'pump_sn_prefix': '',
        },
        'carton_pairing': {
            'carton_label_prefix': '',
            'ean_number': '',
        },
    }

]

config_manager = ConfigManager(CONFIG_PATH)

project = config_manager.config_data['project']
line = config_manager.config_data['line']
station = config_manager.config_data['station']

stations = {
    'MTRP': 'Motor_Pairing',
    'PUMP': 'Pump_Pairing',
    'PRPP': 'Carton_Pairing',
    #'PCBA': 'PCBA_Pairing'
}

password = "abc12345"



