from argParse import *          # for userInputStr... and 

binAreaLen = {"startOffset":204,    "SBCT":30,           "MAC":6,\
              "ForceNetBoot":1,     "ForceBackLight":1,  "DisableLidSwitch":1, \
              "Counter":2,          "Period":2,          "endOffset":15 }

sbctEnd = binAreaLen["startOffset"]+binAreaLen["SBCT"]
counterStart = binAreaLen["startOffset"]+binAreaLen["SBCT"]\
                +binAreaLen["MAC"]+binAreaLen["ForceNetBoot"] \
                +binAreaLen["ForceBackLight"]+binAreaLen["DisableLidSwitch"]
counterEnd = counterStart+binAreaLen["Counter"]

binAreaStart = {"SBCT":binAreaLen["startOffset"],\
                "MAC":sbctEnd,\
                "Counter":counterStart,\
                "Period":counterEnd,\
                }

argumentDict={"MAC":None,"SBCT":None,"Counter":None,"Period":None}

userInputData = ["("+str(i)+")"+j for i,j in zip(range(len(argumentDict)),argumentDict)]
userInputStr = "Which number you want to modify \n"+ "\n".join(userInputData) \
                + "\n(Enter) to exit :"

def PrintWriteInfoSize(WriteDataFileName) :
    print("In "+WriteDataFileName+" :")
    print("\tSBCT start at : "+str(binAreaLen["startOffset"]))
    print("\t     end   at : "+str(binAreaLen["startOffset"]+binAreaLen["SBCT"]))
    print("\tMAC start at : "+str(sbctEnd))
    print("\t    end   at : "+str(sbctEnd+binAreaLen["MAC"]))
    print("\tCounter start at : "+str(counterStart))
    print("\t        end   at : "+str(counterStart+binAreaLen["Counter"]))
    print("\tPeriod start at : "+str(counterEnd))
    print("\t       end   at : "+str(counterEnd+binAreaLen["Period"]))


def ModifyWriteBin(WriteDataFileName, argumentDict) :
    if list(argumentDict.values()).count(None) == len(argumentDict.keys()) :
        print("You can't manually modify the binary" \
              +"when you run this program with additional parameters.")
    elif input("Input any key if you want to modify data or only enter to skip: ") :
        whichOne = "\n"
        while whichOne :
            whichOne = input(userInputStr)
            if whichOne == "\n" :
                break
            elif whichOne == "0" :
                temp = input(macHelpStr)
                if checkAll(temp, 12) :
                    argumentDict["MAC"] = temp
                else : print("Input MAC format illegal !\n")
            elif whichOne == "1" :
                temp = input(sbctHelpStr)
                if checkAll(temp, 30) : 
                    argumentDict["SBCT"] = temp
                else : print("Input SBCT format illegal !\n")
            elif whichOne == "2" :
                temp = input(counterHelpStr)
                if checkAll(temp, 4) :
                    argumentDict["Counter"] = temp[2:]+temp[0:2]
                else : print("Input Counter format illegal !\n")
            elif whichOne == "3" :
                temp = input(periodHelpStr)
                if checkAll(temp, 4) :
                    argumentDict["Period"] = temp[2:]+temp[0:2]
                else : print("Input Period format illegal !\n")
            else :
                print("!!Not legal input options !!\n")

    #PrintWriteInfoSize(WriteDataFileName)
    with open(WriteDataFileName, "rb+") as writeData :
        print("Opened Modify Input-Data name : " + WriteDataFileName )
        #data = writeData.read()
        #print(data)
        for x in argumentDict :
            if argumentDict[x] and x in binAreaStart :
                #print(x)
                #print(argumentDict[x])
                writeData.seek(int(hex(binAreaStart[x]),0),0) 
                for y in range(0,len(argumentDict[x]),2) : # two byte write once
                    #print(argumentDict[x][y]+argumentDict[x][y+1])
                    writeData.write(bytes([int(argumentDict[x][y]+argumentDict[x][y+1],16)]))
        #writeData.seek(int(hex(binAreaLen["startOffset"]),0),0)
        #writeData.write(bytes([int("44",16)]))

#print(int( hex(binAreaLen["startOffset"]),0 ))
#print(bytes([int("9A",16)]))
#print(bytes([136]))
#WriteDataFileName = "write_data.bin"
#ModifyWriteBin(WriteDataFileName, argumentDict)