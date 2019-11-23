import sys
import os
import argparse
import yaml
import pprint
import copy

sys.path.append(os.path.join(sys.path[0], "../../.."))  # enable package import from parent directory

#from KicadModTree import *  # NOQA

class Device(object):

    def __init__(self):
        # From KLC
        self.fab_line_width_mm = 0.1
        self.silk_line_width_mm = 0.12
        self.courtyard_line_width_mm = 0.05
        self.courtyard_clearance_mm = 0.25
        self.courtyard_precision_mm = 0.01
        # Base properties from config_file
        self.family = 'TSOP'
        self.series = 'TSOP'
        self.name = 'TSOP'
        self.description = 'TSOP SMD package'
        self.keywords = 'TSOP'
        self.fab_x_mm = 0
        self.pin_distance_x_mm = 0
        self.pin_distance_y_mm = 0
        self.pin_width_x_mm = 0
        self.pin_width_y_mm = 0
        self.distance_from_last_pin_to_fab_y_mm = 0
        # Variant properties from config_file
        self.pins = 0
        self.description_prefix = 'TSOP6'
        self.additional_keywords = 'TSOP6'
        self.datasheet = 'https://www.nxp.com/docs/en/package-information/SOT457.pdf'

class ConfigDeserializer(object):

    def __init__(self):
        self.devices = []

    def deserialize(self, config_file, device_list):
        config = self.__load_config(config_file)
        self.__deserialize_config(config, device_list)

    def __load_config(self, config_file):
        try:
            my_config = yaml.safe_load_all(open(config_file))
            return my_config
        except FileNotFoundError as fnfe:
            print(fnfe)
            return None

    def __deserialize_single_value(self, device_config, value_key, default_value):
        try: return device_config[value_key]
        except KeyError: return default_value

    def __deserialize_config(self, config, device_list):
        for device_config in config:
            if not device_list or device_config['base']['family'] in device_list or device_config['base']['series'] in device_list:
                device = Device()
                self.__deserialize_device(device, device_config['base'])
                self.__deserialize_variants(device, device_config)

    def __deserialize_device(self, device, device_config):
        # Base properties
        device.series = self.__deserialize_single_value(device_config, 'series', device.series)
        device.description = self.__deserialize_single_value(device_config, 'description', device.description)
        device.keywords = self.__deserialize_single_value(device_config, 'keywords', device.keywords)
        device.fab_x_mm = self.__deserialize_single_value(device_config, 'fab_x, mm', device.fab_x_mm)
        device.pin_distance_x_mm = self.__deserialize_single_value(device_config, 'pin_distance_x_mm', device.pin_distance_x_mm)
        device.pin_distance_y_mm = self.__deserialize_single_value(device_config, 'pin_distance_y_mm', device.pin_distance_y_mm)
        device.pin_width_x_mm = self.__deserialize_single_value(device_config, 'pin_width_x_mm', device.pin_width_x_mm)
        device.pin_width_y_mm = self.__deserialize_single_value(device_config, 'pin_width_y_mm', device.pin_width_y_mm)
        device.distance_from_last_pin_to_fab_y_mm = self.__deserialize_single_value(device_config, 'distance_from_last_pin_to_fab_y_mm', device.distance_from_last_pin_to_fab_y_mm)
        # Variant properties
        device.pins = self.__deserialize_single_value(device_config, 'pins', device.pins)
        device.description_prefix = self.__deserialize_single_value(device_config, 'description_prefix', device.description_prefix)
        device.additional_keywords = self.__deserialize_single_value(device_config, 'additional_keywords', device.additional_keywords)
        device.datasheet = self.__deserialize_single_value(device_config, 'datasheet', device.datasheet)

    def __deserialize_variants(self, device, device_config):
        for variant_config in device_config['variants']:
            device_copy = copy.copy(device)
            self.__deserialize_variant(device_copy, variant_config)
            self.devices.append(device_copy)

    def __deserialize_variant(self, variant, variant_config):
        self.__deserialize_device(variant, variant_config)


class Footprint(object):

    def __init__(self):
        self.pins = [(0, 0)]
        self.fabric = (0, 0)


class FootprintBuilder(object):

    def __init__(self):
        self.footprints = []


class FootprintSerializer(object):

    def __init__(self, devices):
        self.devices = devices

    def serialize(self):
        for device in self.devices:
            print(device.series)


if __name__ == '__main__':

    print('Building SOT/TSOP')

    #from SOT_TSOP import ConfigDeserializer, FootprintSerializer

    CONFIG = 'SOT_TSOP_config.yaml'
    args = []

    config_deserializer = ConfigDeserializer()
    config_deserializer.deserialize(CONFIG, args)
    footprint_serializer = FootprintSerializer(config_deserializer.devices)
    footprint_serializer.serialize()