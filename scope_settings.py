import visa
import time
# start of Untitled

rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x0699::0x0413::C026422::0::INSTR')
print scope.query('*IDN?')


scope.write('HORizontal:SCAle 20e-6')

scope.write('HORizontal:POSition 10')   #trigger position in % of screen (0-100%)

scope.write('CH4:POSition -1')    #sets the Ch vert pos #CH<x>:POSition <NR3># NR3 in div from center graticule
scope.write('CH4:SCAle 5')  #CH<x>:SCAle <NR3>

print ('done')

