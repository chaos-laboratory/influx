from influxdb import InfluxDBClient
import sseclient
import requests
import datetime as datetime
import time as time
import knowntypes
import thermistor
import particle

# All credentials are stored in a GIT IGNORED file
import credentials as cd

# Particle creds
access_token = cd.access_token

device_API = 'https://api.particle.io/v1/devices/?access_token=' + access_token

# Influx creds
usr = ''
passwd = ''
db = 'particles'
client = InfluxDBClient('localhost', 8086, usr, passwd, db)

devices = []
connected_devices = []

collect_for = 10*60  # seconds


def get_connected_devices():
    claimed_devices = device_api_call()
    _connected_devices = [device for device in claimed_devices if device["connected"]]

    return _connected_devices


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
        self.var_url = ""
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
        else:
            self.location = "unknown"

    def return_a_variable(self, var):
        self.url_to_check = self.generate_var_url(var)
        self.result = self.url_json(self.url_to_check)
        self.result = self.result["result"]
        return self.result

    def influx_push(self, var, curr_time):
        self.measure = knowntypes.get_measurements.return_measurement(var)
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
        return json_body
        # client.write_points(json_body)


def generate_device_obj():
    _connected_devices = get_connected_devices()
    print "\n\nLooking up Particle data..."
    for index, connected_device in enumerate(_connected_devices):
        devices.append(ConnectedDevice(connected_device["id"]))
        print "Added data for " + devices[index].name
    print "Done!\n"


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

devices = []
generate_device_obj()
influx_push()
