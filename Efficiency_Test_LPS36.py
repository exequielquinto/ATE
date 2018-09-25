#import numpy as np
import pandas as pd         
import visa, time    

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL1::INSTR')
eload1 = rm.open_resource('USB0::0x0A69::0x083E::636002000532::0::INSTR')  #Ch2, Ch1
eload2 = rm.open_resource('USB0::0x0A69::0x083E::636002000381::0::INSTR')  #Ch4, Ch3

#Read Instrument IDs
print daq.query('*IDN?')
print eload1.query('*IDN?')
print eload2.query('*IDN?')

#For load sequence
steps=(0,1,2,3,4,5,6,7,8,9,10,11,12)
load=(0,0.002,0.025,0.050,0.075,0.1,0.125,0.150,0.175,0.2,0.225,0.25,0.255)

#quick check channel
#steps=(0,1,2)    
#load=(0.025,0.125)

print steps
print load

#Burn In
eload1.write('CHAN 3')   #Ch1    
eload1.write('CURR:STAT:L1 %.4f' % load[11])
eload1.write('LOAD ON')
eload1.write('CHAN 1')   #Ch2
eload1.write('CURR:STAT:L1 %.4f' % load[11])
eload1.write('LOAD ON')
eload2.write('CHAN 3')   #Ch3    
eload2.write('CURR:STAT:L1 %.4f' % load[11])
eload2.write('LOAD ON')
eload2.write('CHAN 1')   #Ch4
eload2.write('CURR:STAT:L1 %.4f' % load[11])
eload2.write('LOAD ON')
print ('warming up...')
print ('time now is')
print (time.ctime())
time.sleep(5)     # burn In time at full full before capturing efficiency

results = pd.DataFrame()

for step in steps:

    eload1.write('CHAN 3')   #Ch1
    time.sleep(0.5)    
    eload1.write('CURR:STAT:L1 %.4f' % load[step])
    time.sleep(0.5)
    eload1.write('LOAD ON')
    time.sleep(0.5)
    eload1.write('CHAN 1')   #Ch2
    time.sleep(0.5)
    eload1.write('CURR:STAT:L1 %.4f' % load[step])
    time.sleep(0.5)
    eload1.write('LOAD ON')
    time.sleep(0.5)
    eload2.write('CHAN 3')   #Ch3
    time.sleep(0.5)    
    eload2.write('CURR:STAT:L1 %.4f' % load[step])
    time.sleep(0.5)
    eload2.write('LOAD ON')
    time.sleep(0.5)
    eload2.write('CHAN 1')   #Ch4
    time.sleep(0.5)
    eload2.write('CURR:STAT:L1 %.4f' % load[step])
    time.sleep(0.5)
    eload2.write('LOAD ON')
    time.sleep(0.5)
       
    print step
    print ('capturing efficiency every min...')
    print ('time now is')
    print (time.ctime())
    time.sleep(60)   # Delay in seconds before capturing results

    temp = {}
    
    #Vin Measure
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@101)')
    time.sleep(0.5)                              
    Vin = float(daq.read())
    temp['A_Vin'] = Vin
    #Iin Measure
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@110)')
    time.sleep(0.5)                              
    Iin = float(daq.read())
    temp['B_Iin'] = Iin*1000    #Amp
    
    #Ch1 Measure  
    eload1.write('CHAN 3')   #Ch1    
    V1 = (eload1.query('MEASure:VOLTage?'))
    time.sleep(0.5)
    I1 = (eload1.query('MEASure:CURRent?'))
    #V1 = (eload1.query('MEASure:VOLTage?'))    also works with these
    #print (eload1.query('FETCh:ALLVoltage?'))
    #x=(eload1.query('MEASure:ALLVoltage?'))
    #print x
    #print x[0:10]
    time.sleep(0.5)
    temp['C_Ch1_Vout'] = float(V1)
    temp['D_Ch1_Iout'] = float(I1)

    #Ch2 Measure
    eload1.write('CHAN 1')   #Ch1    
    V2 = (eload1.query('MEASure:VOLTage?'))
    time.sleep(0.5)
    I2 = (eload1.query('MEASure:CURRent?'))
    time.sleep(0.5)
    temp['E_Ch2_Vout'] = float(V2)
    temp['F_Ch2_Iout'] = float(I2)
    
    #Ch3 Measure  
    eload2.write('CHAN 3')   #Ch1    
    V3 = (eload2.query('MEASure:VOLTage?'))
    time.sleep(0.5)
    I3 = (eload2.query('MEASure:CURRent?'))
    time.sleep(0.5)
    temp['G_Ch3_Vout'] = float(V3)
    temp['H_Ch3_Iout'] = float(I3)

    #Ch4 Measure
    eload2.write('CHAN 1')   #Ch1    
    V4 = (eload2.query('MEASure:VOLTage?'))
    time.sleep(0.5)
    I4 = (eload2.query('MEASure:CURRent?'))
    time.sleep(0.5)
    temp['I_Ch4_Vout'] = float(V4)
    temp['J_Ch4_Iout'] = float(I4)
    
    
    #Efficiency
    #temp['K_Efficiency'] = ((V1*I1)+(V2*I2)+(V3*I3)+(V4*I4))*100/(Vin*Iin)
    #temp['K_Pout'] = (V4*I4)
    #temp['M_Efficiency'] = (Vin*Iin)
    
    results = results.append(temp, ignore_index=True)    # 17
    #print results
    print "%.2fV\t%.3fA" % (temp['C_Ch1_Vout'],temp['D_Ch1_Iout'])    # ? on print formatting
    
#Set to less load after finishing test
eload1.write('CHAN 3')   #Ch1    
eload1.write('CURR:STAT:L1 %.4f' % load[3])
eload1.write('LOAD ON')
eload1.write('CHAN 1')   #Ch2
eload1.write('CURR:STAT:L1 %.4f' % load[3])
eload1.write('LOAD ON')
eload2.write('CHAN 3')   #Ch3    
eload2.write('CURR:STAT:L1 %.4f' % load[3])
eload2.write('LOAD ON')
eload2.write('CHAN 1')   #Ch4
eload2.write('CURR:STAT:L1 %.4f' % load[3])
eload2.write('LOAD ON')                  
results.to_csv('Results.csv')                    # Heading Arranged alphabetically

print('finished')
