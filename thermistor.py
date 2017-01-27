import csv

# Reference values can be found at the below link:
# http://www.bapihvac.com/wp-content/uploads/2010/11/Thermistor_100K.pdf

index = []
input_vals = []


# will run once to get the array in python
def generate_lookup_index(array):
    with open("100k_ohm_thermistor.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            array.append((row[1], row[0]))
    return array
#  114 reference points


def linear_interpolate(resis_before, resis_after, temp_before, temp_after, resistance):
    resis_gap = resis_before - resis_after  # find delta resistance
    multiplier = (resis_before - resistance) / resis_gap
    temp_gap = temp_after - temp_before  # find delta temp.
    new_temp = temp_after - (multiplier * temp_gap)
    return new_temp


def interpolate_kelvin(resistance):
    # print("You entered: " + str(resistance) + " ohms")
    for counter, pair in enumerate(index):
        if resistance == int(pair[0]):  # if its greater than the resistance part of the tuple
            # print("The temp is")
            # print(pair[1])
            return pair[1]
        if resistance > int(pair[0]):
            interpolated_temp = linear_interpolate(float(pair[0]),float(index[counter-1][0]),float(index[counter-1][1]),float(pair[1]),resistance)

            return interpolated_temp


def resist_to_celsius(resist):
    celsius = float(interpolate_kelvin(resist)) - 273.15  # to convert to celsius
    # print("The temp in celsius is: " + str(celsius))
    return celsius


lookUp_index = generate_lookup_index(index)

# print("There are: " + str(len(index)) + " reference pairs. They are:\n")
# for val in index:
#     print(str(val[0]) + " " + str(val[1]))




