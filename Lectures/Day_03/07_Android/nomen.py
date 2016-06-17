"""
Created on Sat Jun 11 09:53:46 2016
@author: thm02004
"""

import numpy as np
import os

plebians = []
patricians = []

filePath = str(os.path.dirname(os.path.abspath(__file__))) + '/nomen.txt'
nomenFile = open(filePath)
nomenLine = nomenFile.readline()

while nomenLine:

    nomen, status = nomenLine.split(',')
    status = status[0]

    if status == 'N':
        plebians.append(nomen)

    elif status == 'Y':
        patricians.append(nomen)

    else:
        print "Unexpected status value: ", status

    nomenLine = nomenFile.readline()

choice = 'not q'
while choice != 'q':

    choice = raw_input("Input [ p=plebian | P=patrician | q=quit] default = p: ")

    if len(choice) == 0:
        choice = 'p'

    if choice == 'p':
        print '\n', np.random.choice(plebians), '\n'

    elif choice == 'P':
        print '\n', np.random.choice(patricians), '\n'

    elif choice == 'q':
        continue

    else:
        print "Valid inputs are [ p | P]"