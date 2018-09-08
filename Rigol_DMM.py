import visa, time    

#Connect to Instruments
rm = visa.ResourceManager()
DM3058E = rm.open_resource('USB0::0x1AB1::0x0588::DM3R151100113::0::INSTR')

#Read Instrument IDs

print DM3058E.query('*IDN?')


#Rigol DMM Measurement
DM3058E.write('MEAS:VOLT:DC? DEF,DEF')
time.sleep(0.5)
print float(DM3058E.read())