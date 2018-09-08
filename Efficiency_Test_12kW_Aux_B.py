#import numpy as np
import pandas as pd         
import visa, time

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL1::INSTR')
scope = rm.open_resource('USB0::0x0699::0x0408::C030077::0::INSTR')
DM3058E = rm.open_resource('USB0::0x1AB1::0x0588::DM3R151100113::0::INSTR')
eload = rm.open_resource('USB0::0x0A69::0x083E::636002000368::0::INSTR')

#Read Instrument IDs
print daq.query('*IDN?')
print scope.query('*IDN?')
print DM3058E.query('*IDN?')
print eload.query('*IDN?')

#For load sequence
#steps=(0,1,2,3,4,5,6)
#load1=(2.68,2.36,2.36,1.7,0.687,0.687,0.25)
#load2=(2.68,1.04,0.32,0.7,1.04,0.32,0.25)
steps=(0,1)
#load1=(2.68,2.36)
#load2=(2.68,1.04)

#For 240Vin
load1=(0.687,0.25)
load2=(0.32,0.25)

print steps
print load1
print load2

results = pd.DataFrame()

for step in steps:
    #chroma.write('CURR:STAT:L1 %.2f' % load)
    #chroma.write('LOAD ON')
    #time.sleep(1)
    eload.write('CHAN 1')   #13Vp    
    eload.write('CURR:STAT:L1 %.2f' % load1[step])
    eload.write('LOAD ON')
    
    eload.write('CHAN 3')   #13Vs
    eload.write('CURR:STAT:L1 %.2f' % load2[step])
    eload.write('LOAD ON')
    
    print step
    if step==0:
        print ('time now is')
        print (time.ctime())
        time.sleep(5)    #warm up time  1200 for 20 mins
    else:
        print ('time now is')
        print (time.ctime())
        time.sleep(5)    #180 for 3 mins
         
    #print step
    #time.sleep(3)   # Delay in seconds before capturing results

    temp = {}
    
    #Vin Measure
    DM3058E.write('MEAS:VOLT:DC? DEF,DEF')
    time.sleep(0.5)
    Vin = float(DM3058E.read())
    temp['A_Vin'] = Vin
    #Iin Measure
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@101)')
    time.sleep(0.5)                                 #delay fix some random error
    Iin = float(daq.read())
    temp['B_Iin'] = Iin*1000    #mA
    
    #13Vp Measure  
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@102)')
    time.sleep(0.5)
    V1 = float(daq.read())
    temp['C_13Vp_Vout'] = V1
    #13Vp I Measure
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@103)')
    time.sleep(0.5)                                 #delay fix some random error
    I1 = float(daq.read())/0.1
    temp['D_13Vp_Iout'] = I1
    
    #5Vp Measure  
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@104)')
    time.sleep(0.5)
    V2 = float(daq.read())
    temp['E_5Vp_Vout'] = V2
    #5Vp I Measure
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@105)')
    time.sleep(0.5)                                 #delay fix some random error
    I2 = float(daq.read())/0.1
    temp['F_5Vp_Iout'] = I2
    
    #13Vs Measure  
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@106)')
    time.sleep(0.5)
    V3 = float(daq.read())
    temp['G_13Vs_Vout'] = V3
    #13Vs I Measure
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@107)')
    time.sleep(0.5)                                 #delay fix some random error
    I3 = float(daq.read())/0.1
    temp['H_13Vs_Iout'] = I3
    
    #Temp reading
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@113'))
    time.sleep(0.5)
    temp['I_Q102_Temp'] = float(daq.read())
    daq.write('MEAS:TEMP? %s,%s,(%s)' % ('TCouple', 'K', '@114'))
    time.sleep(0.5)
    temp['J_Q103_Temp'] = float(daq.read())
    
    #Efficiency
    temp['K_Efficiency'] = ((V1*I1)+(V2*I2)+(V3*I3))*100/(Vin*Iin)
    
    results = results.append(temp, ignore_index=True)    # 17
    #print results
    print "%.2fdegC\t%.3fPercent" % (temp['I_Q102_Temp'],temp['K_Efficiency'])    # ? on print formatting
    
    #Change horizontal scale to any value
    
    scope.write('ACQ:STATE OFF')
    scope.write('HOR:SCA 10e-6')
    time.sleep(3)        
    #Capture Scope screen
    scope.write('SAVE:IMAG:FILEF PNG')
    scope.write('HARDCOPY START')
    raw_data = scope.read_raw()

    fid = open('tek000'+str(step)+'.png','wb')
    fid.write(raw_data)
    fid.close()
    
    scope.write('HOR:SCA 2e-6')
    time.sleep(3)       
    #Capture Scope screen
    scope.write('SAVE:IMAG:FILEF PNG')
    scope.write('HARDCOPY START')
    raw_data = scope.read_raw()

    fid = open('tek000'+str(step)+'b.png','wb')
    fid.write(raw_data)
    fid.close()

    
    scope.write('HOR:SCA 20e-6')
    scope.write('ACQ:STATE ON')

#set to min load
eload.write('CHAN 1')   #13Vp    
eload.write('CURR:STAT:L1 0.25')
eload.write('CHAN 3')   #13Vs
eload.write('CURR:STAT:L1 0.25')
                  
results.to_csv('Results.csv')                    # Heading Arranged alphabetically

print('finished')
