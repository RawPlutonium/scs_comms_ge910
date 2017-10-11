"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_comms.modem.pca8574 import PCA8574

from scs_host.lock.lock import Lock
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

class IO(object):
    """
    NXP PCA8574 remote 8-bit I/O expander
    """
    HIGH =                  True
    LOW =                   False

    ADDR =                  0x38

    __MASK_OUTPUT_ENABLE =  0x01            # 0000 0001
    __MASK_PWMON =          0x02            # 0000 0010
    __MASK_POWER =          0x04            # 0000 0100

    __MASK_ON_OFF =         0x08            # 0000 1000
    __MASK_HW_SHUTDOWN =    0x10            # 0001 0000

    __MASK_GPIO_03 =        0x20            # 0010 0000
    __MASK_GPIO_02 =        0x40            # 0100 0000

    __LOCK =                "MODEM_IO"
    __LOCK_TIMEOUT =        2.0

    __FILENAME =            "modem_io.json"


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def filename(cls):
        return Host.SCS_TMP + cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return cls.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__device = PCA8574.construct(IO.ADDR, self.filename())      # device is None if it can't be accessed


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def output_enable(self):                                    # active high
        return self.__get_output(IO.__MASK_OUTPUT_ENABLE)


    @output_enable.setter
    def output_enable(self, level):
        self.__set_output(IO.__MASK_OUTPUT_ENABLE, level)


    @property
    def power(self):                                            # active low
        return self.__get_output(IO.__MASK_POWER)


    @power.setter
    def power(self, level):
        self.__set_output(IO.__MASK_POWER, level)


    # ----------------------------------------------------------------------------------------------------------------
    # outputs...

    @property
    def on_off(self):                                           # active low (on is low)
        return self.__get_output(IO.__MASK_ON_OFF)


    @on_off.setter
    def on_off(self, level):
        self.__set_output(IO.__MASK_ON_OFF, level)


    @property
    def hw_shutdown(self):                                      # active low
        return self.__get_output(IO.__MASK_HW_SHUTDOWN)


    @hw_shutdown.setter
    def hw_shutdown(self, level):
        self.__set_output(IO.__MASK_HW_SHUTDOWN, level)


    # ----------------------------------------------------------------------------------------------------------------
    # inputs...

    @property
    def pwmon(self):                                            # active high
        return self.__get_input(IO.__MASK_PWMON)


    @property
    def gpio_02(self):                                          # not assigned
        return self.__get_input(IO.__MASK_GPIO_02)


    @property
    def gpio_03(self):                                          # not assigned
        return self.__get_input(IO.__MASK_GPIO_03)


    # ----------------------------------------------------------------------------------------------------------------

    def __get_input(self, mask):
        byte = self.__device.read()

        return bool(byte & mask)


    def __get_output(self, mask):
        if self.__device is None:
            return None

        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT)

        try:
            byte = self.__device.state.byte

            return bool(byte & mask)

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))


    def __set_output(self, mask, level):
        if self.__device is None:
            return

        Lock.acquire(IO.__lock_name(IO.__LOCK), IO.__LOCK_TIMEOUT)

        try:
            byte = self.__device.state.byte

            if level:
                byte |= mask
            else:
                byte &= ~mask

            self.__device.write(byte)
            self.__device.state = byte

        finally:
            Lock.release(IO.__lock_name(IO.__LOCK))



    # ----------------------------------------------------------------------------------------------------------------

    @property
    def state(self):
        if self.__device is None:
            return None

        return self.__device.state


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "IO:{device:%s}" % self.__device
