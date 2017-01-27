from influxdb import InfluxDBClient
import requests
import datetime as datetime
import time as time
import knowntypes
import thermistor

access_token = "a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0"

device_API = 'https://api.particle.io/v1/devices/?access_token=' + access_token

file_name = datetime.datetime.isoformat(datetime.datetime.now())

# influx creds
usr = 'jcoleman'
passwd = 'four'
db = 'particles'
client = InfluxDBClient('localhost', 8086, usr, passwd, db)

# this is used to get the correct series to publish to
get_measurements = knowntypes.Measurements()
# client.create_database(file_name)
# end influx stuff

devices = []
connected_devices = []

collect_for = 10  # seconds

static_variables = ["location"]

header = ["Time", "Event", "Value", "ID", "Location"]

def device_api_call():
    devices_req = requests.get(device_API)
    devices_req_json = devices_req.json()
    return devices_req_json


def get_connected_devices():
    claimed_devices = device_api_call()
    connected_devices = [device for device in claimed_devices if device["connected"]]

    return connected_devices


def truncate_strings(_strings, cut_mark):
    truncated_strings = [string[cut_mark:] for string in _strings]
    return truncated_strings


def strings_to_ints(_list):
    _list = [int(item) for item in _list]
    return _list


def json_sort(_list, _key):
    # this function will sort a list of JSON using values of one key
    keys = [item[_key] for item in _list]
    keys = truncate_strings(keys, 8)
    keys = strings_to_ints(keys)
    keys, _list = (list(t) for t in zip(*sorted(zip(keys, _list))))

    return _list


class ConnectedDevice:
    def __init__(self, unique_id):
        self.id = unique_id
        self.location = ""
        self.name = ""
        self.api = "https://api.particle.io/v1/devices/" + self.id + "/?access_token=" + access_token
        self.variables = []
        self.val = None
        self.json = ""

        self.get_meta_data()
        self.measure = ""
        # self.print_attributes()

    def url_json(self, url):
        req = requests.get(url)
        req_json = req.json()
        return req_json

    def generate_var_url(self, var):
        self.var_url = "https://api.particle.io/v1/devices/" + self.id + "/" + var + "?access_token=" + access_token
        return self.var_url

    def get_location(self):
        self.location_url = self.generate_var_url("location")
        self.location_json = self.url_json(self.location_url)
        return self.location_json["result"]

    def get_meta_data(self):
        self.json = self.url_json(self.api)
        self.name = self.json["name"]
        if self.json["variables"]:
            for variable in self.json["variables"]:
                self.variables.append(variable)
            if "location" in self.variables:
                self.location = self.get_location()
                self.variables.remove("location")
            else:
                self.location = "unknown"
        else: self.location = "unknown"

    def return_a_variable(self, var):
        self.url_to_check = self.generate_var_url(var)
        self.result = self.url_json(self.url_to_check)
        self.result = self.result["result"]
        return self.result

    def influx_push(self, var, curr_time):
        self.measure = get_measurements.return_measurement(var)
        self.val = self.return_a_variable(var)
        if self.measure == "temp_resist":
            self.val = thermistor.resist_to_celsius(float(self.val))
            self.measure = "temp_c"
        json_body = [
            {
                "measurement": self.measure,
                "tags": {
                    "label": var,
                    "location": self.location,
                    "name": self.name
                },
                "time": curr_time,
                "fields": {
                    "value": self.val
                }
            }
        ]
        client.write_points(json_body)


def generate_device_obj():
    connected_devices = get_connected_devices()
    print "\n\nLooking up Particle data..."
    for index, connected_device in enumerate(connected_devices):
        devices.append(ConnectedDevice(connected_device["id"]))
        print "Added data for " + devices[index].name
    print "Done!\n"

devices = []
generate_device_obj()


def influx_push():
    current_time = time.time()
    print current_time
    end = current_time + collect_for
    print "Beginning Data Collection.\nThe time is:  ",
    print datetime.datetime.isoformat(datetime.datetime.fromtimestamp(current_time))
    while current_time < end:
        current_time = time.time()
        time_str = str(datetime.datetime.fromtimestamp(current_time))
        # print "The time is " + time_str
        for device in devices:
            for var in device.variables:
                try:
                    device.influx_push(var, time_str)
                except:
                    pass

    print "\ncompleted " + str(collect_for) + " seconds of collection."

influx_push()
