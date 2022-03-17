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

xoffset = 12
yoffset = 12
total_width = 1050
total_height = 390
stroke_width = 5
svgfile = None
dictIds = dict()

class Room:
    pass

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
# number of total inches.  If there's an error, we return None.
def parse_inches(distance):
    temp = distance.strip()
    inches = 0
    pattern = "\"$"
    # remove trailing "
    if re.search("\"$",temp):        
        temp = temp[:-1]
    # Parse trailing fractional inches, if any.
    mymatch = re.search("\d+/\d+$", temp)
    if mymatch:
        frac = mymatch.group()
        inches = eval(frac)
        temp = temp[:-len(frac)]
        if temp.endswith(" "):
            temp = temp[:-1]
    # Deal with leading feet.
    patternFeet = "^[+-]?((\d+(\.\d*)?)|(\.\d+))\'"
    mymatch = re.search(patternFeet, temp)
    if mymatch:
        feet = mymatch.group()
        temp = temp[len(feet):].strip()
        if feet.endswith("'"):
            feet = feet[:-1]
        inches += 12 * eval(feet)
    # Deal with the remaining, which should be only inches
    patternInches = "^[+-]?((\d+(\.\d*)?)|(\.\d+))"
    mymatch = re.search(patternInches, temp)
    if mymatch:
        thisInches = mymatch.group()
        temp = temp[len(thisInches):].strip()
        if thisInches.endswith("\""):
            thisInches = thisInches[:-1]
        inches += eval(thisInches)
    # Ensure there's no extra garbage.
    temp = temp.strip()
    if len(temp) > 0:
        print("** Error: for " + distance + " temp is =" + temp + "=; should be empty")
        inches = None
    return inches

def do_rect(id,label,width,height,objrel,otherid,otherrel,relx,rely):
    global dictIds, xoffset, yoffset, total_width, total_height, stroke_width

    width = parse_inches(width) + xoffset
    height = parse_inches(height) + yoffset
    relx = parse_inches(relx) 
    rely = parse_inches(rely)
    
    if otherid == "origin":
        other_room = Room()
        other_room.x = xoffset
        other_room.y = yoffset
        other_room.width = total_width
        other_room.height = total_height
    else:
        other_room = dictIds[otherid]
        if other_room is None:
            print("** Cannot find id " + otherid)
    # The coordinate system has (0,0) at the upper left.
    # - ll = lower left
    # - ul = upper left
    # - lr = lower right
    # - ur = upper right

    x = 0
    y = 0
    if objrel == "ul" and otherrel == "ul":
        x = other_room.x + relx 
        y = other_room.y + rely
    elif objrel == "lr" and otherrel == "lr":
        #print(f"{id} lower right: other x={other_room.x} other width={other_room.width} width={width} relx={relx}")
        x = other_room.x + other_room.width - width + relx
        y = other_room.y + other_room.height - height + rely
        #x -= stroke_width
        #y -= stroke_width
    elif objrel == "lr" and otherrel == "ur":
        x = other_room.x + other_room.width - width + relx
        y = other_room.y - height + rely
    elif objrel == "ul" and otherrel == "ll":
        x = other_room.x + relx
        y = other_room.y + other_room.height + rely
    elif objrel == "ll" and otherrel == "ll":
        x = other_room.x + relx
        y = other_room.y + other_room.height - height + rely        
    else:
        print(f"** Unrecognized objrel {objrel} otherrel {otherrel}")

    thisObj = Room()
    thisObj.x = x
    thisObj.y = y
    thisObj.width = width
    thisObj.height = height
    dictIds[id] = thisObj

    line = f'<rect id="{id}" x="{x}" y="{y}" width="{width}" height="{height}"' + \
        f' stroke-width="{stroke_width}" stroke="black" fill="transparent"/>'
    write_line(line)

def process_cmd(cmd, row):
    if cmd=="rect":
        # rect,outline,myoutline,993 13/16,341 5/16,ul,origin,ul,0,0
        if len(row) != 10:
            print("Bad number of args for rect")
        else:
            do_rect(row[1], row[2], row[3], row[4], row[5], row[6],row[7],row[8],row[9])
    elif cmd is None or cmd.startswith("#"):
        # Ignore comments
        pass
    else:
        print("Bad cmd " + cmd)

def write_line(txt):
    global svgfile
    svgfile.write(txt)
    svgfile.write("\n")

def write_file_header(dict_args):
    global svgfile
    outfile = dict_args["outfile"]
    svgfile = open(outfile, "w")
    write_line(f'<svg width="{total_width}" height="{total_height}" version="1.1" xmlns="http://www.w3.org/2000/svg">')

def write_file_footer():
    write_line("</svg>")

def read_csv_file(dict_args):
    infile = dict_args["infile"]
    print("About to read " + dict_args["infile"])
    with open(infile, newline='') as csvfile:
        csvreader = csv.reader(csvfile, quoting=csv.QUOTE_NONE)
        write_file_header(dict_args)
        for row in csvreader:
            cmd = row[0]
            process_cmd(cmd, row)
            pass
    write_file_footer()
    return

# Unit test for parsing of distances.
# The results must be inspected manually.
def test_parse_inches():
    list_fractions = ["341 5/16", "2' 4 7/8\"", "2' 4 7/8", 
        "2.3'", "2'", "34' 4 5/8", "34' 4\"", "32.14", "23 3/4", "a23"]
    for item in list_fractions:
        result = parse_inches(item)
        print(item + " = " + str(result))

def test_all():
    test_parse_inches()

def main():
    #test_all()
    success, dict_args = parse_cmd_line()
    read_csv_file(dict_args)

main()
