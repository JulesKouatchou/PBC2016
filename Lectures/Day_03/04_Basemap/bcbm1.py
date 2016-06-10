#!/usr/bin/env python

# Purpose : Python Boot Camp - Basemap Teaching Program 1. 

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

class Bcbm1CP():

    def bcbm1_cp(self, bcbm1_cmd_line):        

        description = ("Python Boot Camp - Basemap Teaching Program 1")
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

        self.args = parser.parse_args(bcbm1_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("BCBM1 : bcbm1_cmd_line = " + str(bcbm1_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Bcbm1():

    def bcbm1(self, bcbm1_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        bcbm1_cp1     = Bcbm1CP()
        bcbm1_cp1_ret = bcbm1_cp1.bcbm1_cp(bcbm1_cmd_line)        

        self.bcbm1_cmd_line = bcbm1_cmd_line
        if (len(self.bcbm1_cmd_line) == 0):
            self.bcbm1_cmd_line = " " 

        if (bcbm1_cp1_ret):
            return(bcbm1_cp1_ret)

        self.verbose          = bcbm1_cp1.args.verbose                        
        self.test_mode        = bcbm1_cp1.args.test_mode                

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("BCBM1 : Running in test mode\n")
                sys.stdout.write("BCBM1 : sys.version = " + str(sys.version) + "\n")
        else:
            self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (self.verbose):                   
                sys.stdout.write("BCBM1 : Program started : " + str(self.start_time) + "\n")
                sys.stdout.write("BCBM1 : sys.version     = " + str(sys.version)     + "\n")

        if (self.verbose):
            sys.stdout.write("BCBM1 : sys.version           = " + str(sys.version)           + "\n")
            sys.stdout.write("BCBM1 : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("BCBM1 : self.test_mode        = " + str(self.test_mode)        + "\n")

# Call functions

        bcbm1_f11_ret = self.display_map1()
        if (bcbm1_f11_ret):
            return(bcbm1_f11_ret)

        #bcbm1_f21_ret = self.display_map2()
        #if (bcbm1_f21_ret):
        #    return(bcbm1_f21_ret)

        #bcbm1_f31_ret = self.display_map3()
        #if (bcbm1_f31_ret):
        #    return(bcbm1_f31_ret)

# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("BCBM1 : Program ended : " + str(self.end_time) + "\n")  
                sys.stdout.write("BCBM1 : Run time      : " + str(self.run_time) + "\n")

        if (self.verbose):                       
            sys.stdout.write("BCBM1 : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def display_map1(self):
        if (self.verbose):
            sys.stdout.write("BCBM1 : display_map1 ACTIVATED\n")

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
                           lon_0=0,
                           #lat_0=0,
                           resolution='c')

        #self.map.drawmapboundary(fill_color='aqua')
        #self.map.fillcontinents(color='coral',lake_color='aqua')
        self.map.drawcoastlines()

        #self.map.drawcountries()
        #self.map.drawrivers()
        #self.map.drawstates()
 
        self.map.drawparallels(np.arange( -90.0,  90.0, 20.0))
        self.map.drawmeridians(np.arange(-180.0, 181.0, 20.0))

# Write the output to a graphic file

        self.current_figure.savefig("bcbm1_plot1")
        mpl.pyplot.close(self.current_figure)


        return(0)
    
#------------------------------------------------------------------------------

    def display_map2(self):
        if (self.verbose):
            sys.stdout.write("BCBM1 : display_map2 ACTIVATED\n")

# Set up figure in Matplotlib

        self.current_figure = mpl.pyplot.figure(1, figsize=(14.0, 10.0))        

        self.current_figure.suptitle("Basemap - Second Map\n" +
                                     self.timestamp)

        self.current_figure.text(0.05, 0.95, "Robinson Projection - Blue Marble")

        self.current_figure.subplots_adjust(left=0.05,
                                            right=0.95,
                                            top=0.80,
                                            bottom=0.05,
                                            wspace=0.2,
                                            hspace=0.4)

        self.current_plot = self.current_figure.add_subplot(1, 1, 1)
        
# Plot figure

        self.map = Basemap(projection='robin',
                           lon_0=0,
                           lat_0=0,
                           resolution='c')

        #self.map.drawcoastlines()
        #self.map.drawcountries()
        #self.map.drawrivers()
        #self.map.drawstates()
 
        self.map.drawparallels(np.arange( -90.0,  90.0, 20.0))
        self.map.drawmeridians(np.arange(-180.0, 181.0, 20.0))

        self.map.bluemarble() # Known bug here - may appear upside down

# Write the output to a graphic file

        self.current_figure.savefig("bcbm1_plot2")
        mpl.pyplot.close(self.current_figure)


        return(0)

#------------------------------------------------------------------------------

    def display_map3(self):
        if (self.verbose):
            sys.stdout.write("BCBM1 : display_map3 ACTIVATED\n")

# Set up figure in Matplotlib

        self.current_figure = mpl.pyplot.figure(1, figsize=(14.0, 10.0))        

        self.current_figure.suptitle("Basemap - Third Map\n" +
                                     self.timestamp)

        self.current_figure.text(0.05, 0.95, "Near-Sided Perspective Projection - Different Colours")

        self.current_figure.subplots_adjust(left=0.05,
                                            right=0.95,
                                            top=0.80,
                                            bottom=0.05,
                                            wspace=0.2,
                                            hspace=0.4)

        self.current_plot = self.current_figure.add_subplot(1, 1, 1)
        
# Plot figure

        self.map = Basemap(projection='nsper',
                           lon_0=0,
                           lat_0=0, 
                           resolution='c')

        #self.map.drawmapboundary(fill_color='#7777ff')
        #self.map.fillcontinents(color='#ddaa66',lake_color='#7777ff')

        self.map.drawlsmask(land_color = "#ddaa66", 
                            ocean_color="#7777ff")

        #self.map.drawcoastlines()
        #self.map.drawcountries()
        #self.map.drawrivers()
        #self.map.drawstates()
 
        self.map.drawparallels(np.arange( -90.0,  90.0, 20.0))
        self.map.drawmeridians(np.arange(-180.0, 181.0, 20.0))

# Display day and night shading

        #self.date           = datetime.datetime.utcnow()
        #self.map_nightshade = self.map.nightshade(self.date)

# Write the output to a graphic file

        self.current_figure.savefig("bcbm1_plot3")
        mpl.pyplot.close(self.current_figure)


        return(0)

#------------------------------------------------------------------------------
    
    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        bcbm1_cmd_line = sys.argv[1:]

    bcbm1     = Bcbm1()
    bcbm1_ret = bcbm1.bcbm1(bcbm1_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
