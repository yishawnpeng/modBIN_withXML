import xml.etree.ElementTree as ET          # xml

def GetLocation_XMLInfo(tree, targetName, targetAct):
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
    return location