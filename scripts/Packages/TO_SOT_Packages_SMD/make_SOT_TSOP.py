#!/usr/bin/env python

# KicadModTree is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KicadModTree is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with kicad-footprint-generator. If not, see < http://www.gnu.org/licenses/ >.
#
# (C) 2016 by Thomas Pointhuber, <thomas.pointhuber@gmx.at>

import sys
import os
import argparse
import yaml
import pprint

sys.path.append(os.path.join(sys.path[0], "../../.."))  # enable package import from parent directory

#from KicadModTree import *  # NOQA


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', help='device type to build: TSOP  (default is all)',
                        type=str, nargs=1)
    parser.add_argument('-v', '--verbose', help='show extra information while generating the footprint',
                        action='store_true')
    return parser.parse_args()


if __name__ == '__main__':

    print('Building SOT/TSOP')

    from SOT_TSOP import ConfigDeserializer, FootprintSerializer

    CONFIG = './SOT_TSOP_config.yaml'
    args = get_args()

    config_deserializer = ConfigDeserializer()
    config_deserializer.deserialize(CONFIG, args)
    footprint_serializer = FootprintSerializer(config_deserializer.devices)
    footprint_serializer.serialize