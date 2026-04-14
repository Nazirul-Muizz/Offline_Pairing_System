class MotorPairing:
    def __init__(self):
        super().__init__()
        wip_label = "WIP Serial Number"
        motor_sn_label = "Motor Serial Number"

        self.label_array = [wip_label, motor_sn_label]
    
    def load_previous_motor_scan(self):
        return