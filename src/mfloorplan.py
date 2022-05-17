# mfloorplan.py - program to read an input file describing a floor plan and
# create a graphics file with a rendering of that floor plan.
# The input file contains commands used to describe the floor plan, 
# in CSV format. 
# The output file is in SVG (Scaled Vector Graphics) format.
#
# The commands take the format:
#   commandName,arg1,arg2,...
# Not all commands take the same number of arguments, so this is kind of a 
# weird CSV file.
# Height and width in most cases are meant to be in inches, or feet and inches.
# However, in actuality the units are arbitrary.
#
#-----------------------------------------------------------------------------
# The commands are:
# imagesize,width,height
#   Specifies the image size.  Must be the first non-comment command.
#   where width and height are the total size of the image in pixels.
#
# rect,id,name,width,height,mycorner,otherid,othercorner,relativeX,relativeY 
#   Causes a rectangle to be drawn.
#   id is the id of this (new) rectangle.  It can contain letters, digits,
#     and _. Ids are case-sensitive and must start with a letter.
#     (These rules are not yet 100% enforced yet.)
#   name is the human-friendly name; some advanced version of the app will 
#     draw this.  Can be empty.
#   width is the width
#   height is the height of the rectangle; see below for the syntax and units
#   mycorner is the corner of this new rectangle which will be used for 
#     relative positioning.  It's one of ll, ul, lr, ur
#   otherid is the id of another, existing rectangle.  The special id "origin"
#     indicates the upper left corner of the image.
#   othercorner is the corner of that other rectangle which will be used for 
#     relative positioning.  It is ignored for the otherid "origin". 
#   relativeX is the relative horizontal position of the new rectangle w.r.t. 
#     the other rectangle.  Units are as described below, with the addition 
#     that negative numbers indicate a position to the left
#   relativeY is the relative vertical position of the new rectangle w.r.t. 
#     the other rectangle.  Units are as described below, with the addition 
#     that negative numbers indicate a position above.
#
# class,classes
#   Sets the CSS class(es) to be used from this point on (to the next)
#   class command.  This applies to objects other than text.
#   classes is a blank-separated list of CSS class names.
#
# textclass,classes
#   Sets the CSS class(es) to be used from this point on (to the next)
#   textclass command.  This applies only to text.
#
# repeat,id
#   Redraws the object with the given id, using the current classes.
#   This can be used when two objects overlap.
#-----------------------------------------------------------------------------
#
#  The default unit is inches, and partial inches can be specified via both 
# decimal places and fractions (like 5/16).   Feet and inches can also be 
# specified.  Decimal places are allowed on both feet and inches, though 
# they are not encouraged.
#
# Here are some valid sizes and their meanings:
# 12 means 12 inches
# 12 5/16 means 12 and 5/16 inches
# 14' means 14 feet
# 14' 6 means 14 feet and 6 inches
# 14' 6 5/16 means 14 feet and 6 and 5/16 inches
#
# Mark Riordan  2022-03-10

import argparse
import re
from datetime import datetime

xoffset = 12
yoffset = 12
total_width = 0
total_height = 0
current_class = ""
current_text_class = ""
list_classes = [current_class]
list_text_classes = [current_text_class]
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
    parser.add_argument("--skelfile", type=str, required=True,
        help="name of input HTML skeleton file")
    parser.add_argument("--htmlfile", type=str, required=True,
        help="name of output HTML file")
    parser.add_argument("--cssfile", type=str, required=False, 
        help="name of optional existing CSS file to reference")
    args = parser.parse_args()
    dict_args["infile"] = args.infile
    dict_args["outfile"] = args.outfile
    dict_args["cssfile"] = args.cssfile
    dict_args["skelfile"] = args.skelfile
    dict_args["htmlfile"] = args.htmlfile
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

def get_timestamp():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return current_time

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

    if current_text_class != "":
        line += f' class="{current_text_class}"'
    line += ">"
    line += f'{label}</text>'
    write_line(line)

# Process the "rect" command by writing directives to the SVG file
# which cause a rectange to be drawn.
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
        y = other_room.y - height + rely
    elif objrel == "ur" and otherrel == "lr":
        x = other_room.x + other_room.width - width + relx
        y = other_room.y + other_room.height + rely
    elif objrel == "ur" and otherrel == "ul":
         x = other_room.x - width + relx
         y = other_room.y + rely
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

def do_textclass(new_class):
    global current_text_class, list_text_classes
    if new_class=="prev" or new_class=="pop":
        current_text_class = list_text_classes.pop()
    else:
        list_text_classes.append(current_text_class)
        current_text_class = new_class

def do_imagesize(sizex, sizey):
    global total_width, total_height
    if total_width == 0:
        total_width = sizex
        total_height = sizey
        write_line(f'<svg width="{total_width}" height="{total_height}" version="1.1" xmlns="http://www.w3.org/2000/svg">')
        write_line(f"<!-- Rendered {get_timestamp()} by mfloorplan.py https://github.com/riordanmr/mfloorplan -->")
    else:
        print("Error in imagesize: image size has already been set")

def do_repeat(id):
    global dict_vectors
    line = dict_vectors[id]
    write_line(line)

# Process a command.
# Entry:    cmd     is the command, e.g., "rect"
#           row     is a list of the command name and its arguments.
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
    elif cmd=="textclass":
        if len(row) != 2:
            print("Bad number of args for textclass: " + concat_list(row))
        else:
            do_textclass(row[1])
    elif cmd=="repeat":
        if len(row) != 2:
            print("Bad number of args for repeat: " + concat_list(row))
        else:
            do_repeat(row[1])
    elif cmd=="imagesize":
        if len(row) != 3:
            print("Bad number of args for {cmd}: " + concat_list(row))
        else:
            do_imagesize(row[1], row[2])
    else:
        print("Bad cmd " + cmd)

# Write a line of text to the SVG file.
# We append a newline to the line.
# Entry:    txt is the line of text to write. 
def write_line(txt):
    global svgfile
    svgfile.write(txt)
    svgfile.write("\n")

# Open the output SVG file and write the header.
# Entry:    dict_args["outfile"] is the name of the output file.
#           dict_args["cssfile"] is the name of the CSS file being used;
#               this will be reference in the SVG file.
# Exit:     svgfile is the file handle for the SVG output file.
def write_file_header(dict_args):
    global svgfile
    outfile = dict_args["outfile"]
    svgfile = open(outfile, "w")
    if "cssfile" in dict_args:
        cssfile = dict_args["cssfile"]
        write_line(f'<?xml-stylesheet type="text/css" href="{cssfile}"?>')

def write_file_footer():
    write_line("</svg>")

def read_csv_file(dict_args):
    global total_width
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
    if total_width==0:
        print("Error: no  imagesize  command found")
    write_file_footer()
    return

# Create an HTML file from an HTML skeleton input file.
# Certain patterns in the input file are replaced with runtime values.
# Entry:    dict_args["skelfile"] is the name of the input skeleton file.
#           dict_args["htmlfile"] is the name of the output file.
def process_skel_file(dict_args):
    stamp = datetime.today().strftime('%Y-%m-%d')
    with open(dict_args["htmlfile"], "w") as htmlfile:
        with open(dict_args["skelfile"], newline='') as skelfile:
            for line in skelfile:
                finalLine = line.replace("@[DATE@]", stamp)
                htmlfile.write(finalLine)
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
    process_skel_file(dict_args)

main()
