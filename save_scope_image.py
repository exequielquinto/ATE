import visa, time

rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x0699::0x0413::C026422::0::INSTR')
print scope.query('*IDN?')

x=131

#scope.write('HARDCOPY:INKSAVER ON')      #NOT WORKING

#Change horizontal scale to any value

#scope.write('HOR:SCA 5e-6')
#scope.write('HOR:SCA 2e-6')

scope.write('SAVE:IMAG:FILEF PNG')
scope.write('HARDCOPY START')
raw_data = scope.read_raw()

fid = open('tek00'+str(x)+'.png','wb')
#fid = open('normal @ 340V min load'+'.png','wb')
fid.write(raw_data)
fid.close()

#print('???')

#scope.write(":MEAS:SOUR CHAN1")
# Grab VMAX
#v_max = scope.query_ascii_values(":MEAS:ITEM? VMAX")
#print v_max

#print scope.query('DATA:SOURCE?')
#print scope.write('MEASU:MEAS1:VAL?')
#print scope.write('CURVE?')

#print scope.write('MEASU:MEAS3:VAL?')
#print scope.write('MEASure:VMAX %s' % ('CHANNEL3'))
#print 1
#temp_values = scope.query_ascii_values(':MEASure:VMAX? %s' % ('CHANNEL3'))
#print temp_values
#print scope.ask('MEASU:VMAX:VAL')
#print float(scope.read())


print('finish')