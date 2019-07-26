#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# Interface for ADS1115 16-bit I2C ADC

class ADS1115:

    def __init__(self, i2c, address=0x49, gain=0):
        # Modified to work in Wipy2.0
        self.i2c = i2c
        self.address = address
        self.gain = gain # 0 --> 2/3 6.144V

    def _write_register(self, register, value):
        data = ustruct.pack('>BH', register, value)
        self.i2c.writeto(self.address, data)

    def _read_register(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 2 )
        return ustruct.unpack('>h', data)[0]
