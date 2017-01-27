class Measurements:
    def __init__(self):
        self.known_pairs = {
            "temp_c": [
                "object",
                "ambient"
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
                "ldrVal",
                "ldrVal2"
            ]

        }
    def get_measurements(self):
        for measure in self.known_pairs:
            print measure

    def get_inputs(self):
        for measure in self.known_pairs:
            for _input in self.known_pairs[measure]:
                print _input
