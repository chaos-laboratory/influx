
import requests
import pandas as pd

access_token = 'a29cef4e07f57df80ddcc15fb5857e9fc5b98ce0'
# Particle device api stash
particle_url = 'https://api.particle.io/v1/devices?access_token=' + access_token
df = pd.read_csv('test.csv', sep='\t', index_col=0)
# sends GET request to our particle api
req = requests.get(particle_url)
# turns url into json
req_json = req.json()
d = pd.DataFrame(req_json)
# The d here can be further extracted for a status report on all devices if necessary.
d = d[d['connected'] == True]  # check if online, and record device name if online
print d

# Multiple Devices online:
for i in range(len(d['id'])):
    deviceMAC = str(d['id'].iloc[i])
    IP = d['last_ip_address'].iloc[i]
    NAME = d['name'].iloc[i]
    onDevice = requests.get('https://api.particle.io/v1/devices/' + deviceMAC + '?access_token=' + access_token)
    on_device = onDevice.json()
    loc = 'Unknown'
    for var in on_device['variables']:
        new = requests.get(
            'https://api.particle.io/v1/devices/' + deviceMAC + '/' + var + '?access_token=' + access_token).json()
        # data.append(new)
        # print new
        if new.get('name') == 'location':
            loc = new.get('result')
            continue
        variable = new.get('name')
        result = new.get('result')
        # ID = new.get('coreInfo').get('deviceID')
        # if variable.lower() in ['temperature','temp']:
        #         result = (result*9/5)+32
        # print str('on device: ' + NAME),str(', the ' + variable + ' is:'),str(result)#,'device info:',str(ID),str(IP)
        print variable, result, loc, NAME
        # should be able to use deviceID as tags to 'tag' the values.

        # print str(ID),str(variable),str(result)



# check = jsonbody(particle_url)
