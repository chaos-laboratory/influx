from influxdb import InfluxDBClient
import sseclient
import requests
import datetime as datetime
import time as time
from pytz import timezone
import pytz
import json

import credentials as cd

# Particle creds
access_token = cd.access_token

# Influx creds
usr = ''
passwd = ''
db = 'particles'
influx = InfluxDBClient('localhost', 8086, usr, passwd, db)

# SSE
url = 'https://api.particle.io/v1/events/threshold?access_token=a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'
client = sseclient.SSEClient(url)

measure = "door"

devices = {
    "2a0060000a51353335323535": "Door 1",
    "2a0032000547343233323032": "Door 2"
}


def make_json(name, _time):
    json_body = [
        {
            "measurement": measure,
            "tags": {
                # "label": var,
                # "location": self.location,
                "name": name
            },
            "time": _time,
            "fields": {
                "value": 1
            }
        }
    ]
    return json_body


def influx_push():
    current_time = time.time()
    print current_time
    print "Beginning Data Collection.\nThe time is:  ",
    t = datetime.datetime.isoformat(datetime.datetime.fromtimestamp(current_time))
    print t

    for event in client:
        current_time = time.time()
        t = str(datetime.datetime.fromtimestamp(current_time))
        if event.event != 'message':
            j = json.loads(event.data)
            x = make_json(devices[j["coreid"]], t)
            influx.write_points(x)
            print event.event, devices[j["coreid"]]

influx_push()