#!/usr/bin/env python

# Purpose : Skeleton Python program. 

# Ensure that environment variable PYTHONUNBUFFERED=yes
# This allows STDOUT and STDERR to both be logged in chronological order

import sys                       # platform, args, run tools
import os                        # platform, args, run tools
                                                    
import argparse                  # For parsing command line
import datetime                  # For date/time processing

#########################################################################
# Command Line Parameters Class
#########################################################################

class PyskelCP():

    def pyskel_cp(self, pyskel_cmd_line):        

        description = ("Skeleton Python program")
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

        self.args = parser.parse_args(pyskel_cmd_line)

        if (self.args.verbose):
            sys.stdout.write("PYSKEL : pyskel_cmd_line = " + str(pyskel_cmd_line) + "\n")

# Return

        return(0)

#########################################################################
# Main Program
#########################################################################

class Pyskel():

    def pyskel(self, pyskel_cmd_line):
          
# Start time

        self.start_time = datetime.datetime.today()

# Parse input parameters from cmd line

        pyskel_cp1     = PyskelCP()
        pyskel_cp1_ret = pyskel_cp1.pyskel_cp(pyskel_cmd_line)        

        self.pyskel_cmd_line = pyskel_cmd_line
        if (len(self.pyskel_cmd_line) == 0):
            self.pyskel_cmd_line = " " 

        if (pyskel_cp1_ret):
            return(pyskel_cp1_ret)

        self.verbose          = pyskel_cp1.args.verbose                        
        self.test_mode        = pyskel_cp1.args.test_mode                
        self.input_file_name  = pyskel_cp1.args.input_file_name

        if (self.test_mode):
            self.timestamp = "Test Mode Date/Time Stamp"
            if (self.verbose):                
                sys.stdout.write("PYSKEL : Running in test mode\n")
                sys.stdout.write("PYSKEL : sys.version = " + str(sys.version) + "\n")                     
        else:
            self.timestamp = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            if (self.verbose):                   
                sys.stdout.write("PYSKEL : Program started : " + str(self.start_time) + "\n")
                sys.stdout.write("PYSKEL : sys.version     = " + str(sys.version)     + "\n")

        if (self.verbose):
            sys.stdout.write("PYSKEL : sys.version           = " + str(sys.version)           + "\n")     
            sys.stdout.write("PYSKEL : self.verbose          = " + str(self.verbose)          + "\n")
            sys.stdout.write("PYSKEL : self.test_mode        = " + str(self.test_mode)        + "\n")
            sys.stdout.write("PYSKEL : self.input_file_name  = " + str(self.input_file_name)  + "\n")

# Call functions

        pyskel_f11_ret = self.function1()
        if (pyskel_f11_ret):
            return(pyskel_f11_ret)

        pyskel_f21_ret = self.function2()
        if (pyskel_f21_ret):
            return(pyskel_f21_ret)

# End program

        self.end_time = datetime.datetime.today()
        self.run_time = self.end_time - self.start_time 

        if (self.verbose):
            if (self.test_mode):
                pass
            else:
                sys.stdout.write("PYSKEL : Program ended : " + str(self.end_time) + "\n")  
                sys.stdout.write("PYSKEL : Run time      : " + str(self.run_time) + "\n")

        if (self.verbose):                       
            sys.stdout.write("PYSKEL : Program completed normally\n")
            
        return(0)

# Define functions

#------------------------------------------------------------------------------

    def function1(self):
        if (self.verbose):
            sys.stdout.write("PYSKEL : function1 ACTIVATED\n")

        return(0)
    
#------------------------------------------------------------------------------

    def function2(self):
        if (self.verbose):
            sys.stdout.write("PYSKEL : function2 ACTIVATED\n")

        return(0)

    
####################################################

def main(argv=None):  # When run as a script

    if argv is None:
        pyskel_cmd_line = sys.argv[1:]

    pysk1     = Pyskel()
    pysk1_ret = pysk1.pyskel(pyskel_cmd_line)    

if __name__ == '__main__':                           
    sys.exit(main())
