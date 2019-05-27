# Implementation of the input CLI.
import argparse, sys, os
from input_module import *
from Input_tool import *
from Input_tool_cmd import *
#def _parseArguments():
#    searchDict = {}

# Defines and describes the arguments of the helper. Optional ones are defined with '--name', and obligatory ones are defined with only 'name'
parser = argparse.ArgumentParser(description='What do you want to do?')

parser.add_argument('-i','--input', help='Use this option to insert a file to the database', default=False, dest='input', action='store_true')    # Correct?     
parser.add_argument('-d','--delete', help='Use this option to delete a file from the database') # Correct?
parser.add_argument('-fl','--flush', help='Use this option to flush a file from the database', default=False, dest ='flush', action='store_true')  # Correct?
parser.add_argument('-cmd','--command', nargs='+', help='Use this option to upload a ts and an xml to the database. The format is the path and the name of both files separated by a space.')             # Correct?
parser.add_argument('--ignoreErrors', help='Activate this flag to ignore all possible errors and insert all files to the database anyways', default=False, dest='ignoreErrors', action='store_true')
parser.add_argument('--automatize', help='Activate this flag to get a report of the possible errors but insert all files to the database anyways', default=False, dest='automatize', action='store_true')
args = parser.parse_args()

if args.input:
    input_tool(args.ignoreErrors, args.automatize)
if args.delete:
    xml_name = args.delete
    delete(xml_name)

if args.flush:
    flush()

if args.command:
    if len(args.command) != 4:
        parser.error('Wrong number of arguments')
    else:
        pathts = args.command[0]
        ts = args.command[1]
        pathxml = args.command[2]
        xml = args.command[3]
        cmd_input(pathts, ts, pathxml,xml)
