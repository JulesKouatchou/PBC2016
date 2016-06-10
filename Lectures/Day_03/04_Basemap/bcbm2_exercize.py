#!/usr/bin/env python

# Purpose : Python Boot Camp - Basemap Teaching Program 2. 

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

################################################

#########################################################################
# Command Line Parameters Class
#########################################################################

class Bcbm2CP():

    def bcbm2_cp(self, bcbm2_cmd_line):        

        description = ("Python Boot Camp - Basemap Teaching Program 2")
        parser = argparse.ArgumentParser(description=description)

        help_text = ("Input file name")      
        parser.add_argument('input_file_name',
                            metavar='input_file_name',
                            #type=string,
                            help=help_text)

        self.meridian_width = 20.0
        help_text = ("Meridian width " +
                     "(DEFAULT=20.0 degrees)")        
        parser.add_argument("-m", "--meridian_width",
                            choices=range(10, 190, 10),                            
                            default=self.meridian_width,
                            help=help_text,
                            action="store",
                            type=float,                          
                            dest="meridian_width")

        self.parallel_width = 20.0
        help_text = ("Parallel width " +
                     "(DEFAULT=20.0 degrees)")        
        parser.add_argument("-p", "--parallel_width",
                            choices=range(5, 100, 5),                            
                            default=self.parallel_width,
                            help=help_text,
                            action="store",
                            type=float,                          
                            dest="parallel_width")
        
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

        self.args = parser.parse_args(bcbm2_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("BCBM2 : bcbm2_cmd_line = " + str(bcbm2_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Bcbm2():

    def bcbm2(self, bcbm2_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        bcbm2_cp1     = Bcbm2CP()
        bcbm2_cp1_ret = bcbm2_cp1.bcbm2_cp(bcbm2_cmd_line)        

        self.bcbm2_cmd_line = bcbm2_cmd_line
        if (len(self.bcbm2_cmd_line) == 0):
            self.bcbm2_cmd_line = " " 

        if (bcbm2_cp1_ret):
            return(bcbm2_cp1_ret)

        self.meridian_width   = bcbm2_cp1.args.meridian_width
        self.parallel_width   = bcbm2_cp1.args.parallel_width                           
        self.verbose          = bcbm2_cp1.args.verbose                        
        self.test_mode        = bcbm2_cp1.args.test_mode                
        self.input_file_name  = bcbm2_cp1.args.input_file_name

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("BCBM2 : Running in test mode\n")
                sys.stdout.write("BCBM2 : sys.version = " + str(sys.version) + "\n")
        else:
            self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (self.verbose):                   
                sys.stdout.write("BCBM2 : Program started : " + str(self.start_time) + "\n")
                sys.stdout.write("BCBM2 : sys.version     = " + str(sys.version)     + "\n")

        if (self.verbose):
            sys.stdout.write("BCBM2 : sys.version           = " + str(sys.version)           + "\n")
            sys.stdout.write("BCBM2 : self.meridian_width   = " + str(self.meridian_width)   + "\n")
            sys.stdout.write("BCBM2 : self.parallel_width   = " + str(self.parallel_width)   + "\n")
            sys.stdout.write("BCBM2 : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("BCBM2 : self.test_mode        = " + str(self.test_mode)        + "\n")
            sys.stdout.write("BCBM2 : self.input_file_name  = " + str(self.input_file_name)  + "\n")

# Call functions

        bcbm2_f11_ret = self.make_mercator_projection()
        if (bcbm2_f11_ret):
            return(bcbm2_f11_ret)

        #bcbm2_f21_ret = self.read_omps_data()
        #if (bcbm2_f21_ret):
        #    return(bcbm2_f21_ret)

        #bcbm2_f31_ret = plot_satellite_tracks()
        #if (bcbm2_f31_ret):
        #    return(bcbm2_f31_ret)

# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("BCBM2 : Program ended : " + str(self.end_time) + "\n")  
                sys.stdout.write("BCBM2 : Run time      : " + str(self.run_time) + "\n")

        if (self.verbose):                       
            sys.stdout.write("BCBM2 : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def make_mercator_projection(self):
        if (self.verbose):
            sys.stdout.write("BCBM2 : make_mercator_projection ACTIVATED\n")

# Set up figure in Matplotlib

        self.current_figure = mpl.pyplot.figure(1, figsize=(14.0, 10.0))        

        self.current_figure.suptitle("Basemap - Mercator Map\n" +
                                     self.timestamp)

        self.current_figure.text(0.05, 0.95, "A Mercator Projection of the Earth")

        self.current_figure.subplots_adjust(left=0.05,
                                            right=0.95,
                                            top=0.80,
                                            bottom=0.05,
                                            wspace=0.2,
                                            hspace=0.4)

        self.current_plot = self.current_figure.add_subplot(1, 1, 1)
        
# Plot figure

        self.map = Basemap(projection='merc',
                           lat_0=0,
                           lon_0=0,
                           llcrnrlat=-80,
                           urcrnrlat=80,
                           llcrnrlon=-180,
                           urcrnrlon=180,
                           resolution='c')    

        #self.map.drawmapboundary(fill_color='aqua')
        #self.map.fillcontinents(color='coral',lake_color='aqua')
        self.map.drawcoastlines()

        #self.map.drawcountries()
        #self.map.drawrivers()
        #self.map.drawstates()
 
        self.map.drawparallels(np.arange( -90.0,  90.0, self.parallel_width))
        self.map.drawmeridians(np.arange(-180.0, 181.0, self.meridian_width))

# Display day and night shading

        #self.date           = datetime.datetime.utcnow()
        #self.map_nightshade = self.map.nightshade(self.date)

# Write the output to a graphic file

        #self.current_figure.savefig("bcbm2_plot1")
        #mpl.pyplot.close(self.current_figure)

# Read data from input file

        self.read_omps_data()

# Plot satellite tracks

        #self.plot_satellite_tracks_dots()
        self.plot_satellite_tracks_lines()

        mpl.pyplot.close(self.current_figure)
        
        return(0)
    
#------------------------------------------------------------------------------

    def read_omps_data(self):
        if (self.verbose):
            sys.stdout.write("BCBM2 : read_omps_data ACTIVATED\n")

# Open input HDF5 file
   
        self.input_file = h5py.File(self.input_file_name, "r")
        sys.stdout.write("BCBM2 : self.input_file = " + str(self.input_file) + "\n")
    
        self.o3        = self.input_file["DataFields/O3CombinedValue"]    
        self.lats      = self.input_file["GeolocationFields/Latitude"]
        self.lons      = self.input_file["GeolocationFields/Longitude"] 
        self.orbit_num = self.input_file["GeolocationFields/OrbitNumber"]
          
# Convert from Numpy objects to list arrays    
# Select only centre slit data

        self.lat_cs        = self.lats[:,1]             
        self.lon_cs        = self.lons[:,1]
        self.orbit_num_cs  = self.orbit_num[:,1]             

        sys.stdout.write("BCBM2 : self.lat_cs       = " + str(self.lat_cs)       + "\n")
        sys.stdout.write("BCBM2 : self.lon_cs       = " + str(self.lon_cs)       + "\n")
        sys.stdout.write("BCBM2 : self.orbit_num_cs = " + str(self.orbit_num_cs) + "\n")        

        return(0)

#------------------------------------------------------------------------------

    def plot_satellite_tracks_dots(self):
        if (self.verbose):
            sys.stdout.write("BCBM2 : plot_satellite_tracks_dots ACTIVATED\n")

# Set up mesh for plotting

        self.xmesh, self.ymesh = self.map(self.lon_cs, self.lat_cs)
    
        self.map_scatter = self.map.scatter(self.xmesh,                                          
                                            self.ymesh,
                                            1,
                                            marker='o',
                                            color='r',
                                            label="OMPS"
                                            )  

# Write the output to a graphic file

        self.current_figure.savefig("bcbm2_plot2")
        #mpl.pyplot.close(self.current_figure)

        return(0)

#------------------------------------------------------------------------------

    def plot_satellite_tracks_lines(self):
        if (self.verbose):
            sys.stdout.write("BCBM2 : plot_satellite_tracks_lines ACTIVATED\n")

# Make unique list of orbit numbers

        self.orbit_num_cs_unique = np.unique(self.orbit_num_cs)
        sys.stdout.write("BCBM2 : self.orbit_num_cs_unique = " +
                         str(self.orbit_num_cs_unique) + "\n")

# Loop on unique orbit numbers        

        for self.orbit_num in self.orbit_num_cs_unique:

            #sys.stdout.write("BCBM2 : self.orbit_num = " + str(self.orbit_num) + "\n")    

# Find the data for just that orbit 

            self.lat_cs_orbit = self.lat_cs[np.where(self.orbit_num_cs == self.orbit_num)] 
            self.lon_cs_orbit = self.lon_cs[np.where(self.orbit_num_cs == self.orbit_num)]
            
            #sys.stdout.write("BCBM2 : len(self.lat_cs_orbit) = " + str(len(self.lat_cs_orbit)) + "\n")
            #sys.stdout.write("BCBM2 : len(self.lon_cs_orbit) = " + str(len(self.lon_cs_orbit)) + "\n")

# Set up mesh for plotting

            self.xmesh_orbit, self.ymesh_orbit = self.map(self.lon_cs_orbit, self.lat_cs_orbit)
    
            self.map_plot = self.map.plot(self.xmesh_orbit,
                                          self.ymesh_orbit,
                                          "-",
                                          #marker='o',
                                          color='r',
                                          label="OMPS"
                                          )  

# Write the output to a graphic file

        self.current_figure.savefig("bcbm2_plot3")
        #mpl.pyplot.close(self.current_figure)

        return(0)

#------------------------------------------------------------------------------  

    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        bcbm2_cmd_line = sys.argv[1:]

    bcbm2     = Bcbm2()
    bcbm2_ret = bcbm2.bcbm2(bcbm2_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
