from influxdb import InfluxDBClient
import datetime as datetime
import time as time
import requests

# 100K ohm Thermistor Library
import thermistor as therm

# this imports a list of known measurement relationships
import knowntypes as kt

# this is to hide our credentials with a GIT IGNORE file
import credentials as cd

# Particle credentials
access_token = cd.access_token

# Influx credentials
usr = cd.usr
passwd = cd.passwd
db = cd.db
host = cd.host
port = cd.port
client = InfluxDBClient(host, port, usr, passwd, db)

# import known measurement types for influx
m = kt.Measurements()

#
particles = {}
connected_particles = {}
variables = []

#
good_particles = [
    '1c003c000347343339373536',
    '46002a000b51353335323535',
    '30004b000a51353335323536'
]

ignore_vars = [
    'location',
    'resistance'
]


class Particle:
    def __init__(self, _id, name, last_app, last_ip_address, last_heard, product_id, connected, platform_id,
                 cellular, status):
        # Particle defined attributes
        self.id = _id
        self.name = name
        self.last_app = last_app
        self.last_ip_address = last_ip_address
        self.last_heard = last_heard
        self.product_id = product_id
        self.connected = connected
        self.platform_id = platform_id
        self.cellular = cellular
        self.status = status
        self.current_build_target = None
        self.default_build_target = None

        # Chaos defined attributes
        self.location = ""
        self.api = "https://api.particle.io/v1/devices/" + self.id + "/?access_token=" + access_token
        self.variables = []


# deviceAPI
class DeviceAPI:
    def __init__(self):
        self.url = 'https://api.particle.io/v1/devices/?access_token=' + access_token

        self.devices_req = None
        self.devices_json = self.get_particles()
        self.claimed = 0

        self.update_particles()

    def get_particles(self):
        self.devices_req = requests.get(self.url)
        self.devices_json = self.devices_req.json()
        return self.devices_json

    def num_claimed(self):
        self.claimed = len(self.get_particles())
        return self.claimed

    def update_particles(self):
        for l in self.get_particles():
            particles[l['id']] = Particle(
                l['id'],
                l['name'],
                l['last_app'],
                l['last_ip_address'],
                l['last_heard'],
                l['product_id'],
                l['connected'],
                l['platform_id'],
                l['cellular'],
                l['status'],
                # Not all devices have this, uncommenting causes a KeyError
                # i['current_build_target'],
                # i['default_build_target'],
            )

    def connected_particles(self):
        if particles:
            self.update_particles()  # update the device statuses
            for l in particles:
                if particles[l].connected:
                    print particles[l].name
        else:
            self.update_particles()
            self.connected_particles()

d = DeviceAPI()

while True:
    for i in particles:
        p = particles[i]
        if p.connected:
            try:
                if p.id in good_particles:
                    current_time = time.time()
                    time_str = str(datetime.datetime.fromtimestamp(current_time))
                    print
                    print p.name
                    d_url = "https://api.particle.io/v1/devices/" + p.id + "?access_token=" + access_token
                    req = requests.get(d_url)
                    j = req.json()
                    # print j
                    # v_url = "https://api.particle.io/v1/devices/" + p.id + "/" + "" + "?access_token=" + access_token
                    # try:
                    for v in j['variables']:
                        if v not in ignore_vars:
                            # print v,
                            v_url = "https://api.particle.io/v1/devices/" + p.id + "/" + v + "?access_token=" + access_token
                            req = requests.get(v_url)
                            k = req.json()['result']
                            # print k
                            if m.return_measurement(v) == 'temp_resist':
                                k = therm.resist_to_celsius(k)
                            json_body = [
                                {
                                    "measurement": m.return_measurement(v),
                                    "tags": {
                                        "label": v,
                                        "name": p.name
                                    },
                                    "time": time_str,
                                    "fields": {
                                        "value": k,
                                    }
                                }
                            ]
                            print
                            print 'measurement',
                            print json_body[0]['measurement']
                            print 'label',
                            print json_body[0]['tags']['label']
                            print 'name',
                            print json_body[0]['tags']['name']
                            print 'time',
                            print json_body[0]['time']
                            print 'fields',
                            print json_body[0]['fields']['value']

                            # client.write_points(json_body)
            except:
                print 'API Error'


