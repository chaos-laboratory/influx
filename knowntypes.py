from termcolor import colored


class Measurements:
    def __init__(self):
        self.known_pairs = {
            "temp_c": [
                "tank",
                "ambient",
                "temperature",
                "_temperature",
                'temp_c',
                'temp',
                "condreturn",
                "condsupply",
                "tanksupply",
                "tankreturn"
            ],
            'humidity': [
                'humidity'
            ],
            "vol": [
                "micvol"
            ],
            "photo_resist": [
                "pump1",
                "pump2",
                'light1',
                'light2',
            ],
            "threshold": [
             "threshold_broken"
            ],
            "location": [
                "location"
            ],
            'rate': [
                'rate'
            ],
            'resistance': [
                'resistance'
            ],
            'ppm': [
                'co2'
            ],
            'calibration': [
                'calibrate_1',
                'calibrate_2',
                'calibrate_3',
                'calibrate_4',
                'calibrate_5',
                'calibrate_6',
                'calibrate_7',
                'calibrate_8',
            ]
        }

    def get_measurements(self):
        for measure in self.known_pairs:
            print measure

    def get_inputs(self):
        for measure in self.known_pairs:
            for _input in self.known_pairs[measure]:
                print _input

    def return_measurement(self, label):
        for measure in self.known_pairs:
            # print '\n' + colored(measure, 'red')
            # for i in self.known_pairs[measure]:
            #     # print i,
            #     if i == label:
            #         # print colored('FOUND', 'green'),
            #     # else:
            #     #     print
            # print self.known_pairs[measure],
            if label.lower() in self.known_pairs[measure]:
                # print colored('FOUND', 'green')
                # print label.lower()
                return measure
        return 'unknown'


# m = Measurements()
# m.return_measurement('TankSupply')
