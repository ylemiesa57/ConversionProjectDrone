import numpy as np
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


listOfMacs = []


def convertPolygonPoints(lines):
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

with open(SCRIPT_DIR / "polygon.yaml", "r") as reader:
    for line in reader.readlines():
        listOfMacs.append(line)

newArray = []

for x in range (9, len(listOfMacs)) :
    if ((x+1) % 5 == 0):
        newArray.append(listOfMacs[x])

XandY = convertPolygonPoints(newArray)
#print(XandY)

homePoint = np.array([39.355038, -76.345028])

XandY = np.divide(XandY, 150000)
plan = np.add(XandY, homePoint)
#(str(plan))

otherMacs = []

with open(SCRIPT_DIR / "uavCopy.plan", "r") as reader2:
    for line in reader2.readlines():
        otherMacs.append(line)

#print(otherMacs[38])

stringPlan = []
middleInt1 = int(len(str(plan[0])) / 2)
fixedString1 = str(plan[0])[0 : middleInt1] + "," + str(plan[0])[middleInt1 + 1 : len(str(plan[0]))]
fixedString1 = fixedString1[0] + fixedString1[2:]
myString = fixedString1

for x in range(1, len(plan)):
    middleInt = int(len(str(plan[x])) / 2)
    fixedString = str(plan[x])[0 : middleInt] + "," + str(plan[x])[middleInt + 1 : len(str(plan[x]))]
    fixedString = fixedString[0] + fixedString[2:]
    myString += "," + fixedString

myString = "                \"polygon\": [" + myString
myString = myString + "],\n"

otherMacs[38] = myString

with open(SCRIPT_DIR / "uavCopy.plan", "w") as file:
    for line in otherMacs:
        file.write(line)
