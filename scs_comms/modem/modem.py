"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_comms.modem.at_command import ATCommand
from scs_comms.modem.ge910 import GE910
from scs_comms.modem.io import IO

from scs_host.lock.lock import Lock
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class Modem(object):
    """
    Modem with Telit GE910 and NXP PCA8574 remote 8-bit I/O expander
    """
    __PCA8574_ADDR =    0x38            # PCA8574: 0x30 + addr, PCA8574A: 0x38 + addr

    __LOCK_PWR =        "PWR"
    __LOCK_TIMEOUT =    60.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return cls.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, use_led):
        """
        Constructor
        """
        self.__use_led = use_led

        self.__ge910 = GE910()
        self.__io = IO(IO.filename(Host))


    # ----------------------------------------------------------------------------------------------------------------

    def switch_on(self):
        # lock...
        self.start_tx()

        print("vaux: %s" % self.__io.vaux)

        print("1: %s" % self.__io.state)

        # io...
        self.__io.power = IO.LOW
        self.__io.output_enable = IO.HIGH

        print("2: %s" % self.__io.state)

        time.sleep(2)

        # TODO: test pwmon

        print("vaux: %s" % self.__io.vaux)

        self.__ge910.setup_serial()

        self.__io.on_off = IO.LOW
        print("3: %s" % self.__io.state)

        time.sleep(6)

        # power...
        self.__io.on_off = IO.HIGH
        print("4: %s" % self.__io.state)

        time.sleep(1)

        # LED...
        if not self.__use_led:
            return

        print("setting LED...")
        cmd = ATCommand("AT#SLED=1", 1.0)
        self.execute(cmd)


    def switch_off(self):
        print("vaux: %s" % self.__io.vaux)

        print("1: %s" % self.__io.state)

        # on_off...
        self.__io.on_off = IO.LOW

        print("2: %s" % self.__io.state)

        time.sleep(4)

        self.__io.on_off = IO.HIGH

        print("3: %s" % self.__io.state)

        time.sleep(2)

        print("vaux: %s" % self.__io.vaux)

        # TODO: test pwmon

        self.__io.power = IO.HIGH

        print("4: %s" % self.__io.state)

        # GPIO...
        self.__serial = None

        # lock...
        self.__ge910.end_tx()
        self.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def execute(self, command):
        return self.__ge910.execute(command)


    # ----------------------------------------------------------------------------------------------------------------

    def start_tx(self):
        Lock.acquire(self.__lock_name(Modem.__LOCK_PWR), Modem.__LOCK_TIMEOUT, False)


    def end_tx(self):
        Lock.release(self.__lock_name(Modem.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    def is_on(self):
        return Lock.exists(self.__lock_name(Modem.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: use of the io expander


    # ----------------------------------------------------------------------------------------------------------------

    def pwmon(self):
        pass            #TODO: implement pwmon()

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Modem:{ge910:%s, io:%s}" % (self.__ge910, self.__io)