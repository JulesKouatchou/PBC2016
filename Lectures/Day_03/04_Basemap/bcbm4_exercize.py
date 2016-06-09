#!/usr/bin/env python

# Purpose : Python Boot Camp - Basemap Teaching Program 4. 

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

class Bcbm4CP():

    def bcbm4_cp(self, bcbm4_cmd_line):        

        description = ("Python Boot Camp - Basemap Teaching Program 4")
        parser = argparse.ArgumentParser(description=description)

        help_text = ("Input file name")      
        parser.add_argument('input_file_name',
                            metavar='input_file_name',
                            #type=string,
                            help=help_text)
        
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

        self.args = parser.parse_args(bcbm4_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("BCBM4 : bcbm4_cmd_line = " + str(bcbm4_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Bcbm4():

    def bcbm4(self, bcbm4_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        bcbm4_cp1     = Bcbm4CP()
        bcbm4_cp1_ret = bcbm4_cp1.bcbm4_cp(bcbm4_cmd_line)        

        self.bcbm4_cmd_line = bcbm4_cmd_line
        if (len(self.bcbm4_cmd_line) == 0):
            self.bcbm4_cmd_line = " " 

        if (bcbm4_cp1_ret):
            return(bcbm4_cp1_ret)

        self.verbose          = bcbm4_cp1.args.verbose                        
        self.test_mode        = bcbm4_cp1.args.test_mode                
        self.input_file_name  = bcbm4_cp1.args.input_file_name

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("BCBM4 : Running in test mode\n")
                sys.stdout.write("BCBM4 : sys.version = " + str(sys.version) + "\n")
        else:
            self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (self.verbose):                   
                sys.stdout.write("BCBM4 : Program started : " + str(self.start_time) + "\n")
                sys.stdout.write("BCBM4 : sys.version     = " + str(sys.version)     + "\n")

        if (self.verbose):
            sys.stdout.write("BCBM4 : sys.version           = " + str(sys.version)           + "\n")
            sys.stdout.write("BCBM4 : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("BCBM4 : self.test_mode        = " + str(self.test_mode)        + "\n")
            sys.stdout.write("BCBM4 : self.input_file_name  = " + str(self.input_file_name)  + "\n")

# Call functions

        bcbm4_f11_ret = self.read_omps_data()
        if (bcbm4_f11_ret):
            return(bcbm4_f11_ret)

        bcbm4_f11_ret = self.make_north_america_map()
        if (bcbm4_f11_ret):
            return(bcbm4_f11_ret)

# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("BCBM4 : Program ended : " + str(self.end_time) + "\n")  
                sys.stdout.write("BCBM4 : Run time      : " + str(self.run_time) + "\n")

        if (self.verbose):                       
            sys.stdout.write("BCBM4 : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def read_omps_data(self):
        if (self.verbose):
            sys.stdout.write("BCBM4 : read_omps_data ACTIVATED\n")

# Open input HDF5 file
   
        self.input_file = h5py.File(self.input_file_name, "r")
        sys.stdout.write("BCBM4 : self.input_file = " + str(self.input_file) + "\n")
    
        self.o3        = self.input_file["DataFields/O3CombinedValue"]    
        self.lats      = self.input_file["GeolocationFields/Latitude"]
        self.lons      = self.input_file["GeolocationFields/Longitude"] 
        self.orbit_num = self.input_file["GeolocationFields/OrbitNumber"]
          
# Convert from Numpy objects to list arrays    
# Select only centre slit data

        self.lat_cs        = self.lats[:,1]             
        self.lon_cs        = self.lons[:,1]
        self.orbit_num_cs  = self.orbit_num[:,1]             

        sys.stdout.write("BCBM4 : self.lat_cs       = " + str(self.lat_cs)       + "\n")
        sys.stdout.write("BCBM4 : self.lon_cs       = " + str(self.lon_cs)       + "\n")
        sys.stdout.write("BCBM4 : self.orbit_num_cs = " + str(self.orbit_num_cs) + "\n")        

        return(0)

#------------------------------------------------------------------------------

    def make_north_america_map(self):
        if (self.verbose):
            sys.stdout.write("BCBM4 : make_north_america_map ACTIVATED\n")

# Set up figure in Matplotlib

        self.current_figure = mpl.pyplot.figure(1, figsize=(14.0, 10.0))        

        self.current_figure.suptitle("Basemap - Lambert Conformal Projection Map\n" +
                                     self.timestamp)

        self.current_figure.text(0.05, 0.95, "A Map of North America")

        self.current_figure.subplots_adjust(left=0.05,
                                            right=0.95,
                                            top=0.80,
                                            bottom=0.05,
                                            wspace=0.2,
                                            hspace=0.4)

        self.current_plot = self.current_figure.add_subplot(1, 1, 1)
        
# Plot figure

        self.map = Basemap(width=12000000,
                           height=9000000,
                           projection='lcc',
                           resolution='c',
                           lat_1=45.,
                           lat_2=55,
                           lat_0=50,
                           lon_0=-107.)


        #self.map.drawmapboundary(fill_color='aqua')
        #self.map.fillcontinents(color='coral',lake_color='aqua')
        self.map.drawcoastlines()

        #self.map.shadedrelief() # - Basemap V.1.0.2 onwards
        #self.map.etopo()        # - Basemap V.1.0.2 onwards

        #self.map.drawcountries()
        #self.map.drawrivers()
        #self.map.drawstates()

        self.parallels = np.arange(0.0, 81.0, 10.0)
        self.map.drawparallels(self.parallels,
                               labels=[False, True, True, False])
        self.meridians = np.arange(10.0, 351.0, 20.0)
        self.map.drawmeridians(self.meridians,
                               labels=[True, False, False, True])

# Include City Data
# Comment out colour/relief overlays before running this

        self.city_data()

# Plot satellite tracks

        self.plot_satellite_tracks_lines()

# Write the output to a graphic file

        self.current_figure.savefig("bcbm4_plot1")
        mpl.pyplot.close(self.current_figure)

        return(0)

#------------------------------------------------------------------------------

    def city_data(self):
        if (self.verbose):
            sys.stdout.write("BCBM4 : city_data ACTIVATED\n")

# Dictionary city populations

        self.pop={'New York':8244910,
                  'Los Angeles':3819702,
                  'Chicago':2707120,
                  'Houston':2145146,
                  'Phoenix':1469471,
                  'Dallas':1223229,
                  'Jacksonville':827908,
                  'Indianapolis':827908,
                  'San Francisco':812826,
                  'Lawrence':876430,
                  'Anchorage':2918260} 

# Dictionary of city latitudes
        
        self.lat={'New York':40.6643,
                  'Los Angeles':34.0194,
                  'Chicago':41.8376,
                  'Houston':29.7805,
                  'Phoenix':33.5722,
                  'Dallas':32.7942,
                  'Jacksonville':30.3370,
                  'Indianapolis':39.7767,
                  'San Francisco':37.7750,
                  'Lawrence':38.9666,
                  'Anchorage':61.2166}
                  
# Dictionary of city longitudes
        
        self.lon={'New York':73.9385,
                  'Los Angeles':118.4108,
                  'Chicago':87.6818,
                  'Houston':95.3863,
                  'Phoenix':112.0880,
                  'Dallas':96.7655,
                  'Jacksonville':81.6613,
                  'Indianapolis':86.1459,
                  'San Francisco':122.4183,
                  'Lawrence':95.2333,
                  'Anchorage':149.9000}
                  
# Plot city population sizes
# Add the city names

        self.max_size=80
        for self.city in self.lon.keys():
            
            self.x, self.y = self.map(-self.lon[self.city],
                                      self.lat[self.city])
            
            self.map.scatter(self.x,
                             self.y,
                             self.max_size*self.pop[self.city]/self.pop['New York'],
                             marker='o',
                             color='r')

            plt.text(self.x+50000, self.y+50000, self.city)

        return(0)

#------------------------------------------------------------------------------  

    def plot_satellite_tracks_lines(self):
        if (self.verbose):
            sys.stdout.write("BCBM4 : plot_satellite_tracks_lines ACTIVATED\n")

# Make unique list of orbit numbers

        self.orbit_num_cs_unique = np.unique(self.orbit_num_cs)
        sys.stdout.write("BCBM4 : self.orbit_num_cs_unique = " +
                         str(self.orbit_num_cs_unique) + "\n")

# Loop on unique orbit numbers        

        for self.orbit_num in self.orbit_num_cs_unique:

            #sys.stdout.write("BCBM4 : self.orbit_num = " + str(self.orbit_num) + "\n")    

# Find the data for just that orbit 

            self.lat_cs_orbit = self.lat_cs[np.where(self.orbit_num_cs == self.orbit_num)] 
            self.lon_cs_orbit = self.lon_cs[np.where(self.orbit_num_cs == self.orbit_num)]
            
            #sys.stdout.write("BCBM4 : len(self.lat_cs_orbit) = " + str(len(self.lat_cs_orbit)) + "\n")
            #sys.stdout.write("BCBM4 : len(self.lon_cs_orbit) = " + str(len(self.lon_cs_orbit)) + "\n")

# Set up mesh for plotting

            self.xmesh_orbit, self.ymesh_orbit = self.map(self.lon_cs_orbit, self.lat_cs_orbit)
    
            self.map_plot = self.map.plot(self.xmesh_orbit,
                                          self.ymesh_orbit,
                                          "-",
                                          #marker='o',
                                          color='m',
                                          label="OMPS"
                                          )

        return(0)

#------------------------------------------------------------------------------

    
    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        bcbm4_cmd_line = sys.argv[1:]

    bcbm4     = Bcbm4()
    bcbm4_ret = bcbm4.bcbm4(bcbm4_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
