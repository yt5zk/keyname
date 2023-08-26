#config: utf-8
import glob
import re
import os
import sys

args = sys.argv

path = args[1]

f = open("./keyMaps.csv")
lines = f.readlines()
f.close
keyMaps = []

for line in lines:
    line = line.rstrip("\r\n")
    splited = line.split(",")
    keyMaps.append(splited)

files = glob.glob(path + "/*")
for file in files:
    for keyMap in keyMaps:
        pattern = ".*[_\-\s]%s[_\-\s\.\d].+"%keyMap[0]
        matched = re.match(pattern, file)
        if matched:
                print (file)
                os.rename(file, os.path.join(path, keyMap[1] + " - " + os.path.basename(file)))