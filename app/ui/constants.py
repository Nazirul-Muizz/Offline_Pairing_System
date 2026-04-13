
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

stations = {
    'MTRP': 'Motor_Pairing',
    'PUMP': 'Pump_Pairing',
    'PRPP': 'Carton_Pairing',
    #'PCBA': 'PCBA_Pairing'
}

password = "abc12345"



