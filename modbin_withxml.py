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
#  (1) User can input manually to modify when execution CT/MAC/ForceNetBoot/counter/timer
#      otherwise default 11002200...EE00/FF..FF/1/5/2 
#  (2) User can also modify by command line use parameters
#  (3) Format for 4-1: \x00\x00\..\x07 in one line
#  (4) Format for 4-2: number of non-spaced strings from 0-9 and A-F
#  (5) If use argument -y it will automatically confirm.
#  (6) Please note that the .bin file will be modified if the argument y and 
#      the four modification arguments m, s, c, and p are used together
# 5.Write date to {Platform_version}.bin
#  (1)Copy {Platform_version}.bin and rename {Platform_version}_ori.bin
#   progrm will modify in {Platform_version}.bin
# 
# 
# Share point
# xxx\CMIT_BIOS\Tools\modbin_withxml(M1Inject)\modBIN_withXML_7z_v{before v3}.7z
# xxx\CMIT_BIOS\Tools\modbin_withxml(M1Inject)\modBIN_withXML(M1Inject)_v4.7z
# GitHub 
# https://github.com/yishawnpeng/modBIN_withXML
#
#############################
# In write_data_default.bin :
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
# NOTICE!! : Using -y and [-m,-s,-c,-p] together will modify the .bin
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
autoUpdate, legalParmeter = argParse_contant(argumentDict)
if not legalParmeter : sys.exit()

# That user chose .xml
XMLFileName = ChoceFile("xml",autoUpdate)
if not XMLFileName : sys.exit()
#print(XMLFileName)

## Get target
TargetFileName = "target.txt"
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
# Always use write_data_default.bin to refer
onlyArg=False
WriteDataFileName = "write_data_default.bin"
if not autoUpdate :                                                             # no -y
    if list(argumentDict.values()).count(None) != len(argumentDict.keys()) :    # only arg 
        onlyArg=True
        BinaryFileName = ChoceFile("bin", autoUpdate)
        if not BinaryFileName : sys.exit()

        with open(BinaryFileName, "rb+") as binaryFile :
            binaryFile.seek(location)
            data = binaryFile.read(sum(list(binAreaLen.values())))

        tmepName = BinaryFileName[:-4]+"_temp"+BinaryFileName[-4:]
        shutil.copy2(BinaryFileName, tmepName)
        with open(tmepName, "wb+") as binaryFile :
            binaryFile.write(data)

        ModifyWriteBin(tmepName, argumentDict)
        WriteDataFileName = tmepName
    else :                                                                      # all arg empty -> manul
        WriteDataFileName = ChoceFile(WriteDataFileName, autoUpdate)
        if not WriteDataFileName : sys.exit()
        # If noy -y let user modify manuly
        ModifyWriteBin_manul(WriteDataFileName, argumentDict)
else :  # is autoUpdate                                                         # have y -> write all data 
    if list(argumentDict.values()).count(None) != len(argumentDict.keys()) :    # mod some in bin
        ModifyWriteBin(WriteDataFileName, argumentDict)
    else :  pass                                                                # only -y 
    
with open(WriteDataFileName, "rb") as writeData :
    print("Opened Input-Data name : " + WriteDataFileName )
    data = writeData.read()

if not onlyArg :                # only arg -> already chose
    # That user chose {written}.bin
    BinaryFileName = ChoceFile("bin", autoUpdate)
    if not BinaryFileName : sys.exit()

#copy _ori.bin and write data to .bin
shutil.copy2(BinaryFileName, BinaryFileName[:-4]+"_ori"+BinaryFileName[-4:])
print("Created _ori.bin ")
with open(BinaryFileName, "rb+") as binaryFile :
    print("Opened Binary name : " + BinaryFileName )
    binaryFile.seek(location)
    binaryFile.write(data)

if onlyArg :                    # only arg
    if os.path.exists(tmepName):
        os.remove(tmepName)

print("Write Complete !")
