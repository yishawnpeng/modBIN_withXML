import argparse

version = "4"
macHelpStr = "Input MAC you want. Enter 12 non-spaced strings from 0-9 and A-F."
sbctHelpStr = "Input SystemBordCT you want. Enter 30 non-spaced strings from 0-9 and A-F."
counterHelpStr = "Input Counter you want. Enter 4 non-spaced strings from 0-9 and A-F."
periodHelpStr = counterHelpStr
autoHelpStr = "Automatically confirm all actions without requiring manual confirmation. \
Please note that the .bin file will be modified if the argument y and the four modification parameters m, s, c, and p are used together."

cheeckRange =["0","1","2","3","4","5","6","7","8","9",\
              "a","b","c","d","e","f","A","B","C","D","E","F"]

def checkAll(string, requestLen) :
    if len(string) != requestLen :
        return False
    for i in string :
        if i not in cheeckRange :
            return False
    return True

def argParse_contant(argumentDict):
    exitFlag = False
    autoUpdate = False
    parser = argparse.ArgumentParser(prog='modbin_withxml.py', description='Tutorial')
    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument("-y", "--yes", action="store_true",help=autoHelpStr )
    parser.add_argument("-m", "--mac", help=macHelpStr )
    parser.add_argument("-s", "--sbct", help=sbctHelpStr )
    parser.add_argument("-c", "--counter", help=counterHelpStr )
    parser.add_argument("-p", "--period", help=periodHelpStr )
    args = parser.parse_args()
    if args.yes :
        autoUpdate = True

    if args.mac:
        argumentDict["MAC"] = args.mac
        if not checkAll(args.mac, 12) :
            print("Input MAC format illegal !")
            exitFlag = True
        
    if args.sbct:
        argumentDict["SBCT"] = "".join([args.sbct[i:i+2]+"00"for i in range(0,len(args.sbct),2)])
        if not checkAll(args.sbct, 30) :
            print("Input SystemBordCT format illegal !")
            exitFlag = True
        
    if args.counter:
        argumentDict["Counter"] = args.counter[2:]+args.counter[0:2]
        if not checkAll(args.counter, 4) :
            print("Input Counter format illegal !")
            exitFlag = True
       
    if args.period:
        argumentDict["Period"] = args.period[2:]+args.period[0:2]
        if not checkAll(args.period, 4) :
            print("Input Period format illegal !")
            exitFlag = True

    if exitFlag :
        return autoUpdate, False
    return autoUpdate, True