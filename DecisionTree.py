#决策树生成算法： treesID3.py
from math import log
from operator import itemgetter

def createDataSet():            #创建数据集
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    featname = ['no surfacing', 'flippers']
    return dataSet,featname

def filetoDataSet(filename):
    fr = open(filename,'r')
    all_lines = fr.readlines()
    featname = all_lines[0].strip().split(',')[1:-1]
    print(featname)
    dataSet = []
    for line in all_lines[1:]:
        line = line.strip()
        lis = line.split(',')[1:]
        dataSet.append(lis)
    fr.close()
    return dataSet,featname

def calcEnt(dataSet):           #计算香农熵
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        label = featVec[-1]
        if label not in labelCounts.keys():
            labelCounts[label] = 0
        labelCounts[label] += 1
    Ent = 0.0
    for key in labelCounts.keys():
        p_i = float(labelCounts[key]/numEntries)
        Ent -= p_i * log(p_i,2)
    return Ent

def splitDataSet(dataSet, axis, value):   #划分数据集,找出第axis个属性为value的数据
    returnSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
    return returnSet

def chooseBestFeat(dataSet):
    numFeat = len(dataSet[0])-1
    Entropy = calcEnt(dataSet)
    DataSetlen = float(len(dataSet))
from math import log
from operator import itemgetter

def filetoDataSet(filename):
    fr = open(filename,'r')
    all_lines = fr.readlines()
    featname = all_lines[0].strip().split(',')[1:-1]
    dataSet = []
    for line in all_lines[1:]:
        line = line.strip()
        lis = line.split(',')[1:]
        dataSet.append(lis)
    fr.close()
    return dataSet,featname

def calcEnt(dataSet, weight):           #计算权重香农熵
    labelCounts = {}
    i = 0
    for featVec in dataSet:
        label = featVec[-1]
        if label not in labelCounts.keys():
            labelCounts[label] = 0
        labelCounts[label] += weight[i]
        i += 1
    Ent = 0.0
    for key in labelCounts.keys():
        p_i = float(labelCounts[key]/sum(weight))
        Ent -= p_i * log(p_i,2)
    return Ent

def splitDataSet(dataSet, weight, axis, value, countmissvalue):   #划分数据集,找出第axis个属性为value的数据
    returnSet = []
    returnweight = []
    i = 0
    for featVec in dataSet:
        if featVec[axis] == '?' and (not countmissvalue):
            continue
        if countmissvalue and featVec[axis] == '?':
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
        if featVec[axis] == value:
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
            returnweight.append(weight[i])
        i += 1
    return returnSet,returnweight

def splitDataSet_for_dec(dataSet, axis, value, small, countmissvalue):
    returnSet = []
    for featVec in dataSet:
        if featVec[axis] == '?' and (not countmissvalue):
            continue
        if countmissvalue and featVec[axis] == '?':
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
        if (small and featVec[axis] <= value) or ((not small) and featVec[axis] > value):
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
    return returnSet
            
def DataSetPredo(filename,decreteindex):     #首先运行，权重不变为1
    dataSet,featname = filetoDataSet(filename)
    DataSetlen = len(dataSet)
    Entropy = calcEnt(dataSet,[1 for i in range(DataSetlen)])
    for index in decreteindex:     #对每一个是连续值的属性下标
        UnmissDatalen = 0
        for i in range(DataSetlen):      #字符串转浮点数
            if dataSet[i][index] != '?':
                UnmissDatalen += 1
                dataSet[i][index] = float(dataSet[i][index])
        allvalue = [vec[index] for vec in dataSet if vec[index] != '?']
        sortedallvalue = sorted(allvalue)
        T = []
        for i in range(len(allvalue)-1):        #划分点集合
            T.append(float(sortedallvalue[i]+sortedallvalue[i+1])/2.0)
        bestGain = 0.0
        bestpt = -1.0
        for pt in T:          #对每个划分点
            nowent = 0.0
            for small in range(2):   #化为正类(1)负类(0)
                Dt = splitDataSet_for_dec(dataSet, index, pt, small, False)
                p = len(Dt) / float(UnmissDatalen)
                nowent += p * calcEnt(Dt)
            if Entropy - nowent > bestGain:
                bestGain = Entropy-nowent
                bestpt = pt
        featname[index] = str(featname[index]+"<="+"%.3f"%bestpt)
        for i in range(DataSetlen):
            if dataSet[i][index] != '?':
                dataSet[i][index] = "是" if dataSet[i][index] <= bestpt else "否"
    return dataSet,featname

