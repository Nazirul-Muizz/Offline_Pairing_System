
fields = [
    {'label': 'WO Number', 'type': 'text', 'validator': 'wo_number'},
    {'label': 'WO Quantity', 'type': 'int', 'validator': 'wo_quantity'},
]

config = [
    {
        'project': '3146',
        'line': ['L1', 'L2', 'L3'],
        'station': ['MTRP', 'PUMP', 'PRPP'],
    },
    {
        'project': '3059',
        'line': ['L1', 'L2', 'L3'],
        'station': ['MTRP', 'PRPP'],
    },
    {
        'project': '2977',
        'line': ['L1'],
        'station': ['MTRP', 'PRPP'],
    },
    {
        'project': '2996',
        'line': ['L2'],
        'station': ['MTRP', 'PCBA', 'PUMP', 'PRPP'],
    },
    {
        'project': '3028',
        'line': ['L1'],
        'station': ['MTRP', 'PRPP'],
    },
    {
        'project': '3219',
        'line': ['L1'],
        'station': ['MTRP', 'PUMP', 'PRPP'],
    }

]

stations = {
    'MTRP': 'Motor_Pairing',
    'PUMP': 'Pump_Pairing',
    'PRPP': 'Carton_Pairing',
    #'PCBA': 'PCBA_Pairing'
}

