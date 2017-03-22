from influxdb import InfluxDBClient
from pylab import *
from datetime import datetime
import pytz
import credentials as cd

# use local InfluxDB credentials
usr = cd.usr
password = cd.passwd
db = 'siemens'  # cd.db
measurement = 'siemens'
host = cd.host
port = cd.port
client = InfluxDBClient(host, port, usr, password, db)

# load file
a = []  # this holds the files data
f = open('B70.MARIA.CSV', 'r')
for line_num, line in enumerate(f):
    a.append(line)
f.close()

# set up timezones
utc = pytz.utc
eastern = pytz.timezone('US/Eastern')
fmt = '%Y-%m-%dT%H:%M:%S.0000000Z'  # in nano seconds


# This is to put data in the correct format
def json_write(measurement, name, location, _time, value):
    json2write = [
        {
            "measurement": measurement,
            "tags": {
                'name': name,
                'location': location
            },
            "time": _time,
            "fields": {
                "value": value,
            }
        }
    ]
    return json2write


# checks for number-ness
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# handling data types
def siemens_value(raw_value, measure='Unknown Measurement'):
    val_map = {
        'ON': 1.0,
        'OFF': 0.0
    }
    if is_number(raw_value):
        result = float(raw_value)
        return result
    else:
        if raw_value in val_map:
            result = val_map[raw_value]
            return result
        else:
            print 'ERROR, unknown reading from  ' + measure


# a little list comprehension for cleaning the file
clean_file = [line[:-2] for line in a if len(line) > 3]  # Removes unwanted chars and lines
label = ''  # active variable
location = ''  # active location

# Generate JSON strings from each line measurements
for l in clean_file:
    # IF new variable: update the label variable and location
    if len(l) > 0 and l.split()[0] == "Point":
        tags = l.split()[2].split(".")
        location = tags[0]
        label = ''.join(tags[1:])
    # IF data line is found... create JSON
    if len(l) == 54:
        # SPLIT input string
        y = l.split()
        value = siemens_value(y[2], label)  # modify the value to the correct type

        # data and time
        d = y[0].split('/')
        d = map(int, d)
        t = y[1].split(":")
        t = map(int, t)
        loc_dt = eastern.localize(datetime(d[2], d[0], d[1], t[0], t[1], t[2]))

        # generate JSON, ADD to Influxdb
        entry = json_write(measurement, label, location, loc_dt, value)
        client.write_points(entry)
