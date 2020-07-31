# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:29:43 2019

Transmission of a serial command with CRC-8 byte calculation 

@author: Adriano De Rosa
"""
import serial # Import pySerial for serial communication

ser = serial.Serial(None,
                    9600,
                    bytesize =  serial.EIGHTBITS,
                    parity =    serial.PARITY_EVEN,
                    stopbits =  serial.STOPBITS_ONE,
                    timeout =   0.05)

# Siehe auch https://crccalc.com/ als Tool zum Nachrechnen des Wertes

# CRC-8 calculation Maxim / Dallas

def Crc8(b, crc):
    b2 = b
    if (b < 0):
        b2 = b + 256
    for i in range(8):
        odd = ((b2^crc) & 1) == 1
        crc >>= 1
        b2 >>= 1
        if (odd):
            crc ^= 0x8C 
    return crc

# CalculateCrc calls Crc8 (Dallas/Maxim crc) for one byte 
# A list of hex numbers is passed as parameter  
def CalculateCrc(hex_liste):
    i=0
    crc_i = 0
    for i in hex_liste:
        print(hex(i))
        crc_i=Crc8(i,crc_i)
    return crc_i    
    
crc = 0  # Initialer Wert ist 0x00
wert=0x32 # Test wert für kalkulation von einem CRC wert für ein byte
#liste_mit_bytes = [0x01,0x01,0x01,0x01]  # Liste mit Werten aus denen eine CRC gerechnet werden soll

cmd_1_list  = [0x01,0x01,0x1F,0x29]  # Command to HVC to control the DC motors
 # crc8 = 0xD5, auch bestätigt über crc tool

#Berechnung eines einzelnen CRC wertes aus einem Byte
print("Dallas CRC für ein Byte mit dem Wert", hex(wert))
print("CRC-8 Hex-Wert", hex(Crc8(wert, crc)))
print("CRC-8 Dez-Wert", Crc8(wert, crc))

# Berechnung von einer CRC über eine Liste von Byte Werten
#print("\nBerechnung der CRC für eine Liste von Werten")
#print("Liste:", hex(CalculateCrc(liste_mit_bytes)))

cmd_crc=0
cmd_crc=CalculateCrc(cmd_1_list)

print("Command1a",cmd_1_list)
print("CRC von Command 1a=",hex(cmd_crc))
cmd_1_list.append(cmd_crc)
print("Command1a with CRC byte added",cmd_1_list)

# Serial Port Handling
ser.port='COM10'
ser.open()
# Write the command to the HVC, including CRC byte at the end 
ser.write(serial.to_bytes(cmd_1_list))
ser.close()

'''
// Meine C Implementierung für Dallas/Maxim CRC

char CRC8(char *data,int length) 
{
   char crc = 0x00;
   char extract;
   char sum;
	 int i;
	 char tempI;
	
   for(i=0;i<length;i++)
   {
      extract = *data;
      for (tempI = 8; tempI; tempI--) 
      {
         sum = (crc ^ extract) & 0x01;
         crc >>= 1;
         if (sum)
            crc ^= 0x8C;
         extract >>= 1;
      }
      data++;
   }
   return crc;
}

'''
