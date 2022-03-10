# mfloorplan.py - program to read an input file describing a floor plan and
# create a graphics file with a rendering of that floor plan.
# The input file contains a list of commands.  Currently the input file is in 
# CSV format.
# The output file is in SVG (Scaled Vector Graphics) format.
#
# Mark Riordan  2022-03-10

import argparse
import csv

# Returns a tuple with success,values
def parse_cmd_line():
    dict_args = dict()
    success = True
    parser = argparse.ArgumentParser(
        description="Create a SVG file depicting a floor plan")
    parser.add_argument("--infile", type=str, required=True, 
        help="name of input CSV file")
    parser.add_argument("--outfile", type=str, required=True, 
        help="name of output SVG file")
    args = parser.parse_args()
    dict_args["infile"] = args.infile
    dict_args["outfile"] = args.outfile
    return success

def main():
    success, dict_args = parse_cmd_line()

main()