def getUnmissDataSet(dataSet, weight, axis):
    returnSet = []
    returnweight = []
    tag = []
    i = 0
    for featVec in dataSet:
        if featVec[axis] == '?':
            tag.append(i)
        else:
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
        i += 1
    for i in range(len(weight)):
        if i not in tag:
            returnweight.append(weight[i])
    return returnSet,returnweight

def printlis(lis):
    for li in lis:
        print(li)
        
def chooseBestFeat(dataSet,weight,featname):
    numFeat = len(dataSet[0])-1
    DataSetWeight = sum(weight)
    bestGain = 0.0
    bestFeat = -1
    for i in range(numFeat):
        UnmissDataSet,Unmissweight = getUnmissDataSet(dataSet, weight, i)   #无缺失值数据集及其权重
        Entropy = calcEnt(UnmissDataSet,Unmissweight)      #Ent(D~)
        allvalue = [featVec[i] for featVec in dataSet if featVec[i] != '?']
        UnmissSumWeight = sum(Unmissweight)
        lou = UnmissSumWeight / DataSetWeight        #lou
        specvalue = set(allvalue)
        nowEntropy = 0.0
        for v in specvalue:      #该属性的几种取值
            Dv,weightVec_v = splitDataSet(dataSet,Unmissweight,i,v,False)   #返回 此属性为v的所有样本 以及 每个样本的权重
            p = sum(weightVec_v) / UnmissSumWeight          #r~_v = D~_v / D~
            nowEntropy += p * calcEnt(Dv,weightVec_v)
        if lou*(Entropy - nowEntropy) > bestGain:
            bestGain = Entropy - nowEntropy
            bestFeat = i
    return bestFeat

def Vote(classList,weight):
    classdic = {}
    i = 0
    for vote in classList:
        if vote not in classdic.keys():
            classdic[vote] = 0
        classdic[vote] += weight[i]
        i += 1
    sortedclassDic = sorted(classdic.items(),key=itemgetter(1),reverse=True)
    return sortedclassDic[0][0]

def splitDataSet_adjustWeight(dataSet,weight,axis,value,r_v):
    returnSet = []
    returnweight = []
    i = 0
    for featVec in dataSet:
        if featVec[axis] == '?':
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
            returnweight.append(weight[i] * r_v)
        elif featVec[axis] == value:
            retVec = featVec[:axis]
            retVec.extend(featVec[axis+1:])
            returnSet.append(retVec)
            returnweight.append(weight[i])
        i += 1
    return returnSet,returnweight
    
def createDecisionTree(dataSet,weight,featnames):
    featname = featnames[:]              ################
    classlist = [featvec[-1] for featvec in dataSet]  #此节点的分类情况
    if classlist.count(classlist[0]) == len(classlist):  #全部属于一类
        return classlist[0]
    if len(dataSet[0]) == 1:         #分完了,没有属性了
        return Vote(classlist,weight)       #少数服从多数
    # 选择一个最优特征进行划分
    bestFeat = chooseBestFeat(dataSet,weight,featname)
    bestFeatname = featname[bestFeat]
    del(featname[bestFeat])     #防止下标不准
    DecisionTree = {bestFeatname:{}}
    # 创建分支,先找出所有属性值,即分支数
    allvalue = [vec[bestFeat] for vec in dataSet if vec[bestFeat] != '?']
    specvalue = sorted(list(set(allvalue)))  #使有一定顺序
    UnmissDataSet,Unmissweight = getUnmissDataSet(dataSet, weight, bestFeat)   #无缺失值数据集及其权重
    UnmissSumWeight = sum(Unmissweight)      # D~
    for v in specvalue:
        copyfeatname = featname[:]
        Dv,weightVec_v = splitDataSet(dataSet,Unmissweight,bestFeat,v,False)   #返回 此属性为v的所有样本 以及 每个样本的权重
        r_v = sum(weightVec_v) / UnmissSumWeight          #r~_v = D~_v / D~
        sondataSet,sonweight = splitDataSet_adjustWeight(dataSet,weight,bestFeat,v,r_v)
        DecisionTree[bestFeatname][v] = createDecisionTree(sondataSet,sonweight,copyfeatname)
    return DecisionTree


if __name__ == '__main__':
    filename = "D:\\MLinAction\\Data\\breast-cancer-wisconsin.data"
    DataSet,featname = filetoDataSet(filename)
    Tree = createDecisionTree(DataSet,featname)
    print(Tree)
