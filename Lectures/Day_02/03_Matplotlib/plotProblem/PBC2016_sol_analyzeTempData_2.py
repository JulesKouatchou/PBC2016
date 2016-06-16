#!/usr/bin/env python

"""
   NASA Goddard Space Flight Center
          Python User Group
        2016 Python BootCamp  
"""

import matplotlib.pyplot as plt
import numpy as np

# Read the file
#--------------
fileName = 'Global_Land-Ocean_TempIndex.txt'

A = np.genfromtxt(fileName, skip_header=5, missing_values='*', usemask=True)

year         = A[:,0]
annualMean   = A[:,1]
fiveYearMean = A[:,2]

# Plot the data
#--------------

plt.plot(year, annualMean,   label='Annual Mean', linestyle='-',color='black', marker='s')
plt.plot(year, fiveYearMean, label='5-year Running Mean', linestyle='-', color='r')
plt.title('Global Land-Ocean Temperature Index')
plt.ylabel('Temperature Anomaly ($^{o}C$)')
plt.xlim(year[0],year[-1])
plt.grid()
plt.legend(loc=2)

plt.show()
