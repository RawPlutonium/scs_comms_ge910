#!/usr/bin/env python3

"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_comms.modem.at_command import ATCommand
from scs_comms.modem.modem import Modem

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

print("modem...")
modem = Modem()
print(modem)
print("-")

command = ATCommand.construct("")

try:
    print("on...")
    modem.switch_on()

    modem.setup_serial()

    print(modem)
    print("-")

    print("cmd...")

    while True:
        print("> ", end="")
        sys.stdout.flush()

        text = sys.stdin.readline().strip()
        sys.stdin.flush()

        if len(text) > 0:
            command = ATCommand.construct(text)     # use previous command on empty text

        command_start_time = time.time()
        response = modem.execute(command)
        print(response)
        print("-")

        command_time = time.time() - command_start_time
        print("cmd time: %6.3f" % command_time)
        print("")

except KeyboardInterrupt:
    print("modem_test: KeyboardInterrupt", file=sys.stderr)

finally:
    print("off...")
    modem.switch_off()
    print(modem)
    print("-")

    I2C.close()
