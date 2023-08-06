import csv
from collections import defaultdict
import re
import pprint
from operator import itemgetter
import argparse
import os
import copy
from collections import defaultdict
from .common import *
from .kipart import *

pp = pprint.PrettyPrinter(indent=4)

def parse_csv_file(csv_file):
    """Parses the CSV file and returns a list of pins in the form of (number, 'name')"""

    pins = []
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    next(reader, None) # skip header
    for row in reader:
        number, name, ptype, signal, label = row

        if label:
            name += '/' + label
        elif signal:
            name += '/' + signal

        name = name.replace(' ', '_')

        print("%s: %s" % (number, name))
        pins.append((number, name))

    return pins

def parse_portpin(name):
    """Finds the port name and number of a pin in a string. If found
    returns a tuple in the form of ('port_name', port_number).
    Otherwise returns `None`.
    """
    m = re.search('P([A-Z])(\d+)', name)
    if m:
        port_name, port_number = m.groups()
        return (port_name, int(port_number))

def group_pins(pins):
    """Groups pins together per their port name and functions. Returns a
    dictionary of {'port': [pin]}."""
    ports = defaultdict(list)

    power_names = ['VDD', 'VSS', 'VCAP', 'VBAT', 'VREF']
    config_names = ['OSC', 'NRST', 'SWCLK', 'SWDIO', 'BOOT']

    for pin in pins:
        number, name = pin
        if any(pn in name for pn in power_names):
            ports['power'].append(pin)

        elif any(pn in name for pn in config_names):
            ports['config'].append(pin)

        else:
            m = parse_portpin(name)
            if m:
                port_name, port_number = m
                ports[port_name].append(pin)
            else:
                ports['other'].append(pin)

    # sort pins
    for port in ports:
        # config and power gates are sorted according to their function name
        if port in ['config', 'power']:
            ports[port] = sorted(ports[port], key=itemgetter(1))
        # IO ports are sorted according to port number
        else:
            ports[port] = sorted(ports[port], key=lambda p: parse_portpin(p[1])[1])

    return ports

def stm32cube_reader(csv_file):
    print("Reading file %s..." % csv_file)
    pins = parse_csv_file(csv_file)
    print("File read. %d pins." % len(pins))

    ports = group_pins(pins)
    print("Pins are grouped as:")
    pp.pprint(ports)

    # create pin data
    pin_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    index = 0

    for port_name in ports:
        for p in ports[port_name]:
            # Get the pin attributes from the cells of the row of data.
            pin = copy.copy(DEFAULT_PIN) # Start off with default values for the pin.
            pin.index = index = index + 1
            pin.num = p[0]
            pin.name = p[1]
            pin.unit = port_name

            pin_data[pin.unit][pin.side][pin.name].append(pin)

    # use file name as the part name
    part_name = os.path.splitext(os.path.split(csv_file.name)[1])[0]

    # what should be the part_num?
    yield part_name, pin_data
