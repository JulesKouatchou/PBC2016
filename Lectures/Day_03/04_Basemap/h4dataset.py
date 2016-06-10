#!/usr/bin/env python

# Purpose :
# Read an HDF4 file and load its datasets to internal variables.
# This program is meant to be called as a module from other programs
# so they can access HDF4 format data.

# Ensure that environment variable PYTHONUNBUFFERED=yes
# This allows STDOUT and STDERR to both be logged in chronological order

import sys                       # platform, args, run tools
import os                        # platform, args, run tools
                                                    
import argparse                  # For parsing command line
import re

from pyhdf import SD             # Needed for HDF4 type files

#########################################################################
# Command Line Parameters Class
#########################################################################

class H4datasetCP():

    def h4dataset_cp(self, h4dataset_cmd_line):        

        description = ("Read an HDF4 file and load its datasets")
        parser = argparse.ArgumentParser(description=description)

        help_text = ("Input file name")      
        parser.add_argument('input_file_name',
                            metavar='input_file_name',
                            #type=string,
                            help=help_text)

        nowpath = os.path.abspath(os.path.dirname(__file__))
        default_yaml = nowpath + "/h4dataset.yaml"

        self.action = "r"
        help_text = ("File open type action r:Read only, file must exist, r+:Read/write, file must exist " +
                     "(DEFAULT=r)")        
        parser.add_argument("-a", "--action",
                            default=self.action,
                            help=help_text,
                            action="store",
                            #type="string",                                
                            dest="action")

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

        self.args  = parser.parse_args(h4dataset_cmd_line)  

        if (self.args.verbose):
            sys.stdout.write("H4DATASET : h4dataset_cmd_line = " + str(h4dataset_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class H4dataset():

    def h4dataset(self, h4dataset_cmd_line):
          
# Parse input parameters from cmd line

        h4datasetcp1     = H4datasetCP()
        h4datasetcp1_ret = h4datasetcp1.h4dataset_cp(h4dataset_cmd_line)        

        if (h4datasetcp1_ret):
            return(h4datasetcp1_ret)

        self.action           = h4datasetcp1.args.action    
        self.verbose          = h4datasetcp1.args.verbose                        
        self.test_mode        = h4datasetcp1.args.test_mode                
        self.input_file_name  = os.path.abspath(h4datasetcp1.args.input_file_name.strip())

        if (self.verbose):
            sys.stdout.write("H4DATASET : self.action           = " + str(self.action)           + "\n")
            sys.stdout.write("H4DATASET : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("H4DATASET : self.test_mode        = " + str(self.test_mode)        + "\n")
            sys.stdout.write("H4DATASET : self.input_file_name  = " + str(self.input_file_name)  + "\n")

        if (self.test_mode):
            if (self.verbose):            
                sys.stdout.write("H4DATASET : Running in test mode\n")

# Check file open action

        self.action = self.action.strip()
        self.action = self.action.lower()
        self.action_test = re.compile(r"r|r+")

        if (re.match(self.action_test, self.action)):
            pass     
        else:          
	    if (self.verbose):                                             
                sys.stderr.write("H4DATASET : ERROR : Unknown file open type action = " +
                                 str(self.action) + "\n")
                sys.stderr.write("H4DATASET : ERROR : Must be one of r|r+\n")
                sys.stderr.write("H4DATASET : ERROR : Defaulting to 'r'\n")
            self.action = "r" 

# Call functions

        pf1_ret = self.process_file()
        if (pf1_ret):
            return(pf1_ret)

# End program

        return(0)

# Define functions

#------------------------------------------------------------------------------

    def process_file(self):
        if (self.verbose):
            sys.stdout.write("H4DATASET : process_file ACTIVATED\n")

# Open the HDF4 file for reading

        try:
            
            self.input_file = SD.SD(self.input_file_name)
            
        except Exception as inst:

            if (self.verbose):

                sys.stderr.write("H4DATASET : ERROR : type(inst) =  " + str(type(inst)) + "\n")
                sys.stderr.write("H4DATASET : ERROR : inst.args  =  " + str(inst.args)  + "\n")
                sys.stderr.write("H4DATASET : ERROR : inst       =  " + str(inst)       + "\n")

                sys.stderr.write("H4DATASET : ERROR : Cannot open file : " + str(self.input_file_name) + "\n")               
                sys.stderr.write("H4DATASET : ERROR : File open type action : " + str(self.action) + "\n")                
                sys.stderr.write("H4DATASET : ERROR : Processing bypassed\n")

            return(2)

# Make list of dataset names

        self.list_of_datasets = self.input_file.datasets().keys()

        if (self.verbose):    
           for dataset_name in self.list_of_datasets:
                sys.stdout.write("H4DATASET : dataset_name = " + str(dataset_name) + "\n")


        self.list_of_dsnames = [i1.replace(" ", "_") for i1 in self.list_of_datasets]
        self.list_of_dsnames = [i1.replace("-", "_") for i1 in self.list_of_datasets]        


        if (self.verbose):    
            sys.stdout.write("H4DATASET : self.input_file.datasets().keys()   = " + str(self.input_file.datasets().keys())   + "\n")
            sys.stdout.write("H4DATASET : self.input_file.datasets().values() = " + str(self.input_file.datasets().values()) + "\n")
        
        #os.sys.exit(0)
        
# Read the dataset

        for i2, self.dataset_name in enumerate(self.list_of_datasets):
            
            try:
                
                self.dataset_get    = self.input_file.select(self.dataset_name).get()
                
                setattr(self, self.list_of_dsnames[i2], self.dataset_get)                
            
            except Exception as inst:

                if (self.verbose):

                    sys.stderr.write("H4DATASET : ERROR : type(inst) =  " + str(type(inst)) + "\n")
                    sys.stderr.write("H4DATASET : ERROR : inst.args  =  " + str(inst.args)  + "\n")
                    sys.stderr.write("H4DATASET : ERROR : inst       =  " + str(inst)       + "\n")
                    
                    sys.stderr.write("H4DATASET : ERROR : Cannot open dataset " + str(self.dataset_name) + "\n")               
                    sys.stderr.write("H4DATASET : ERROR : File open type action : " + str(self.action) + "\n")                
                    sys.stderr.write("H4DATASET : ERROR : Processing bypassed\n")


        self.list_of_dsvars = ["self."+i3 for i3 in self.list_of_dsnames] 
        if (self.verbose):   
            for self.dsname in self.list_of_dsvars:
                sys.stdout.write("H4DATASET : self.dsname         = " + str(self.dsname) + "\n")
     
        return(0)
    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        h4dataset_cmd_line = sys.argv[1:]

    h4ds1     = H4dataset()
    h4ds1_ret = h4ds1.h4dataset(h4dataset_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
