#!/usr/bin/env python

# Purpose :
# Read an HDF5 file and load its datasets to internal variables.
# This program is meant to be called as a module from other programs
# so they can access HDF5 format data.

# Ensure that environment variable PYTHONUNBUFFERED=yes
# This allows STDOUT and STDERR to both be logged in chronological order

import sys                       # platform, args, run tools
import os                        # platform, args, run tools

import argparse                  # For parsing command line
import h5py
import re

#########################################################################
# Command Line Parameters Class
#########################################################################

class H5datasetCP():

    def h5dataset_cp(self, h5dataset_cmd_line):        

        description = ("General purpose HDF5 file reader")
        parser = argparse.ArgumentParser(description=description)

        self.input_file_name = ""
        help_text = ("Input File Name")      
        parser.add_argument('input_file_name',
                            metavar='input_file_name',
                            #type=string,
                            help=help_text)

        self.action = "r"
        help_text = ("File open type action r:Read only, file must exist, r+:Read/write, file must exist " +
                     "(DEFAULT=r)")        
        parser.add_argument("-a", "--action",
                            default=self.action,
                            help=help_text,
                            action="store",
                            #type="string",                                
                            dest="action")

        help_text = ("Display processing messages to STDOUT (DEFAULT=NO)")        
        parser.add_argument("-v", "--verbose",
                            default=False,
                            help=help_text,
                            action="store_true",
                            dest="verbose")

        help_text = ("Run program in test mode (DEFAULT=NO)")        
        parser.add_argument("-t", "--test_mode",
                            default=False,
                            help=help_text,
                            action="store_true",
                            dest="test_mode")

        self.args = parser.parse_args(h5dataset_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("H5DATASET : h5dataset_cmd_line = " + str(h5dataset_cmd_line) + "\n")

        self.input_file_name = os.path.abspath(self.input_file_name.strip()) 

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class H5dataset():

    def h5dataset(self, h5dataset_cmd_line):
          
# Parse input parameters from cmd line

        h5datasetcp1     = H5datasetCP()
        h5datasetcp1_ret = h5datasetcp1.h5dataset_cp(h5dataset_cmd_line)        

        if (h5datasetcp1_ret):
            return(h5datasetcp1_ret)

        self.action           = h5datasetcp1.args.action    
        self.verbose          = h5datasetcp1.args.verbose                        
        self.test_mode        = h5datasetcp1.args.test_mode                
        self.input_file_name  = h5datasetcp1.args.input_file_name

        if (self.verbose):
            sys.stdout.write("H5DATASET : self.action           = " + str(self.action)           + "\n")
            sys.stdout.write("H5DATASET : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("H5DATASET : self.test_mode        = " + str(self.test_mode)        + "\n")
            sys.stdout.write("H5DATASET : self.input_file_name  = " + str(self.input_file_name)  + "\n")

        if (self.test_mode):
            if (self.verbose):            
                sys.stdout.write("H5DATASET : Running in test mode\n")
            
# Check file open action

        self.action = self.action.strip()
        self.action = self.action.lower()
        self.action_test = re.compile(r"r|r+")

        if (re.match(self.action_test, self.action)):
            pass     
        else:          
	    if (self.verbose):                                             
                sys.stderr.write("H5DATASET : ERROR : Unknown file open type action = " +
                                 str(self.action) + "\n")
                sys.stderr.write("H5DATASET : ERROR : Must be one of r|r+\n")
                sys.stderr.write("H5DATASET : ERROR : Defaulting to 'r'\n")
            self.action = "r" 

# Call functions

        pf1_ret = self.open_file()
        if (pf1_ret):
            return(pf1_ret)

        pf2_ret = self.process_file_attributes()
        if (pf2_ret):
            return(pf2_ret)

        pf3_ret = self.process_file_data()
        if (pf3_ret):
            return(pf3_ret)

# End program

        return(0)

# Define functions

#------------------------------------------------------------------------------

    def open_file(self):
        if (self.verbose):
            sys.stdout.write("H5DATASET : open_file ACTIVATED\n")

# Open input HDF file

        try:
            self.input_file = h5py.File(self.input_file_name, self.action)

        except Exception as inst:

            if (self.verbose):

                sys.stderr.write("H5DATASET : ERROR : type(inst) =  " + str(type(inst)) + "\n")
                sys.stderr.write("H5DATASET : ERROR : inst.args  =  " + str(inst.args)  + "\n")
                sys.stderr.write("H5DATASET : ERROR : inst       =  " + str(inst)       + "\n")

                sys.stderr.write("H5DATASET : ERROR : Cannot open file : " + str(self.input_file_name) + "\n")
                sys.stderr.write("H5DATASET : ERROR : File open type action : " + str(self.action) + "\n")                
                sys.stderr.write("H5DATASET : ERROR : Processing bypassed\n")

            return(2)

        return(0)

#------------------------------------------------------------------------------

    def process_file_attributes(self):
        if (self.verbose):
            sys.stdout.write("H5DATASET : process_file_attributes ACTIVATED\n")

        self.input_file_attr_names  = list(self.input_file.attrs)
        self.input_file_attr_values = list()

        for self.input_file_attr_name in self.input_file_attr_names:

            self.input_file_attr_values.append(self.input_file.attrs.__getitem__(self.input_file_attr_name))

            if (self.verbose):    
                sys.stdout.write("H5DATASET : self.input_file_attr_name = " + str(self.input_file_attr_name) + "\n")
                sys.stdout.write("H5DATASET : self.input_file.attrs.__getitem__(self.input_file_attr_name) = " +
                                 str(self.input_file.attrs.__getitem__(self.input_file_attr_name)) + "\n")

        if (self.verbose):    
            sys.stdout.write("H5DATASET : self.input_file_attr_names  = " + str(self.input_file_attr_names)  + "\n")
            sys.stdout.write("H5DATASET : self.input_file_attr_values = " + str(self.input_file_attr_values) + "\n")

        #os.sys.exit(0)

        return(0)
    
#------------------------------------------------------------------------------

    def process_file_data(self):
        if (self.verbose):
            sys.stdout.write("H5DATASET : process_file_data ACTIVATED\n")

# Make list of dataset names

        self.list_of_datasets = []
        self.list_of_groups   = []

        self.check_datasets("", self.input_file, 0)
        
        if (self.verbose):    
            for self.group_name in self.list_of_groups:
                sys.stdout.write("H5DATASET : self.group_name = " + str(self.group_name) + "\n")
            for self.dataset_name in self.list_of_datasets:
                sys.stdout.write("H5DATASET : self.dataset_name = " + str(self.dataset_name) + "\n")


        self.list_of_gpnames = [i1.replace("/", "", 1) for i1 in self.list_of_groups]
        self.list_of_gpnames = [i1.replace(" ", "_")   for i1 in self.list_of_gpnames] 
        self.list_of_gpnames = [i1.replace("/", "_")   for i1 in self.list_of_gpnames] 
        self.list_of_gpnames = [i1.replace("-", "_")   for i1 in self.list_of_gpnames]
        self.list_of_gpnames = [i1.replace(".", "_")   for i1 in self.list_of_gpnames]         

        self.list_of_dsnames = [i3.replace("/", "", 1) for i3 in self.list_of_datasets]
        self.list_of_dsnames = [i3.replace(" ", "_")   for i3 in self.list_of_dsnames] 
        self.list_of_dsnames = [i3.replace("/", "_")   for i3 in self.list_of_dsnames] 
        self.list_of_dsnames = [i3.replace("-", "_")   for i3 in self.list_of_dsnames]
        self.list_of_dsnames = [i3.replace(".", "_")   for i3 in self.list_of_dsnames]
        
        if (self.verbose):    
            sys.stdout.write("H5DATASET : self.list_of_gpnames = " + str(self.list_of_gpnames) + "\n")
            sys.stdout.write("H5DATASET : self.list_of_dsnames = " + str(self.list_of_dsnames) + "\n")

# Set group names as program attributes
 
        for i1, self.group_name in enumerate(self.list_of_groups):
            
            try:
                setattr(self, self.list_of_gpnames[i1], self.input_file.__getitem__(self.group_name))                
            except:
                if (self.verbose):                              
                    sys.stderr.write("H5DATASET : ERROR : Cannot read group : " +
                                     str(self.group_name) + "\n")
                    sys.stderr.write("H5DATASET : ERROR : Processing bypassed\n")                

# Set dataset names as program attributes

        for i3, self.dataset_name in enumerate(self.list_of_datasets):
            
            try:
                setattr(self, self.list_of_dsnames[i3], self.input_file[self.dataset_name].value)                
            except:
                if (self.verbose):                              
                    sys.stderr.write("H5DATASET : ERROR : Cannot read dataset : " +
                                     str(self.dataset_name) + "\n")
                    sys.stderr.write("H5DATASET : ERROR : Processing bypassed\n")      


        self.list_of_gpvars = ["self."+i3 for i3 in self.list_of_gpnames] 
        self.list_of_dsvars = ["self."+i4 for i4 in self.list_of_dsnames] 

# Display lists of group and dataset names

        if (self.verbose):   

            for self.gpname in self.list_of_gpvars:
                sys.stdout.write("H5DATASET : self.gpname = " + str(self.gpname) + "\n")
                
            for self.dsname in self.list_of_dsvars:
                sys.stdout.write("H5DATASET : self.dsname = " + str(self.dsname) + "\n")

# Close input HDF file

        # DO NOT CLOSE FILE HERE
        # CLOSING FILE BLOCKS READING OF ATTRIBUTES
        #self.input_file.close()

        return(0)

#------------------------------------------------------------------------------

    def check_datasets(self, InputPath, InputParent, Level):
        if (self.verbose):
            sys.stdout.write("H5DATASET : check_datasets ACTIVATED\n")

# This function adapted from original work by Dan Kahn (SSAI)

        InputChildren = list(InputParent)

        for InputChild in InputChildren:

            if isinstance(InputParent[InputChild], h5py.highlevel.Dataset):
                self.list_of_datasets.append(InputPath+"/"+InputChild)
        
            elif isinstance(InputParent[InputChild], h5py.highlevel.Group):
                self.list_of_groups.append(InputPath+"/"+InputChild)                
                self.check_datasets(InputPath+"/"+InputChild, InputParent[InputChild], Level+1)

            else:
                sys.stderr.write("H5DATASET : ERROR : Unknown object = " + str(InputChild) + "\n") 

        return(0)

####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        h5dataset_cmd_line = sys.argv[1:]

    h5ds1     = H5dataset()
    h5ds1_ret = h5ds1.h5dataset(h5dataset_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
