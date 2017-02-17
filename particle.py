import requests
from termcolor import colored


# All credentials are stored in a GIT IGNORED file
import credentials as cd

# make sure this is current
access_token = cd.access_token

# will hold all registered particles
particles = {}


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

        # Particles APIs
        self.api = "https://api.particle.io/v1/devices/" + self.id + "/?access_token=" + access_token
        self.var_api = 'https://api.particle.io/v1/devices/' + self.id + '/?access_token=' + access_token
        self.result_api = ''

        # Chaos defined attributes
        self.has_location = False
        self.location = "unknown"
        self.var_req = None
        self.var_json = None
        self.variables = []
        self.current_var = None

        # Gather more data if device is connected
        if self.connected:
            try:
                self.get_variables()
            except:
                self.connected = False
                print self.name + ' is now offline.'

    def generate_result_url(self):
        self.result_api = 'https://api.particle.io/v1/devices/' + self.id + '/' + self.current_var +'/?access_token=' + access_token
        return self.result_api

    def get_variables(self):
        try:
            self.var_req = requests.get(self.var_api)
            self.var_json = self.var_req.json()['variables']
            self.variables = [v for v in self.var_json]
            if 'location' in self.variables:
                self.has_location = True
                self.location = 'known'
                self.variables = [v for v in self.variables if v != 'location']
                print '\n' + colored(self.name, 'red')
                print 'finding location...'
                try:
                    self.current_var = 'location'
                    self.generate_result_url()
                    self.var_req = requests.get(self.result_api)
                    self.var_json = self.var_req.json()
                    self.location = self.var_json['result']
                    print 'Current device\'s location is: ',
                    print colored(self.location, 'green')
                except:
                    print 'Error retrieving location'
            print 'It\'s ' + colored('variables', 'green') + ' are: '
            for v in self.variables:
                print v
        except KeyError:
            print 'This particles has no variables'


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
            )

    def connected_particles(self):
        if particles:
            self.update_particles()  # update the device statuses

        else:
            self.update_particles()
            self.connected_particles()

d = DeviceAPI()
d.connected_particles()
