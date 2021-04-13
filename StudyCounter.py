import os
import re
import json

path = os.path.realpath("")
print(path)

data = dict()
totalTime = 0

originalPlan = dict()
originalTotalTime = 0


from db import *

def writeToDb(twoDimensionDict, filePath, totalHour):
    session = Session()
    for oneDic in dict(twoDimensionDict).keys():
        print(oneDic + ":\n")
  
        littleItems = dict(twoDimensionDict).get(oneDic)
        for littleItem in dict(littleItems).keys():
            hours = littleItems[littleItem]
            dayPlan = DayPlan(bigItem=oneDic, littleItem=littleItem, time=hours)
            print(f"\t{littleItem}:{hours}\n")
            session.add(dayPlan)
            # fileObject.write('\n')  
    print(f"Total:{totalHour}")
    session.commit()
    for dayPlan in session.query(DayPlan):
        print(dayPlan)


def writeToJson(twoDimensionDict, filePath):
    jsObj = json.dumps(twoDimensionDict)  
    fileObject = open(filePath, 'w')  
    fileObject.write(jsObj)  
    fileObject.close()  


def writeToTxt(twoDimensionDict, filePath, totalHour):
    fileObject = open(filePath, 'w')  
    for oneDic in dict(twoDimensionDict).keys():
        print(oneDic + ":\n")
        fileObject.write(oneDic + ":\n")  
        littleItems = dict(twoDimensionDict).get(oneDic)
        for littleItem in dict(littleItems).keys():
            hours = littleItems[littleItem]
            print(f"\t{littleItem}:{hours}\n")
            fileObject.write(f"\t{littleItem}:{hours}\n")  
            # fileObject.write('\n')  
    print(f"Total:{totalHour}")
    fileObject.write(f"Total:{totalHour}")  
    fileObject.close()

#read original plan
with open(path + "\originalplan.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        dataArr = line.split("||");
        if(len(dataArr) == 3):
            # print(dataArr)
            bigItem = dataArr[0].strip()
            littleItem = dataArr[1].strip()
            time = dataArr[2].strip()
            # time = filter(str.is, time)
            temp = re.findall(r'\d+.\d+', time)
            if len(temp) == 0:
                temp = re.findall(r'\d+', time)
                if len(temp) == 0:
                    print(f"Can't find time in {line}")
                    continue
            temp = temp[0]
            time = temp
            # print(time)
            # time = str(time).replace("H","");
            # time = str(time).replace("h","");
            # time = time.strip();
            time = float(time); # hour
            originalTotalTime += time

            if not originalPlan.get(bigItem):
                originalPlan[bigItem] = dict()
            if not originalPlan[bigItem].get(littleItem):
                originalPlan[bigItem][littleItem] = float(0)
            originalPlan[bigItem][littleItem] += time
writeToTxt(originalPlan, "originalPlanData.txt", originalTotalTime)

#read data
with open(path + "\data.txt", 'r', encoding='utf-8') as f:
    for line in f.readlines():
        dataArr = line.split("||");
        if(len(dataArr) == 3):
            # print(dataArr)
            bigItem = dataArr[0].strip()
            littleItem = dataArr[1].strip()
            time = dataArr[2].strip()
            # time = filter(str.is, time)
            temp = re.findall(r'\d+.\d+', time)
            if len(temp) == 0:
                temp = re.findall(r'\d+', time)
                if len(temp) == 0:
                    print(f"Can't find time in {line}")
                    continue
            temp = temp[0]
            time = temp
            # print(time)
            # time = str(time).replace("H","");
            # time = str(time).replace("h","");
            # time = time.strip();
            time = float(time); # hour
            totalTime += time

            if not data.get(bigItem):
                data[bigItem] = dict()
            if not data[bigItem].get(littleItem):
                data[bigItem][littleItem] = float(0)
            data[bigItem][littleItem] += time

print(data)
print(totalTime)



writeToJson(data, "countData.json")

writeToTxt(data, "countData.txt", totalTime)

writeToDb(data, "countData.txt", totalTime)