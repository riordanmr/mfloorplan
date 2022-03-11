# mfloorplan.py - program to read an input file describing a floor plan and
# create a graphics file with a rendering of that floor plan.
# The input file contains a list of commands.  Currently the input file is in 
# CSV format.
# The output file is in SVG (Scaled Vector Graphics) format.
#
# Mark Riordan  2022-03-10

import argparse
import csv
import re

# Returns a tuple with success,dictionary_of_values
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
    return success, dict_args

# distance is a string containing a distance in some combination of feet,
# inches, and fractional inches.  We parse it and return a floating point
# number of total inches. 
def parse_inches(distance):
    print("parse of " + distance)
    temp = distance
    inches = 0
    pattern = "\"$"
    # print("pattern=",pattern)parse_inches
    if re.search("\"$",temp):
        # remove trailing "
        temp = temp[:-1]
    mymatch = re.search("\d+/\d+$", temp)
    if mymatch:
        print(mymatch)
        frac = mymatch.group()
        print(frac)
        inches = eval(frac)
        temp = temp[:-len(frac)]
        if temp.endswith(" "):
            temp = temp[:-1]
        print("changed temp to ="+temp+"=")
    print("Returning ",inches)
    return inches

def do_rect(id,label,x,y,objrel,otherid,otherrel,relx,rely):
    pass

def process_cmd(cmd, row):
    if(cmd=="rect"):
        # rect,outline,myoutline,341 5/16,993 13/16,ul,origin,ul,0,0
        if len(row) != 10:
            print("Bad number of args for rect")
        else:
            do_rect(row[1], row[2], row[3], row[4], row[5], row[6],row[7],row[8],row[9])

    else:
        print("Bad cmd " + cmd)
    

def read_csv_file(dict_args):
    infile = dict_args["infile"]
    print("About to read " + dict_args["infile"])
    with open(infile, newline='') as csvfile:
        csvreader = csv.reader(csvfile, quoting=csv.QUOTE_NONE)
        for row in csvreader:
            cmd = row[0]
            process_cmd(cmd, row)
            pass
    return

def test_parse_inches():
    result = parse_inches("2' 4 7/8\"")
    result = parse_inches("2' 4 7/8")
    pass

def main():
    test_parse_inches()
    success, dict_args = parse_cmd_line()
    read_csv_file(dict_args)

main()
