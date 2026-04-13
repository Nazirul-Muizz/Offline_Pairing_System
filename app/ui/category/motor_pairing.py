#from ...backend.main_validation import validate_wip_number

class MotorPairing:
    def __init__(self):
        super().__init__()
        self.input_labels = ["WIP Serial Number", "Motor Serial Number"]
    
    def load_previous_motor_scan(self):
        return