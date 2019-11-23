import sys
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../../.."))  # enable package import from parent directory

#from KicadModTree import *  # NOQA

class Variant(object):

    def __init__(self):
        self.pins = 6
        self.description_prefix = 'TSOP6'
        self.additional_keywords = 'TSOP6'
        self.datasheet = 'https://www.nxp.com/docs/en/package-information/SOT457.pdf'


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
        self.fab_x_mm = 1.7
        self.pin_distance_x_mm = 2.4
        self.pin_distance_y_mm = 0.95
        self.pin_width_x_mm = 0.7
        self.pin_width_y_mm = 0.55
        self.distance_from_last_pin_to_fab_y_mm = 0.5
        # Variant list from config_file
        self.variants = []

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

    def __deserialize_config(self, config, device_list):
        for device_config in config:
            if not device_list or device_config['base']['family'] in device_list or device_config['base']['series'] in device_list:
                device = Device()
                self.__deserialize_device(device, device_config)
                self.__deserialize_variants(device, device_config)
                self.devices.append(device)

    def __deserialize_device(self, device, device_config):
        base_config = device_config['base']
        device.series = base_config['series']
        device.description = base_config['description']
        device.keywords = base_config['keywords']
        device.fab_x_mm = base_config['fab_x_mm']
        device.pin_distance_x_mm = base_config['pin_distance_x_mm']
        device.pin_distance_y_mm = base_config['pin_distance_y_mm']
        device.pin_width_x_mm = base_config['pin_width_x_mm']
        device.pin_width_y_mm = base_config['pin_width_y_mm']
        device.distance_from_last_pin_to_fab_y_mm = base_config['distance_from_last_pin_to_fab_y_mm']

    def __deserialize_variants(self, device, device_config):
        for variant_config in device_config['variants']:
            variant = Variant()
            self.__deserialize_variant(variant, variant_config)
            device.variants.append(variant)

    def __deserialize_variant(self, variant, variant_config):
        variant.pins = variant_config['pins']
        variant.description_prefix = variant_config['description_prefix']
        variant.additional_keywords = variant_config['additional_keywords']
        variant.datasheet = variant_config['datasheet']
        try: variant.fab_x_mm = variant_config['fab_x_mm']
        except KeyError: variant.fab_x_mm = None


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