import requests

# make sure this is current
access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'

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
        self.current_build_target = None
        self.default_build_target = None

        # Chaos defined attributes
        self.location = ""
        self.api = "https://api.particle.io/v1/devices/" + self.id + "/?access_token=" + access_token
        self.variables = []


class DeviceAPI:
    def __init__(self):
        self.url = 'https://api.particle.io/v1/devices/?access_token=' + access_token

        self.devices_req = None
        self.devices_json = self.get_particles()
        self.claimed = 0

        self.get_particles()

    def get_particles(self):
        self.devices_req = requests.get(self.url)
        self.devices_json = self.devices_req.json()
        return self.devices_json

    def num_claimed(self):
        self.claimed = len(self.get_particles())
        return self.claimed

    def create_particles(self):
        for i in self.get_particles():
            particles[i['id']] = Particle(
                i['id'],
                i['name'],
                i['last_app'],
                i['last_ip_address'],
                i['last_heard'],
                i['product_id'],
                i['connected'],
                i['platform_id'],
                i['cellular'],
                i['status'],
                # Not all devices have this, uncommenting causes a KeyError
                # i['current_build_target'],
                # i['default_build_target'],
            )

    def connected_particles(self):
        self.devices_json = self.get_particles()  # update the device statuses
        self.device



