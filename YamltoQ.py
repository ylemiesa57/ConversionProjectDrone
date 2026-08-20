"""
Conversion tool to transform YAML mission files into QGroundControl plan files.

This script reads a YAML file containing UAV navigation task definitions,
extracts polygon waypoint coordinates, applies geographic coordinate transformations,
and inserts the converted coordinates into a QGroundControl mission plan template.
"""
import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


yaml_lines = []


def convertPolygonPoints(lines):
    """
    Extract x and y coordinates from YAML position strings.
    
    Parses lines containing YAML position data in the format:
        position: { x: VALUE, y: VALUE, z: VALUE}
    and extracts only the x and y coordinate values.
    
    Args:
        lines: List of strings containing YAML position definitions
        
    Returns:
        List of [x, y] coordinate pairs as integers
    """
    finalSet = []
    for line in lines:
        string = line

        int1 = int(string.index("x"))
        int2 = int(string.index(","))
        stringX = string[int1 + 3: int2 - 2]

        string = string[int2 + 1:]

        int3 = int(string.index("y"))
        int4 = int(string.index(","))
        stringY = string[int3 + 3: int4 - 2]

        string = string[int4:]

        # int5 = int(string.index("z"))
        # int6 = int(string.index("}"))
        # stringZ = string[int5 + 3: int6 - 2]

        shifts = [int(stringX), int(stringY)]

        finalSet.append(shifts)

    return finalSet

# Read YAML file and store all lines
with open(SCRIPT_DIR / "polygon.yaml", "r") as reader:
    for line in reader.readlines():
        yaml_lines.append(line)

# Extract coordinate lines from YAML: skip first 9 lines (header),
# then take every 5th line starting at line 9 (each waypoint is 5 lines apart)
coordinate_lines = []

for x in range(9, len(yaml_lines)):
    if ((x+1) % 5 == 0):
        coordinate_lines.append(yaml_lines[x])

# Convert extracted coordinates and apply transformation
XandY = convertPolygonPoints(coordinate_lines)
#print(XandY)

# Home point reference in WGS84 coordinates (latitude, longitude)
homePoint = np.array([39.355038, -76.345028])

# Scale coordinates from local frame to geographic degrees
# Division by 150000 converts local units to geographic displacement
XandY = np.divide(XandY, 150000)

# Add home point offset to convert from local coordinates to global coordinates
plan = np.add(XandY, homePoint)
#(str(plan))

# Read plan file template
plan_lines = []

with open(SCRIPT_DIR / "uavCopy.plan", "r") as reader2:
    for line in reader2.readlines():
        plan_lines.append(line)

#print(plan_lines[38])

# Format converted coordinates as JSON array for the plan file
stringPlan = []

# Format first coordinate pair: convert numpy array string to [lat, lon] JSON format
middleInt1 = int(len(str(plan[0])) / 2)
fixedString1 = str(plan[0])[0 : middleInt1] + "," + str(plan[0])[middleInt1 + 1 : len(str(plan[0]))]
fixedString1 = fixedString1[0] + fixedString1[2:]
myString = fixedString1

# Format remaining coordinates, comma-separated
for x in range(1, len(plan)):
    middleInt = int(len(str(plan[x])) / 2)
    fixedString = str(plan[x])[0 : middleInt] + "," + str(plan[x])[middleInt + 1 : len(str(plan[x]))]
    fixedString = fixedString[0] + fixedString[2:]
    myString += "," + fixedString

# Build the JSON "polygon" field for the plan file
myString = "                \"polygon\": [" + myString
myString = myString + "],\n"

# Insert formatted polygon into line 38 of the plan file template
# (index 38 is the line in uavCopy.plan where the polygon field should be placed)
plan_lines[38] = myString

# Write updated plan file
with open(SCRIPT_DIR / "uavCopy.plan", "w") as file:
    for line in plan_lines:
        file.write(line)
