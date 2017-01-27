from influxdb import InfluxDBClient
import requests
import datetime as datetime
import time as time
import csv

access_token = "a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0"

device_API = 'https://api.particle.io/v1/devices/?access_token=' + access_token

file_name = datetime.datetime.isoformat(datetime.datetime.now())
client = InfluxDBClient('localhost', 8086, 'jcoleman', 'four', 'particles')
# client.create_database(file_name)
# file_suffix = "_data_log.csv"

devices = []

collect_for = 60*5  # seconds
end = time.time() + collect_for

static_variables = ["location"]

header = ["Time", "Event", "Value", "ID", "Location"]

def device_api_call():
    devices_req = requests.get(device_API)
    devices_req_json = devices_req.json()
    return devices_req_json


def get_connected_devices():
    claimed_devices = device_api_call()

    connected_devices = []  # will contain connected Particle metadata

    for index, device in enumerate(claimed_devices):
        if device["connected"]:
            connected_devices.append(device)

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
        self.json = ""

        self.get_meta_data()
        # self.print_attributes()

    def print_attributes(self):
        print self.name
        print self.id
        print self.location
        print self.api
        if self.variables:
            print "Variables are: "
            for variable in self.variables:
                print "\t" + variable

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

    def influx_push(self,var,):
        json_body = [
            {
                "measurement": "cpu_load_short",
                "tags": {
                    "host": "server01",
                    "region": "us-west"
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "value": 0.64
                }
            }
        ]
        return json_body



def generate_device_obj():
    connected_devices = get_connected_devices()
    print "\n\nLooking up Particle data..."
    for index, connected_device in enumerate(connected_devices):
        devices.append( ConnectedDevice(connected_device["id"]) )
        print "Added data for " + devices[index].name
    print "Done!"


def write_vals_to_CSV():
    # generates file name
    starttime = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
    filename = starttime + file_suffix

    frequency = 0  # in seconds

    # CSV Stuff
    row = []

    with open(filename, "a") as file:
        print "Beginning collection for " + str(collect_for) + " seconds."
        writer = csv.writer(file, delimiter=",")
        writer.writerow(header)
        while True:
            # time.time() < end:
            time_str = str(datetime.datetime.isoformat(datetime.datetime.now()))
            for device in devices:
                for var in device.variables:
                        row.append(time_str)
                        print time_str + " ",
                        row.append(var)
                        print var + " ",
                        try:
                            row.append(device.return_a_variable(var))
                            print str(device.return_a_variable(var)) + " ",
                        except:
                            row.append(None)
                            print "ERROR ",
                        row.append(device.name)
                        print device.name + " ",
                        row.append(device.location)
                        print device.location + " "
                        writer.writerow(row)
                        row = []
                    # except requests.exceptions.ConnectionError:
                        writer.writerow(row)
    print "\ncompleted " + str(collect_for) + " seconds of collection."

devices = []
generate_device_obj()
write_vals_to_CSV()



