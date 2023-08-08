import os                                   # operate file
import re                                   # find file

def ChoceFile(file_type) : # type : xml / bin
    returnName = None
    fatherDir = os.getcwd()
    allDir = os.listdir(fatherDir)
    if file_type == "bin" :
        fileNameList = re.compile("[^write].*\." + file_type)
    else :
        fileNameList = re.compile(".*\." + file_type)
    fileNameList = list( filter( fileNameList.match, allDir ) )

    if len(fileNameList) >= 2 : 
        print("Finded multy ." + file_type + " : ", fileNameList )
        fileNameList = ["("+str(i+1)+")"+fileNameList[i] for i in range(len(fileNameList))]
        fileNameString = ""
        for i in fileNameList : fileNameString += i + " "
        fileNameString = "Input which NUMBER ." \
                            + file_type \
                            + " you want " \
                            + fileNameString \
                            + "\nor press enter to use " \
                            + fileNameList[0][3:] \
                            + " : "
        fileNameNum = input( fileNameString ) or 1
        while not 0 < int(fileNameNum) <= len(fileNameList) :
            print("Not legal input !!!")
            fileNameNum = input( fileNameString ) or 1
        fileName = fileNameList[int(fileNameNum)-1]
        returnName = fileName[3:]
    elif len(fileNameList) == 1 :
        returnName = fileNameList[0]
    else :
        print("Can not find any ." + file_type + " !!!" )
    
    return returnName