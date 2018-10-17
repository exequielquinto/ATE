#import pandas as pd         
import visa, time    

#Connect to Instruments
rm = visa.ResourceManager()
DC_Srce = rm.open_resource('USB0::0x0A69::0x084B::S50000000068::0::INSTR')


#Read Instrument IDs
print DC_Srce.query('*IDN?')

DC_Srce.write('SOUR:VOLT 10.00')
DC_Srce.write('SOUR:CURR 5.00')
DC_Srce.write('CONF:OUTP ON')
time.sleep(2)
DC_Srce.write('CONF:OUTP OFF')