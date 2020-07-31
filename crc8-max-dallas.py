# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:29:43 2019

"""

#!/usr/bin/python

import binascii

def AddToCRC(b, crc):
    b2 = b
    if (b < 0):
        b2 = b + 256
    for i in range(8):
        odd = ((b2^crc) & 1) == 1
        crc >>= 1
        b2 >>= 1
        if (odd):
            crc ^= 0x8C # this means crc ^= 140
    return crc


print(hex(AddToCRC(1, 0)))
