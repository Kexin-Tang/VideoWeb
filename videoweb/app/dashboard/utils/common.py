def checkEnum(enumList, inputList):
    try:
        n = len(enumList)
        for i in range(n):
            enumList[i](inputList[i])
    except:
        return False
    return True

