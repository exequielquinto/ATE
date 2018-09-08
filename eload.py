import visa
import time
# start of untitled
rm = visa.ResourceManager()
eload = rm.open_resource('USB0::0x0A69::0x083E::636002000368::0::INSTR')

#scope = rm.open_resource('USB0::0x0699::0x0413::C026422::0::INSTR')
#print scope.query('*IDN?')

step=(0,1,2,3)

print('start')

eload.write('CHAN 3')   #Channel 1 or 3
print step[1]

eload.write('CURR:STAT:L1 %.2f' % step[2])

#eload.write('CURR:STAT:L1 step[1]')
eload.write('LOAD ON')
time.sleep(5)

eload.write('LOAD Off')


#print eload.query('*IDN?')
print eload.query('*IDN?')


print('finish')