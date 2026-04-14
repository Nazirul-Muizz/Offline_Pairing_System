

class PumpPairing:
    def __init__(self):
        super().__init__()
        wip_label = "WIP Serial Number"
        pump_sn_label = "Pump Serial Number"

        self.label_array = [wip_label, pump_sn_label]

    def load_previous_pump_scan(self):
        return