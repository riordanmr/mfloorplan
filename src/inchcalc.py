# inchcalc.py - simple calculator for inches and feet
# Mark Riordan   25-JUN-2025
# Usage: python3 inchcalc.py

import re

# distance is a string containing a distance in some combination of feet,
# inches, and fractional inches.  We parse it and return a floating point
# number of total inches.  If there's an error, we return None.
def parse_inches(distance):
    temp = distance.strip()
    inches = 0
    pattern = r"\"$"
    # remove trailing "
    if re.search(r"\"$",temp):        
        temp = temp[:-1]
    # Parse trailing fractional inches, if any.
    mymatch = re.search(r"\d+/\d+$", temp)
    if mymatch:
        frac = mymatch.group()
        inches = eval(frac)
        temp = temp[:-len(frac)]
        if temp.endswith(" "):
            temp = temp[:-1]
    # Deal with leading feet.
    patternFeet = r"^[+-]?((\d+(\.\d*)?)|(\.\d+))\'"
    mymatch = re.search(patternFeet, temp)
    if mymatch:
        feet = mymatch.group()
        temp = temp[len(feet):].strip()
        if feet.endswith("'"):
            feet = feet[:-1]
        inches += 12 * eval(feet)
    # Deal with the remaining, which should be only inches
    patternInches = r"^[+-]?((\d+(\.\d*)?)|(\.\d+))"
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

def do_calc():
    pass

def main():
    num = 0.0
    while True:
        user_input = input("Enter a distance (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        elif user_input.lower() == 'reset':
            num = 0.0
            print("Total inches reset to 0.")
            continue
        result = parse_inches(user_input)
        if result is not None:
            num = num + result
            print(f"Current total inches: {num}")
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()
# End of inchcalc.py