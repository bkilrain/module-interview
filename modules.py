import csv
import math
import decimal
D = decimal.Decimal

Q = 1.60217657e-19
K = 1.3806488e-23
ZERO_CELSIUS = 273.  # zero celsius, in Kelvin (be careful about units)


def calculate_module_current(name, irradiance, temperature, voltage):

    # Module Variables
    module = get_parameters(name)
    rs = module['r_series']
    temp_i0 = module['temp_i0']
    i0 = module['i0']
    i_sc = module['i_sc']
    gamma = module['gamma']
    r_series = module['r_series']
    r_parallel = module['r_parallel']
    temperature = temperature + ZERO_CELSIUS

    temp_adjust = i0 * (1.0 + temp_i0) ** (temperature - 298)
    
    # initialize diode and calculate 
    current = i_sc
    diode = voltage + i_sc * r_series
    e_exponent = Q / (K * temperature * gamma) * diode
    current = (i_sc * irradiance / 1000.0) - (temp_adjust * ((math.e ** e_exponent) - 1.0)) - (diode / r_parallel)
    voltage_check = diode - current * r_series


    # if calculations are off (within a certain amount of precision)... adjust diode and re-calculate
    while (round(voltage_check, 10) != round(voltage, 10)):
        # print(voltage_check, voltage)
        volt_diff = voltage_check - voltage
        diode -= volt_diff
        e_exponent = Q / (K * temperature * gamma) * diode
        current = (i_sc * irradiance / 1000.0) - (temp_adjust * ((math.e ** e_exponent) - 1.0)) - (diode / r_parallel)
        voltage_check = diode - current * r_series
    return current


def calculate_max_power_point(name, irradiance, temperature):

    # init voltage and current
    voltage = 1.0
    current = calculate_module_current(name, irradiance, temperature, voltage)
    power = voltage * current
    previous_power = 0
    incrementor = 1

    # increment voltage until calculated power is reduced 
    # then step back in voltage and divide incrementor by 10
    while incrementor > 1e-13:
        previous_power = power
        voltage += incrementor
        current = calculate_module_current(name, irradiance, temperature, voltage)
        power = voltage * current
        if previous_power > power:
            voltage -= incrementor * 2
            incrementor *= 0.1
            current = calculate_module_current(name, irradiance, temperature, voltage)
            power = voltage * current
    return (voltage, current)


def read_csv(filename, field_names):
    """load a structured csv file

    Arguments:
        filename {str} -- the path to the file to be loaded
        field_names {List} -- an array of field names in the order of the
                              columns in the csv
    Returns:
        [type] -- [description]
    """
    rtn = []
    with open(filename) as f:
        reader = csv.DictReader(f, fieldnames=field_names)
        reader.next()
        for row in reader:
            rtn.append(row)

    return rtn


def convert_entry_to_float(val):
    try:
        return float(val)
    except ValueError:
        return val


def get_parameters(name):
    """get the parameters for a solar module

    Arguments:
        name {str} -- the name of the module you'd like to load
    Returns:
        [dictionary] -- the parameters of the modules
    """
    field_names = ['manufacturer', 'name', 'power', 'i_sc', 'gamma', 'i0',
                   'r_series', 'r_parallel', 'temp_i0']

    all_parameters = read_csv('data.csv', field_names)
    panel = next(x for x in all_parameters if x['name'] == name)

    return {
        key: convert_entry_to_float(val) for key, val in panel.items()
    }

if __name__ == '__main__':
    import pprint
    pprint.pprint(get_parameters('TSM PA05'))
    # print(calculate_module_current('TSM PA05', 1000, 25, 30.400000000001004 - 1e-5) * 30.400000000001004 - 1e-5)
    print(calculate_max_power_point('TSM PA05', 1000, 25))