from collections import OrderedDict
import os
import sys
# 读取黑名单和额外名单
def opnWBEList(WBEList):
    with open(WBEList, encoding='utf-8',mode='r') as fin:
        isW = 0
        for aline in fin:
            aline = aline.strip()
            if aline.startswith("#黑名单"):
                isW = 2
                continue
            elif aline.startswith("#额外名单"):
                isW = 3
                continue
            if isW == 2 and aline != "":
                bList[aline] = 1
            elif isW == 3 and aline != "":
                eList[aline] = 1

def writeExtraRlt(rlt):
    tmf = open(rlt, encoding='utf-8', mode='a')
    for i in eList:
        str = i.strip()
        if str.startswith("#EXTM3U"):
            pass
        else:
          tmf.write(str + '\n')
    tmf.flush()
    tmf.close()

def isInBlack(aStr):
    for aItem in bList:
        if aItem in aStr:
            return True
    return False

def writrRlt(source,rlt):
    with open(source, encoding='utf-8',mode='r') as fin:
        allLines = fin.readlines()
        fileLength = len(allLines)
        tmf = open(rlt, encoding='utf-8', mode='a')

        index = 0
        while index < fileLength-1:
            aLine = allLines[index].strip()
            nextLine = allLines[index+1].strip()
            if aLine.startswith("#") and nextLine.startswith("http"):
                if isInBlack(aLine):
                    pass
                else:
                    tmf.write(aLine + '\n')
                    tmf.write(nextLine + '\n')
            index += 1

        tmf.flush()
        tmf.close()

def getRawFileList(path):
    files = []
    for f in os.listdir(path):
        if not f.endswith("~") or not f == "": 
            files.append(os.path.join(path, f))
    return files

if __name__ == "__main__":
    sourcefiles = getRawFileList(sys.argv[1]+"/m3u/source")
    tregetfile = sys.argv[1]+"/tmp.m3u8"
    for i in sourcefiles:
        eList = OrderedDict()
        bList = {}
        opnWBEList(sys.argv[1]+"/m3u/black-extra.list")
        writrRlt(i, tregetfile)
        writeExtraRlt(tregetfile)
