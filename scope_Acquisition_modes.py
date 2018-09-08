import visa
import time
# start of Untitled

rm = visa.ResourceManager()
scope = rm.open_resource('TCPIP0::10.1.17.5::inst0::INSTR')
print scope.query('*IDN?')


#SINGLE
#scope.write('ACQ:STOPA SEQ')
#print 2
#time.sleep(5)

#RUN
scope.write('ACQ:STATE ON')
print 3
time.sleep(15)

#STOP
scope.write('ACQ:STATE OFF')
print 4
time.sleep(5)

#scope.write('ACQ:STOPA RUNST')
#print 4
#time.sleep(5)




scope.close()
rm.close()

print ('done')
# end of Untitled
