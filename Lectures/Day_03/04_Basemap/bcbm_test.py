#!/usr/bin/env python

# Purpose : Python Boot Camp - Basemap Test Program. 

# Ensure that environment variable PYTHONUNBUFFERED=yes
# This allows STDOUT and STDERR to both be logged in chronological order

import sys                       # platform, args, run tools
import os                        # platform, args, run tools
                                                    
import argparse                  # For parsing command line
import datetime                  # For date/time processing

import numpy as np
import h5py

import matplotlib as mpl
mpl.use('Agg', warn=False)
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show, subplots
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import cm as bm_cm
import matplotlib.cm as mpl_cm

#########################################################################
# Command Line Parameters Class
#########################################################################

class Bcbm_testCP():

    def bcbm_test_cp(self, bcbm_test_cmd_line):        

        description = ("Python Boot Camp - Basemap Test Program")
        parser = argparse.ArgumentParser(description=description)
       
        help_text = ("Display processing messages to STDOUT " +
                     "(DEFAULT=NO)")        
        parser.add_argument("-v", "--verbose",
                          default=False,
                          help=help_text,
                          action="store_true",
                          dest="verbose")

        help_text = ("Run program in test mode " +
                     "(DEFAULT=NO)")        
        parser.add_argument("-t", "--test_mode",
                          default=False,
                          help=help_text,
                          action="store_true",
                          dest="test_mode")

        self.args = parser.parse_args(bcbm_test_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("BCBM_TEST : bcbm_test_cmd_line = " + str(bcbm_test_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Bcbm_test():

    def bcbm_test(self, bcbm_test_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        bcbm_test_cp1     = Bcbm_testCP()
        bcbm_test_cp1_ret = bcbm_test_cp1.bcbm_test_cp(bcbm_test_cmd_line)        

        self.bcbm_test_cmd_line = bcbm_test_cmd_line
        if (len(self.bcbm_test_cmd_line) == 0):
            self.bcbm_test_cmd_line = " " 

        if (bcbm_test_cp1_ret):
            return(bcbm_test_cp1_ret)

        self.verbose          = bcbm_test_cp1.args.verbose                        
        self.test_mode        = bcbm_test_cp1.args.test_mode                

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("BCBM_TEST : Running in test mode\n")
                sys.stdout.write("BCBM_TEST : sys.version = " + str(sys.version) + "\n")                     
        else:
            self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (self.verbose):                   
                sys.stdout.write("BCBM_TEST : Program started : " + str(self.start_time) + "\n")
                sys.stdout.write("BCBM_TEST : sys.version     = " + str(sys.version)     + "\n")

        if (self.verbose):
            sys.stdout.write("BCBM_TEST : sys.version           = " + str(sys.version)           + "\n")     
            sys.stdout.write("BCBM_TEST : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("BCBM_TEST : self.test_mode        = " + str(self.test_mode)        + "\n")

# Call functions

        bcbm_test_f11_ret = self.display_map1()
        if (bcbm_test_f11_ret):
            return(bcbm_test_f11_ret)

# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("BCBM_TEST : Program ended : " + str(self.end_time) + "\n")  
                sys.stdout.write("BCBM_TEST : Run time      : " + str(self.run_time) + "\n")

        if (self.verbose):                       
            sys.stdout.write("BCBM_TEST : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def display_map1(self):
        if (self.verbose):
            sys.stdout.write("BCBM_TEST : display_map1 ACTIVATED\n")

# Set up figure in Matplotlib

        self.current_figure = mpl.pyplot.figure(1, figsize=(14.0, 10.0))        

        self.current_figure.suptitle("Basemap - First Map\n" +
                                     self.timestamp)

        self.current_figure.text(0.05, 0.95, "Mollweide Projection")

        self.current_figure.subplots_adjust(left=0.05,
                                            right=0.95,
                                            top=0.80,
                                            bottom=0.05,
                                            wspace=0.2,
                                            hspace=0.4)

        self.current_plot = self.current_figure.add_subplot(1, 1, 1)
        
# Plot figure

        self.map = Basemap(projection='moll',
                           lon_0=0, #lat_0=0,
                           resolution='c')

        self.map.drawcoastlines()
 
        self.map.drawparallels(np.arange( -90.0,  90.0, 20.0))
        self.map.drawmeridians(np.arange(-180.0, 181.0, 20.0))

# Write the output to a graphic file

        self.current_figure.savefig("bcbm_test_plot1")
        mpl.pyplot.close(self.current_figure)


        return(0)

#------------------------------------------------------------------------------
    
    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        bcbm_test_cmd_line = sys.argv[1:]

    bcbm_test     = Bcbm_test()
    bcbm_test_ret = bcbm_test.bcbm_test(bcbm_test_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
