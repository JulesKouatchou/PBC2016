#!/usr/bin/env python

"""
   NASA Goddard Space Flight Center
          Python User Group
        2016 Python BootCamp  
"""

import matplotlib.pyplot as plt
import numpy as np

# Open the file
#--------------
fileName = 'Global_Land-Ocean_TempIndex.txt'
f = open(fileName, 'r')

# Create empty lists
#-------------------
year         = []
annualMean   = []
fiveYearMean = []

# Read the file one line at the time
#-----------------------------------
for line in f:
    if (line[0] == "#"):
       pass
    else:
        # get rid of the \n character
       line             = line.strip()
       # split the line into a list
       columns          = line.split()

       # Extract the year
       #-----------------
       year.append(int(columns[0]))

       # Extract the annual mean temperature
       # Take into account any missing value
       #------------------------------------
       if (columns[1].strip() == '*'):
          annualMean.append(None)
       else:
          annualMean.append(float(columns[1]))

       # Extract the 5-year mean temperature
       # Take into account any missing value
       #------------------------------------
       if (columns[2].strip() == '*'):
          fiveYearMean.append(None)
       else:
          fiveYearMean.append(float(columns[2]))

# Close file
#-----------
f.close()

# Convert the data into Numpy arrays and apply the masks
#-------------------------------------------------------
year = np.array(year)

annualMean = np.array(annualMean).astype(np.double)
s1mask = np.isfinite(annualMean)

fiveYearMean = np.array(fiveYearMean).astype(np.double)
s2mask = np.isfinite(fiveYearMean)

# Plot the data
#--------------

plt.plot(year[s1mask], annualMean[s1mask],   label='Annual Mean', linestyle='-',color='black', marker='s')
plt.plot(year[s2mask], fiveYearMean[s2mask], label='5-year Running Mean', linestyle='-', color='r')
plt.title('Global Land-Ocean Temperature Index')
plt.ylabel('Temperature Anomaly ($^{o}C$)')
plt.xlim(year[0],year[-1])
plt.grid()
plt.legend(loc=2)

plt.show()
