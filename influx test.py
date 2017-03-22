import json
import requests
import sseclient
import time as time
import knowntypes as kt
import thermistor as therm
import datetime as datetime
from termcolor import colored
from influxdb import InfluxDBClient

# import credentials
import credentials as cd

usr = cd.usr
password = cd.passwd
db = 'test'  # cd.db
host = cd.host
port = cd.port
client = InfluxDBClient(host, port, usr, password, db)


def json_write(measurement, name, location, _time, _type, value):
    json2write = [
        {
            "measurement": measurement,
            "tags": {
                "name": name,
                'location': location
            },
            "time": _time,
            "fields": {
                _type: value,
            }
        }
    ]
    return json2write

stamp = datetime.datetime.utcnow().isoformat()
val = 0

while True:
    stamp = datetime.datetime.utcnow().isoformat()
    print time.time.iso(stamp)

    val = stamp - 10

    _json = json_write(
        'caal',
        'Neutron',
        'NewWave',
        stamp,
        'peace_frogs',
        val
    )
    client.write_points(_json)
    time.sleep(1)

