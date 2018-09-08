import numpy as np
import pandas as pd         
import visa, time    

#Connect to Instruments
rm = visa.ResourceManager()
daq = rm.open_resource('ASRL1::INSTR')
scope = rm.open_resource('USB0::0x0699::0x0413::C026422::0::INSTR')
DM3058E = rm.open_resource('USB0::0x1AB1::0x0588::DM3R151100113::0::INSTR')

#Read Instrument IDs
print daq.query('*IDN?')
print scope.query('*IDN?')
print DM3058E.query('*IDN?')

#For load sequence
Load_min=0
Load_max=10
Num_steps=5

loads = np.arange(Load_min,Load_max+(Load_max/Num_steps),Load_max/Num_steps)
print loads
results = pd.DataFrame()

for load in loads:
    #chroma.write('CURR:STAT:L1 %.2f' % load)
    #chroma.write('LOAD ON')
    #time.sleep(1)
    
    print load
    time.sleep(3)   # Delay in seconds before capturing results

    temp = {}
    
    #Rigol DMM Measurement
    DM3058E.write(':MEASure:VOLTage:DC? %s,%s' % ('DEF', 'DEF'))
    time.sleep(0.5)
    temp['D_Vout2'] = float(DM3058E.read())
    
  
    #Data Aquisition Measurements
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@101)')
    time.sleep(0.5)                                 #delay fix some random error
    temp['B_Vout'] = float(daq.read())
    
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@102)')
    time.sleep(0.5)
    temp['C_Iout'] = float(daq.read())/0.01
    
    temp['A_Load_Num'] = load
    #print temp


    results = results.append(temp, ignore_index=True)    # 17
    #print results
    print "%.2fA\t%.3fV" % (temp['C_Iout'],temp['B_Vout'])    # ? on print formatting
    
    #Capture Scope screen
    scope.write('SAVE:IMAG:FILEF PNG')
    scope.write('HARDCOPY START')
    raw_data = scope.read_raw()

    fid = open('image'+str(load)+'.png','wb')
    fid.write(raw_data)
    fid.close()
    
#chroma.write('LOAD OFF')                    
results.to_csv('Results.csv')                    # Heading Arranged alphabetically

print('finished')
