# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:29:43 2019
Transmission of a serial command with CRC-8 byte calculation 
@author: Adriano De Rosa
"""
import serial # Import pySerial for serial communication

ser = serial.Serial(None,9600,bytesize =  serial.EIGHTBITS,parity =    serial.PARITY_EVEN,stopbits =  serial.STOPBITS_ONE, timeout =   0.05)

# CRC-8 calculation Maxim / Dallas
def Crc8(b, crc):
    b2 = b
    if (b < 0): b2 = b + 256
    for i in range(8):
        odd = ((b2^crc) & 1) == 1
        crc >>= 1
        b2 >>= 1
        if (odd): crc ^= 0x8C 
    return crc

# CalculateCrc calls Crc8 (Dallas/Maxim crc) for one byte 
# A list of hex numbers is passed as parameter  
def CalculateCrc(hex_liste):
    i=0
    crc_i = 0
    for i in hex_liste: crc_i=Crc8(i,crc_i)
    return crc_i    
    
cmd_1_list  = [0x01,0x01,0x1F,0x29]  # Command to HVC to control the DC motors (w/o crc byte)
cmd_crc=CalculateCrc(cmd_1_list) # Calculate the CRC over the list of command bytes

print("cmd_1_list",cmd_1_list) # Print the command to the screen
print("CRC from cmd_1_list=",hex(cmd_crc)) # Print the CRC to the screen

cmd_1_list.append(cmd_crc) # Append the crc to the command
print("cmd_1_list with CRC byte added",cmd_1_list) # print the command with crc appended

ser.port='COM10'   # add your com port here
ser.open()# Open serial port 
ser.write(serial.to_bytes(cmd_1_list)) # Write the command to the HVC, including CRC byte at the end 
ser.close() # Close serial port
