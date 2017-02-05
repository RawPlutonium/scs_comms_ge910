#!/usr/bin/env python3

"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_comms.modem.pca8574 import PCA8574

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    io = PCA8574(0x38)
    print(io)

    byte = io.read()
    print("byte:%02x" % byte)


    io.write(0xe7)

    byte = io.read()
    print("byte:%02x" % byte)

except KeyboardInterrupt:
    print("pca8574_test: terminated", file=sys.stderr)

finally:
    I2C.close()
