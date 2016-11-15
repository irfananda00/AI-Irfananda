import csv
import random
import math
import operator
import copy
from time import gmtime, strftime
# ------------------------------------------------------
# TODO : main program
# ------------------------------------------------------
def readFile(csvfile):
    # read all the stored items in file
    reader = csv.reader(csvfile)
    dataset = []
    for row in reader:
        # skip if header
        if 'ID' in row:
            continue
        # get input x1-x10 and y
        inp = []
        for r in range(1,12):
            inp.append(float(row[r]))
        dataset.append(inp)
    return dataset

def readTestFile(csvfile):
    # read all the stored items in file
    reader = csv.reader(csvfile)
    dataset = []
    for row in reader:
        # skip if header
        if 'ID' in row:
            continue
        # get input x1-x10
        inp = []
        for r in range(1,11):
            inp.append(float(row[r]))
        dataset.append(inp)
    return dataset

def minmax(dataset):
    minX = []
    maxX = []
    # x1-x10
    n = len(dataset[0])
    if n > 10:
        n = n-1
    for i in range(n):
        minVal = 99999
        maxVal = -99999
        for j in range(len(dataset)):
            if dataset[j][i] > maxVal:
                maxVal = dataset[j][i]
            elif dataset[j][i] < minVal:
                minVal = dataset[j][i]
        minX.append(minVal)
        maxX.append(maxVal)
    return [minX, maxX]

# TO split into learn and train
def splitDataset(dataset, splitRatio):
    learnSize = int(len(dataset) * splitRatio)
    learns = []
    trains = list(dataset)
    while len(learns) < learnSize:
        index = random.randrange(len(trains))
        learns.append(trains.pop(index))
    return [learns, trains]

def getAccuracy(trainDataset,trainPredict):
    correct = 0.0
    for i in range(len(trainDataset)):
        if trainDataset[i][-1] == trainPredict[i][-1]:
            correct += 1
    print('correct: {0}').format(correct)
    return (correct/len(trainDataset))*100.0

# def normalize(x,minX,maxX):
#     return (x-minX) / ((maxX-minX)+0.0000001)
#
# def normalizeAll(dataset,minX,maxX):
#     for i in range(len(dataset)):
#         # x1-x10
#         n = len(dataset[i])
#         if n > 10:
#             n = n-1
#         for j in range(n):
#             dataset[i][j] = normalize(dataset[i][j],minX[j],maxX[j])
#     return dataset

def getEuclideanDistance(train,learn,min1,max1,min2,max2):
    distance = 0
    # x1-x10
    for i in range(len(learn)-1):
        # distance += pow(normalize(train[i],min1[i],max1[i]) - normalize(learn[i],min2[i],max2[i]), 2)
        distance += pow(train[i] - learn[i], 2)
    return math.sqrt(distance)

def getPrediction(learnDataset,trainDataset,k):
    prediction = []
    # Normalize to get minX and maxX
    min1, max1 = minmax(trainDataset)
    min2, max2 = minmax(learnDataset)

    # Normalize all dataset
    # trainDataset = normalizeAll(trainDataset,min1,max1)
    # learnDataset = normalizeAll(learnDataset,min2,max2)

    for i in range(len(trainDataset)):
        # get distance between trainDataset[i] to all of the learnDataset
        distances = []
        for j in range(len(learnDataset)):
            distance = getEuclideanDistance(trainDataset[i],learnDataset[j],min1,max1,min2,max2)
            distances.append((learnDataset[j],distance))
        # sort by nearest distance
        distances.sort(key=operator.itemgetter(1))
        # get k neighbors of trainDataset[i]
    	neighbors = []
    	for x in range(k):
            neighbors.append(distances[x][0])
        # count total of neighbors with y of all neighbors
        ys = {}
        for x in range(len(neighbors)):
            y = neighbors[x][-1]
            if y in ys:
                ys[y] += 1
            else:
                ys[y] = 1
        # get highest value of ys so that we can predict the y of this trainDataset
        sortedY = sorted(ys.iteritems(), key=operator.itemgetter(1), reverse=True)
        predict = sortedY[0][0]
        # result = "SALAH"
        # if predict == trainDataset[i][-1]:
        #     result = "BENAR"
        print('predict {0} : {1} | total vote : {2}').format(trainDataset[i],predict,sortedY[0][1])
        tmp = copy.copy(trainDataset[i])
        if len(tmp) > 10:
            # ada y nya
            tmp[-1] = predict
        else:
            # tidak ada y
            tmp.append(predict)
        prediction.append(tmp)
    return prediction

def main():
    # open file
    splitRatio = 0.75
    k = 3
    for i in range(11):
        with open('TrainMini.csv', 'rb') as csvfile:
            print('1. Learning ...')
            # Get Data
            dataset1 = readFile(csvfile)
            # Split into learn and train
            learnDataset, trainDataset = splitDataset(dataset1,splitRatio)
            print('Split {0} rows into learn={1} and train={2} rows').format(len(dataset1), len(learnDataset), len(trainDataset))
            # Predict output by learnDataset
            # k = int(math.sqrt(len(learnDataset)))
            trainPredict = getPrediction(learnDataset,trainDataset,k)
            # Evaluate Accuracy
            accuracy = getAccuracy(trainDataset,trainPredict)
            print('accuracy: {0}').format(accuracy)
            csvfile.close()

            # Set y value on Test dataset
            with open('TestMini.csv', 'rb') as csvfile:
                print('2. Testing ...')
                # Get Data
                dataset = readTestFile(csvfile)
                # Predict
                testPredict = getPrediction(dataset1,dataset,k)
                csvfile.close()
                # Get current date time
                date = strftime("%Y_%m_%d %H_%M_%S", gmtime());
                # write testPredict to new csv file
                testPredict.insert(0,["x1","x2","x3","x4","x5","x6","x7","x8","x9","x10","y"])
                with open(date+" k"+str(k)+".csv", "wb") as f:
                    writer = csv.writer(f)
                    writer.writerows(testPredict)
                    f.close()
                # write accuracy record csv file
                with open("record.csv", "a") as r:
                    r.write("Date : "+date+" | K: "+str(k)+" | split into learn: "+str(len(learnDataset))+" & train: "+str(len(trainDataset))+" | accuracy : "+str(accuracy)+" | test prediction : "+date+" k"+str(k)+".csv"+" \n")
                    r.close()
        # increment new k
        k = k+2

main()
