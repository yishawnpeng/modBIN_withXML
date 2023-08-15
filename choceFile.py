import os                                   # operate file
import re                                   # find file

def ChoceFile(file_type, autoUpdate) : # type : xml / bin
    returnName = None
    fatherDir = os.getcwd()
    allDir = os.listdir(fatherDir)
    if file_type == "bin" :
        fileNameList = re.compile("[^write].*\." + file_type)
    elif file_type == "write_data_default.bin" :
        fileNameList = re.compile(file_type)
    else :
        fileNameList = re.compile(".*\." + file_type)
    fileNameList = list( filter( fileNameList.match, allDir ) )

    if len(fileNameList) >= 2 and not autoUpdate : 
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
    elif len(fileNameList) == 1 or autoUpdate :
        returnName = fileNameList[0]
    else :
        if file_type == "write_data_default.bin" :
            print("Can not find write_data_default.bin !!!" )
        print("Can not find any ." + file_type + " !!!" )
    
    return returnName