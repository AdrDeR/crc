# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 09:29:43 2019

CRC Berechnung 

"""

# Implementierung einer CRC-8 Berechnung nach Maxim / Dallas
# Siehe auch https://crccalc.com/ als Tool zum Nachrechnen des Wertes

def Crc8(b, crc):
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

# CalculateCrc ruft DallasCrc für ein byte auf
# Eine Liste von Hex zahlen wird übergeben 
def CalculateCrc(hex_liste):
    i=0
    crc_i = 0
    for i in hex_liste:
        print(hex(i))
        crc_i=Crc8(i,crc_i)
    return crc_i    
    
    
crc = 0  # Initialer Wert ist 0x00
wert=0x32 # Test wert für kalkulation von einem CRC wert für ein byte
liste_mit_bytes=[0x01,0x01,0x01,0x01]  # Liste mit Werten aus denen eine CRC gerechnet werden soll


#Berechnung eines einzelnen CRC wertes ais einem Byte
print("Dallas CRC für ein Byte mit dem Wert", hex(wert))
print("CRC-8 Hex-Wert", hex(Crc8(wert, crc)))
print("CRC-8 Dez-Wert", Crc8(wert, crc))

# Berechnung von einer CRC über eine Liste von Byte Werten
print("\nBerechnung der CRC für eine Liste von Werten")
print("Liste:", hex(CalculateCrc(liste_mit_bytes)))



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
