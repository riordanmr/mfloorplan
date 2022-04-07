# mfloorplan.py - program to read an input file describing a floor plan and
# create a graphics file with a rendering of that floor plan.
# The input file contains a list of commands.  Currently the input file is in 
# CSV format.
# The output file is in SVG (Scaled Vector Graphics) format.
#
# Mark Riordan  2022-03-10

import argparse
import re

xoffset = 12
yoffset = 12
total_width = 1050
total_height = 480
current_class = ""
list_classes = [current_class]
dict_vectors = dict()
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
    parser.add_argument("--cssfile", type=str, required=False, 
        help="name of optional existing CSS file to reference")
    args = parser.parse_args()
    dict_args["infile"] = args.infile
    dict_args["outfile"] = args.outfile
    dict_args["cssfile"] = args.cssfile
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

def concat_list(mylist):
    msg = ""
    for token in mylist:
        msg += token + " "
    return msg

# Draw the text in "label" in the object given by dictIds[objid]
def draw_label(objid,label):
    # To draw a horizontal label, generate an SVG element like this:
    #   <text text-anchor="middle" dominant-baseline="central" transform="translate(xcenter,ycenter) rotate(0)">label</text>
    # To draw a vertical label, generate an SVG element like this:
    #   <text text-anchor="middle" dominant-baseline="central" transform="translate(xcenter,ycenter) rotate(-90)">label</text>
    # For now, we'll draw only horizontal labels.
    rect = dictIds[objid]
    xcenter = rect.x + 0.5*rect.width
    ycenter = rect.y + 0.5*rect.height
    # Use horizontal if the width is greater than the height, or almost so.
    if (1.2*rect.width) >= rect.height:
        line = f'<text text-anchor="middle" dominant-baseline="central" transform="translate({xcenter},{ycenter}) rotate(0)"'
    else:
        # Use vertical.
        line = f'<text text-anchor="middle" dominant-baseline="central" transform="translate({xcenter},{ycenter}) rotate(-90)"'

    # I removed code to add  f' class="{current_class}"'  because the results were unreadable.
    line += ">"
    line += f'{label}</text>'
    write_line(line)

def do_rect(id,label,width,height,objrel,otherid,otherrel,relx,rely):
    global dictIds, xoffset, yoffset, total_width, total_height, stroke_width

    width = parse_inches(width) 
    height = parse_inches(height) 
    relx = parse_inches(relx) 
    rely = parse_inches(rely)
    
    if otherid == "origin":
        other_room = Room()
        other_room.x = xoffset
        other_room.y = yoffset
        other_room.width = total_width
        other_room.height = total_height
    else:
        if otherid not in dictIds:
            print(f"** Unknown otherid {otherid} for {id}")
            return None
            
        other_room = dictIds[otherid]

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
        x = other_room.x + other_room.width - width + relx
        y = other_room.y + other_room.height - height + rely
    elif objrel == "lr" and otherrel == "ul":
        x = other_room.x - width + relx
        y = other_room.y - height + rely
    elif objrel == "lr" and otherrel == "ur":
        x = other_room.x + other_room.width - width + relx
        y = other_room.y - height + rely
    elif objrel == "ul" and otherrel == "ll":
        x = other_room.x + relx
        y = other_room.y + other_room.height + rely
    elif objrel == "ll" and otherrel == "ll":
        x = other_room.x + relx
        y = other_room.y + other_room.height - height + rely
    elif objrel == "ll" and otherrel == "lr":
        x = other_room.x + other_room.width + relx
        y = other_room.y + other_room.height - height + rely
    elif objrel == "ul" and otherrel == "ur":
        x = other_room.x + other_room.width + relx
        y = other_room.y + rely
    elif objrel == "ur" and otherrel == "ur":
        x = other_room.x + other_room.width - width + relx
        y = other_room.y + rely
    elif objrel == "ll" and otherrel == "ul":
        x = other_room.x + relx
        y = other_room.y - height + rely
    elif objrel == "ll" and otherrel == "ur":
        x = other_room.x + other_room.width + relx
        y = other_room.y + rely
    elif objrel == "ur" and otherrel == "lr":
        x = other_room.x + relx
        y = other_room.y + other_room.height + rely
    # elif objrel == "ul" and otherrel == "ur":
    #     x = other_room.x + other_room.width - width + relx
    #     y = other_room.y + rely
    elif objrel == "lr" and otherrel == "ll":
        x = other_room.x - width + relx
        y = other_room.y + other_room.height - height + rely
    else:
        print(f"** for {id} unrecognized objrel {objrel} otherrel {otherrel}")

    thisObj = Room()
    thisObj.x = x
    thisObj.y = y
    thisObj.width = width
    thisObj.height = height
    dictIds[id] = thisObj

    line = f'<rect id="{id}" x="{x}" y="{y}" width="{width}" height="{height}"'
    if len(current_class) > 0:
        line += f' class="{current_class}"'
    line += "/>"
    dict_vectors[id] = line
    write_line(line)

    if label != "":
        draw_label(id, label)

def do_class(new_class):
    global current_class, list_classes
    if new_class=="prev" or new_class=="pop":
        current_class = list_classes.pop()
    else:
        list_classes.append(current_class)
        current_class = new_class

def do_repeat(id):
    global dict_vectors
    line = dict_vectors[id]
    write_line(line)

def process_cmd(cmd, row):
    if cmd=="rect":
        # rect,outline,myoutline,993 13/16,341 5/16,ul,origin,ul,0,0
        if len(row) != 10:
            print("Bad number of args for rect: " + concat_list(row))
        else:
            do_rect(row[1], row[2], row[3], row[4], row[5], row[6],row[7],row[8],row[9])
    elif cmd is None or cmd.startswith("#") or len(cmd)==0:
        # Ignore comments
        pass
    elif cmd=="class":
        if len(row) != 2:
            print("Bad number of args for class: " + concat_list(row))
        else:
            do_class(row[1])
    elif cmd=="repeat":
        if len(row) != 2:
            print("Bad number of args for repeat: " + concat_list(row))
        else:
            do_repeat(row[1])
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
    if "cssfile" in dict_args:
        cssfile = dict_args["cssfile"]
        write_line(f'<?xml-stylesheet type="text/css" href="{cssfile}"?>')
    write_line(f'<svg width="{total_width}" height="{total_height}" version="1.1" xmlns="http://www.w3.org/2000/svg">')

def write_file_footer():
    write_line("</svg>")

def read_csv_file(dict_args):
    infile = dict_args["infile"]
    print("About to read " + dict_args["infile"])
    with open(infile, newline='') as csvfile:
        # The csv class sucks.  It gives unpredictable errors under unknown
        # irreproducible circumstances.  So I'll stop using it.  
        #csvreader = csv.reader(csvfile, quoting=csv.QUOTE_NONE)
        write_file_header(dict_args)
        for line in csvfile:
            #stripped_line = line.rstrip("\n")
            #print(f"Processing {stripped_line}")
            row = line.rstrip("\n").strip().split(",")
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
