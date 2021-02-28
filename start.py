#!/usr/bin/env python3
# coding=utf-8
import os.path
import sys
import Assembler

# --------------------------------
#   Marco Ravelo
#   CSCE 434 - Compiler Design
#   Assignment #2 - 2/10/2021 
#   file: start.py
# --------------------------------

# Resources used:

if __name__ == '__main__':
        
    assember_opts = []

    # command line arguments
    if ('-help' in sys.argv):
        print ('\twrite help stuff here...')
        sys.exit()
    if ('-print' in sys.argv):
        assember_opts.append('-print')

    while (True):
        # prompt user for input file name
        input_file = input ('Input file name [Press \'Enter\' to user default - input.txt]: ')

        # check if blank, change to default
        if (input_file == ''):
            input_file = 'input.txt'

        if (os.path.isfile(input_file)):
            break
        else:
            print ('ImportError: could not find file', input_file)

    print ('Found file', input_file)

    # open file and read all lines (removing any '\n' chars)
    with open (input_file, 'r') as open_file:
        lines = open_file.readlines()
    
    assembler = Assembler.MyAssember(assember_opts)
    code = assembler.start(lines)

    # open output file and write code to it
    with open ('a.bin', 'wb+') as output_file:
        for line in code:
            output_file.write(line)