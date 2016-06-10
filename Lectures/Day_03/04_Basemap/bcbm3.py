#!/usr/bin/env python

# Purpose : Python Boot Camp - Basemap Teaching Program 3. 

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

class Bcbm3CP():

    def bcbm3_cp(self, bcbm3_cmd_line):        

        description = ("Python Boot Camp - Basemap Teaching Program 3")
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

        self.args = parser.parse_args(bcbm3_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("BCBM3 : bcbm3_cmd_line = " + str(bcbm3_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Bcbm3():

    def bcbm3(self, bcbm3_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        bcbm3_cp1     = Bcbm3CP()
        bcbm3_cp1_ret = bcbm3_cp1.bcbm3_cp(bcbm3_cmd_line)        

        self.bcbm3_cmd_line = bcbm3_cmd_line
        if (len(self.bcbm3_cmd_line) == 0):
            self.bcbm3_cmd_line = " " 

        if (bcbm3_cp1_ret):
            return(bcbm3_cp1_ret)

        self.verbose          = bcbm3_cp1.args.verbose                        
        self.test_mode        = bcbm3_cp1.args.test_mode                
        self.input_file_name  = bcbm3_cp1.args.input_file_name

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("BCBM3 : Running in test mode\n")
                sys.stdout.write("BCBM3 : sys.version = " + str(sys.version) + "\n")
        else:
            self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (self.verbose):                   
                sys.stdout.write("BCBM3 : Program started : " + str(self.start_time) + "\n")
                sys.stdout.write("BCBM3 : sys.version     = " + str(sys.version)     + "\n")

        if (self.verbose):
            sys.stdout.write("BCBM3 : sys.version           = " + str(sys.version)           + "\n")
            sys.stdout.write("BCBM3 : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("BCBM3 : self.test_mode        = " + str(self.test_mode)        + "\n")
            sys.stdout.write("BCBM3 : self.input_file_name  = " + str(self.input_file_name)  + "\n")

# Call functions

        bcbm3_f11_ret = self.read_omps_data()
        if (bcbm3_f11_ret):
            return(bcbm3_f11_ret)

        bcbm3_f11_ret = self.make_mercator_projection()
        if (bcbm3_f11_ret):
            return(bcbm3_f11_ret)

# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("BCBM3 : Program ended : " + str(self.end_time) + "\n")  
                sys.stdout.write("BCBM3 : Run time      : " + str(self.run_time) + "\n")

        if (self.verbose):                       
            sys.stdout.write("BCBM3 : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def read_omps_data(self):
        if (self.verbose):
            sys.stdout.write("BCBM3 : read_omps_data ACTIVATED\n")

# Open input HDF5 file
   
        self.input_file = h5py.File(self.input_file_name, "r")
        sys.stdout.write("BCBM3 : self.input_file = " + str(self.input_file) + "\n")
    
        self.o3       = self.input_file["ColumnAmountO3"]    
        self.lat      = self.input_file["Latitude"]
        self.lon      = self.input_file["Longitude"] 
          
# Convert from Numpy objects to list arrays    

        #self.o3  = self.o3[:,:]
        #self.lat = self.lat[:]          
        #self.lon = self.lon[:]

        sys.stdout.write("BCBM3 : self.o3  = " + str(self.o3)  + "\n")
        sys.stdout.write("BCBM3 : self.lat = " + str(self.lat) + "\n")
        sys.stdout.write("BCBM3 : self.lon = " + str(self.lon) + "\n")

        sys.stdout.write("BCBM3 : len(self.o3)  = " + str(len(self.o3))  + "\n")
        sys.stdout.write("BCBM3 : len(self.lat) = " + str(len(self.lat)) + "\n")
        sys.stdout.write("BCBM3 : len(self.lon) = " + str(len(self.lon)) + "\n")

        return(0)

#------------------------------------------------------------------------------

    def make_mercator_projection(self):
        if (self.verbose):
            sys.stdout.write("BCBM3 : make_mercator_projection ACTIVATED\n")

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
 
        self.map.drawparallels(np.arange( -90.0,  90.0, 20.0))
        self.map.drawmeridians(np.arange(-180.0, 181.0, 20.0))

# Write the output to a graphic file

        self.current_figure.savefig("bcbm3_plot1")
        #mpl.pyplot.close(self.current_figure)

# Plot colour scale and contour maps

        #self.plot_colour_scale()
        self.plot_colour_contours()

        mpl.pyplot.close(self.current_figure)

        return(0)

#------------------------------------------------------------------------------

    def plot_colour_scale(self):
        if (self.verbose):
            sys.stdout.write("BCBM3 : plot_colour_scale ACTIVATED\n")

# Set up mesh for plotting

        self.xmesh, self.ymesh = self.map(*np.meshgrid(self.lon, self.lat))
        
        #sys.stdout.write("BCBM3 : self.xmesh = " + str(self.xmesh) + "\n")    
        #sys.stdout.write("BCBM3 : self.ymesh = " + str(self.ymesh) + "\n")    
    
# Set colour map and levels

        self.colormap = mpl_cm.jet
      
        self.colormap.set_under(color='k',
                                alpha=1.0)
        self.colormap.set_over(color='k',
                               alpha=1.0)  

# Set colour levels

        self.plot_colormap_level_lower = 200
        self.plot_colormap_level_upper = 525
        self.plot_colormap_level_space = 25
                                      
        self.color_levels = np.arange(self.plot_colormap_level_lower,
                                      self.plot_colormap_level_upper,
                                      self.plot_colormap_level_space)

# Set plotting of data outside color map range to display in (default=)black
# If this is not done then python will take the first and last colors of the colormap
# and apply them to data outside the range.
# IE.: It will effectively shorten the color scale by two colors
# and then rescale everything else to fit that shortened scale.
# Normalize : "clip" must be set to FALSE
# "alpha=1.0" means use solid color values
# "alpha" controls transparency, alpha=1=solid, alpha=0=transparent
# 0<alpha<1, range of transparent values

        self.norm_range = mpl.colors.Normalize(vmin=self.plot_colormap_level_lower,
                                               vmax=(self.plot_colormap_level_upper-self.plot_colormap_level_space),
                                               clip=False)

# Plot map

        self.map_contourf = self.map.contourf(self.xmesh,
                                              self.ymesh,
                                              self.o3,
                                              self.color_levels,
                                              colors=None,            
                                              cmap=self.colormap,
                                              #norm=self.norm_range,
                                              extend="both")

# Add colour scale to output

        self.current_colorbar = mpl.pyplot.colorbar(orientation="horizontal",
                                                    fraction=0.05,
                                                    pad=0.15,
                                                    aspect=60.0,
                                                    shrink=1.0,
                                                    extend="both",
                                                    spacing="uniform",
                                                    ticks=self.color_levels,                                          
                                                    #ticks=None,
                                                    format=None)

        self.current_colorbar.set_label("Ozone scale in Dobson Units",
                                        fontsize=20)
        
# Write the output to a graphic file

        self.current_figure.savefig("bcbm3_plot2")
        #mpl.pyplot.close(self.current_figure)

        return(0)

#------------------------------------------------------------------------------

    def plot_colour_contours(self):
        if (self.verbose):
            sys.stdout.write("BCBM3 : plot_colour_contours ACTIVATED\n")


# Set up mesh for plotting

        self.xmesh, self.ymesh = self.map(*np.meshgrid(self.lon, self.lat))
        
        #sys.stdout.write("BCBM3 : self.xmesh = " + str(self.xmesh) + "\n")    
        #sys.stdout.write("BCBM3 : self.ymesh = " + str(self.ymesh) + "\n")    
    
# Set colour map and levels

        self.colormap = mpl_cm.jet
      
        self.colormap.set_under(color='k',
                                alpha=1.0)
        self.colormap.set_over(color='k',
                               alpha=1.0)  

# Set colour levels

        self.plot_colormap_level_lower = 200
        self.plot_colormap_level_upper = 525
        self.plot_colormap_level_space = 25
                                      
        self.color_levels = np.arange(self.plot_colormap_level_lower,
                                      self.plot_colormap_level_upper,
                                      self.plot_colormap_level_space)

# Set plotting of data outside color map range to display in (default=)black
# If this is not done then python will take the first and last colors of the colormap
# and apply them to data outside the range.
# IE.: It will effectively shorten the color scale by two colors
# and then rescale everything else to fit that shortened scale.
# Normalize : "clip" must be set to FALSE
# "alpha=1.0" means use solid color values
# "alpha" controls transparency, alpha=1=solid, alpha=0=transparent
# 0<alpha<1, range of transparent values

        self.norm_range = mpl.colors.Normalize(vmin=self.plot_colormap_level_lower,
                                               vmax=(self.plot_colormap_level_upper-self.plot_colormap_level_space),
                                               clip=False)

# Plot map

        self.map_contour = self.map.contour(self.xmesh,
                                            self.ymesh,
                                            self.o3,
                                            self.color_levels,
                                            colors=None,            
                                            cmap=self.colormap,
                                            #norm=self.norm_range,
                                            extend="both")

# Label the contours

        self.map_contour_label = mpl.pyplot.clabel(self.map_contour,
                                                   self.color_levels,
                                                   inline=1,
                                                   fontsize=9,
                                                   fmt='%1.0f',)
        
# Write the output to a graphic file

        self.current_figure.savefig("bcbm3_plot3")
        #mpl.pyplot.close(self.current_figure)

        return(0)

#------------------------------------------------------------------------------  

    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        bcbm3_cmd_line = sys.argv[1:]

    bcbm3     = Bcbm3()
    bcbm3_ret = bcbm3.bcbm3(bcbm3_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
