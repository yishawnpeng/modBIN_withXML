#############################
# UTF-8
# Shawn.Peng@quantatw.com
# Can modify binary with location recorded by xml
############################
# Work flow :
# 1.Can change target.txt to modify more step
#  (1) Default BiosStartInFullRomImage + PcdFlashNvStorageVariableOffset
#  (2) Rule : one line of feature-name and one line of act 
#  (3) The act only suppout +/-
#  (4) If act isn't correct or feature-name cannot find than it will be skiped
# 2.Find feature-name which user set in {Platform}.xml
#  (1) Now can find feature-name in tag of first layer and its text is the value we want
#  (2) Now can find feature-name in value of "name" tag of forth or fifth layers 
#      and the value of the tag "value" of the same layer is what we want
#  (3) User can choice number or press enter to use .xml witch first finded
# 3.Count the value and print it to double check
# 4.Read write_data.bin which will replace 
#  (1) User can input 1 to choice other write_data_factory_default.bin
#      otherwise default write_data.bin
#  (2) User can input manually to modify when execution CT/MAC/ForceNetBoot/counter/timer
#      otherwise default 11002200...EE00/FF..FF/1/5/2 
#  (3) User can also modify by command line use parameters
#  (4) Format for 4-2: \x00\x00\..\x07 in one line
#  (5) Format for 4-3: number of non-spaced strings from 0-9 and A-F
#  (6) *FF* Support other input format
# 5.Write date to {Platform_version}.bin
#  (1)Copy {Platform_version}.bin and rename {Platform_version}_ori.bin
#   progrm will modify in {Platform_version}.bin
# 
# 
# Share point
# xxx\CMIT_BIOS\
# GitHub 
# https://github.com/yishawnpeng/modBIN_withXML
#
#############################
# In write_data.bin :
#         CT start at : 204
#            end   at : 234
#         MAC start at : 234
#             end   at : 240
#         BootCounter start at : 243
#                     end   at : 245
#         Period start at : 245
#                end   at : 247
#############################
# NOTICE!! : in xml, <PCD> Block Skip
#############################
### Get and Count location
#import xml.etree.ElementTree as ET          # xml
import shutil                               # copy file
import sys                                  # exit
#import os                                   # operate file
#import re                                   # find file
from getXMLInfo import *                   # will import ET
from choceFile import *                    # will import os/re
from argParse import *
from modifyBin import *

#argumentDict={"MAC":None,"SBCT":None,"Counter":None,"Period":None} ## defined in argParse.py
legalParmeter = argParse_contant(argumentDict)
if not legalParmeter : sys.exit()

# That user chose .xml
XMLFileName = ChoceFile("xml")
if not XMLFileName : sys.exit()
#print(XMLFileName)

## Get target
TargetFileName = "target.txt"
#XMLFileName = "U21.xml"
#maybe user input filename
targetName =[]
targetAct=[]
with open(TargetFileName, "r") as targetFile :
    print("Opened Target name : " + TargetFileName )
    for i in targetFile.readlines() :
        if i[0:3] != "act":
            #maybe at end don't have \n
            targetName.append(i[:-1] if i[-1]=="\n" else i)
        else :
            targetAct.append(i[-2])       
## Get xml info
tree = ET.parse(XMLFileName)
print("Opened XML name : " + XMLFileName )
location = GetLocation_XMLInfo(tree, targetName, targetAct)
if not location : sys.exit()

#print(targetName)
#print(targetValue)
#print(targetValueINT)
#print(targetAct)
print("Taget location at :" , hex(location))

### Mod bin
# That user chose {written}.bin
#BinaryFileName = "U21_892627_32.bin"
BinaryFileName = ChoceFile("bin")
if not BinaryFileName : sys.exit()
#print(BinaryFileName)

# That user chose {written}.bin
#WriteDataFileName = "write_Data.bin"
writeDataFileString = "Input 1 to use write_data_factory_default.bin" \
                    + "or press enter to use write_data.bin which can modify." 
WriteDataFileName = input(writeDataFileString) or 0
while WriteDataFileName not in {0,1} :
    print("Not legal input !!!")
    WriteDataFileName = input(writeDataFileString) or 0
WriteDataFileName = "write_data.bin" if WriteDataFileName == 0 else "write_data_factory_default"

# if can modi write_data.bin
if WriteDataFileName == "write_data.bin" :
    ModifyWriteBin(WriteDataFileName, argumentDict)

#maybe user input BinaryFileName
with open(WriteDataFileName, "rb") as writeData :
    print("Opened Input-Data name : " + WriteDataFileName )
    data = writeData.read().split()    

#copy _ori.bin and write data to .bin
shutil.copy2(BinaryFileName, BinaryFileName[:-4]+"_ori"+BinaryFileName[-4:])
print("Created _ori.bin ")
with open(BinaryFileName, "rb+") as binaryFile :
    print("Opened Binary name : " + BinaryFileName )
    binaryFile.seek(location)
    #print(BinaryFile.read(1))
    #BinaryFile.seek(location)
    for i in data :
        binaryFile.write(i)
print("Write done !")
