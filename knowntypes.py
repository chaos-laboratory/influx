class Measurements:
    def __init__(self):
        self.known_pairs = {
            "temp_c": [
                "Tank",
                "Ambient"
            ],
            "temp_resist": [
                "condReturn",
                "condSupply",
                "tnkSupply",
                "tnkReturn"
            ],
            "vol": [
                "micVol"
            ],
            "photo_resist": [
                "Pump1",
                "Pump2"
            ],
            "threshold": [
             "threshold_broken"
            ]
        }

    def get_measurements(self):
        for measure in self.known_pairs:
            print measure

    def get_inputs(self):
        for measure in self.known_pairs:
            for _input in self.known_pairs[measure]:
                print _input

    def return_measurement(self, var):
        for measure in self.known_pairs:
            if var in self.known_pairs[measure]:
                return measure
        return "unknown"
