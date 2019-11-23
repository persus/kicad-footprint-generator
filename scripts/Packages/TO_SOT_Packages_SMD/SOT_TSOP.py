import sys
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../../.."))  # enable package import from parent directory

#from KicadModTree import *  # NOQA

class Variant(object):

    def __init__(self, variant):
        self.pins = 6
        self.description_prefix = 'SOT-457T'
        self.additional_keywords = 'SOT-457T'
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
        self.varaints = []

class ConfigDeserializer(object):

    def __init__(self):
        self.devices = []

    def deserialize(self, config_file, device_list):
        config = self.load_config(config_file)
        self.deserialize_config(config, device_list)

    def load_config(self, config_file):
        try:
            my_config = yaml.safe_load_all(open(config_file))
            return my_config
        except FileNotFoundError as fnfe:
            print(fnfe)
            return None

    def deserialize_config(self, config, device_list):
        for device_config in config:
            if not device_list or device_config['base']['family'] in device_list or device_config['base']['series'] in device_list:
                device = Device()
                self.deserialize_device(device, device_config)
                self.deserialize_variants(device, device_config)
                self.devices.append(device)

    def deserialize_device(self, device, device_config):
        base = device_config['base']
        device.description = base['description']
        device.keywords = base['keywords']
        device.fab_x_mm = base['fab_x_mm']
        device.pin_distance_x_mm = base['pin_distance_x_mm']
        device.pin_distance_y_mm = base['pin_distance_y_mm']
        device.pin_width_x_mm = base['pin_width_x_mm']
        device.pin_width_y_mm = base['pin_width_y_mm']
        device.distance_from_last_pin_to_fab_y_mm = base['distance_from_last_pin_to_fab_y_mm']

    def deserialize_variants(self, device, device_config):
        for variant_config in device_config['base']['variants']:
            variant = Variant
            self.deserialize_variant(variant, variant_config)
            device.variants.append(variant)

    def deserialize_variant(self, variant, variant_config):
        variant.pins = variant['pins']
        variant.description_prefix = variant['description_prefix']
        variant.additional_keywords = variant['additional_keywords']
        variant.datasheet = variant['datasheet']


class FootprintSerializer(object):

    def __init__(self, devices):
        self.devices = devices

    def serialize(self):
        for device in self.devices:
            print(device.series)


if __name__ == '__main__':

    print('Building SOT/TSOP')

    from SOT_TSOP import ConfigDeserializer, FootprintSerializer

    CONFIG = './SOT_TSOP_config.yaml'
    args = []

    config_deserializer = ConfigDeserializer()
    config_deserializer.deserialize(CONFIG, args)
    footprint_serializer = FootprintSerializer(config_deserializer.devices)
    footprint_serializer.serialize