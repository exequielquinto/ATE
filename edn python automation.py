# Code listing for "How to automate measurements with Python"
# By Fabrizio Guerrieri, Ph.D,
# Senior Member of the Technical Staff, Maxim Integrated
# http://www.edn.com/design/test-and-measurement/4441692/How-to-automate-measurements-with-Python

import numpy as np                            # 1
import pandas as pd                         # 2
import visa, time                        # 3

chroma = visa.instrument('GPIB::2')                # 4
daq = visa.instrument('GPIB::9')                # 5

results = pd.DataFrame()                    # 6
loads = np.arange(0,20+2,2)                    # 7

for load in loads:                        # 8
# Measure the current and the voltage
# Save the results


for load in loads:                        # 8
    chroma.write('CURR:STAT:L1 %.2f' % load)        # 9    
    chroma.write('LOAD ON')                    # 10
    time.sleep(1)                        # 11
    
    temp = {}                        # 12
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@101)')        # 13
    temp['Vout'] = float(daq.read())            # 14
    daq.write('MEAS:VOLT:DC? AUTO,DEF,(@102)')        # 15
    temp['Iout'] = float(daq.read())/0.004            # 16
    
    temp['Vout_id'] = 1.0 - 2.5e-3*temp['Iout']         # A
    temp['Vout_err'] = temp['Vout_id'] - temp['Vout']     # B
    temp['Pass'] = 'Yes'                     # C
    if (abs(temp['Vout_err']) > temp['Vout_id']*0.001):    # D
        temp['Pass'] = 'No'                # E

    results = results.append(temp, ignore_index=True)    # 17
    print "%.2fA\t%.3fV" % (temp['Iout'],temp['Vout'])    # 18

chroma.write('LOAD OFF')                    # 19
results.to_csv('Results.csv')                    # 20


from scipy.stats import linregress                # A
loadline = linregress(results['Iout'], results['Vout'])        # B
print "The loadline is %.2f mohm" % (loadline[0]*1000)        # C
print "The intercept point is %.3f V" % loadline[1]         # D


import matplotlib.pyplot as plt                 # A
plt.plot(results['Iout'],results['Vout'], 'ro')            # B
plt.show()                             # C