import visa
#import time
# start of Untitled

rm = visa.ResourceManager()
scope = rm.open_resource('USB0::0x0699::0x0413::C026422::0::INSTR')
print scope.query('*IDN?')


scope.write('HORizontal:SCAle 200e-6')

scope.write('CH4:POSition -1')    #sets the Ch vert pos #CH<x>:POSition <NR3># NR3 in div from center graticule
scope.write('CH4:SCAle 5')  #CH<x>:SCAle <NR3> in V/div
scope.write('HARDCOPY:INKSAVER ON')  #HARDCOPY:INKSAVER ON   Not working
scope.write('MEASUrement:STATIstics:MODE OFF')     #statistics off or on

#TRIGGERING
scope.write('HORizontal:POSition 20')   #trigger position in % of screen (0-100%)
scope.write('TRIGGER:A:EDGE:COUPLING DC')    #{DC|HFRej|LFRej|NOISErej}
scope.write('TRIGGER:A:EDGE:SOURCE CH4')
scope.write('TRIGGER:A:EDGE:SLOPE RISE')
scope.write('TRIGger:A:LEVel:CH4 5')   #{ECL|TTL|<NR3>}   ECL=-1.3V:TTL=1.4V

print ('done')

