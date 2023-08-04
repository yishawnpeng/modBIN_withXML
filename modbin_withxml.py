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
#  (2) *FF* User can input manually to modify CT/MAC/ForceNetBoot/counter/timer
#      otherwise default 11002200...EE00/FF..FF/1/5/2
#  (3) Format : \x00\x00\..\x07 in one line
#  (4) *FF* Support other input format
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
# NOTICE!! : in xml, <PCD> Block Skip
#############################
### Get and Count location
import xml.etree.ElementTree as ET          # xml
import shutil                               # copy file
import sys                                  # exit
#import os                                   # operate file
#import re                                   # find file
from choce_file import *                    # will import os/re
from modifyBin import *

# That user chose .xml
XMLFileName = Choce_file("xml")
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
root = tree.getroot()
targetValue=[]
for i in targetName :
    try:
        temp = root.find(i).text
        targetValue.append(temp)
    except Exception as maybeInSomones_AddressOffset :
        finded = False
        for j in root :
            for k in j :
                if k.tag == "Address" and not finded :
                    #print(k ,"k yes")
                    if k.find("Offset").find("Name").text == i:
                        #print(k.find("Offset").find("Value").text)
                        targetValue.append(k.find("Offset").find("Value").text)
                        finded = True
                elif not finded : # more deep like PeiA / DxeA
                    for l in k :
                        if l.tag == "Address" :
                            if l.find("Offset").find("Name").text == i :
                                targetValue.append(l.find("Offset").find("Value").text)
                                finded = True
                                break
                else : # can not find this name
                    print("Can not find this name : " + i )
                    print("Skip it !! ")
                    targetAct.pop(targetName.index(i)-1)
                if finded :
                    break
            if finded :
                break
## Count location
targetValueINT=[int(i, 16) for i in targetValue]
location = targetValueINT[0]
totalCount = []
totalCount.append(targetValueINT[0])
if len(targetValueINT) >= 2 :
    for i in range(1, len(targetValueINT)) :
        if targetAct[i-1] == "+" :
            location += targetValueINT[i]
            totalCount.append(targetAct[i-1])
        elif targetAct[i-1] == "-" :
            location -= targetValueINT[i]
        else :
            print("Don't supoort act : " + targetAct[i-1] + " !! Only +/- !!" )
            print("Skip this act and value : " + targetAct[i-1] + ","+ targetValueINT[i])
            break
else :
    location = None
    print("Don't have enough number !!")
    print("EXIT !!!")
    sys.exit()

#print(targetName)
#print(targetValue)
#print(targetValueINT)
#print(targetAct)
print("Taget location at :" , hex(location))

### Mod bin
# That user chose {written}.bin
#BinaryFileName = "U21_892627_32.bin"
BinaryFileName = Choce_file("bin")
if not BinaryFileName : sys.exit()
#print(BinaryFileName)

# That user chose {written}.bin
#WriteDataFileName = "write_Data.bin"
WriteDataFileString = "Input 1 to use write_data_factory_default.bin \
                       or press enter to use write_data.bin which can modify." 
WriteDataFileName = input(WriteDataFileString) or 0
while WriteDataFileName not in {0,1} :
    print("Not legal input !!!")
    writeDataFileName = input(WriteDataFileString) or 0
writeDataFileName = "write_data.bin" if writeDataFileName == 0 else "write_data_factory_default"

if writeDataFileName == "write_data.bin" :
    ModifyWriteBin(WriteDataFileName)

#maybe user input BinaryFileName
with open(WriteDataFileName, "rb") as writeData :
    print("Opened Input-Data name : " + WriteDataFileName )
    data = writeData.read().split()    

shutil.copy2(BinaryFileName, BinaryFileName[:-4]+"_ori"+BinaryFileName[-4:])
print("Created _ori.bin ")
with open(BinaryFileName, "rb+") as binaryFile :
    print("Opened Binary name : " + BinaryFileName )
    binaryFile.seek(location)
    #print(BinaryFile.read(1))
    #BinaryFile.seek(location)
    for i in data :
        binaryFile.write(i)
