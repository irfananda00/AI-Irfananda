import csv
import random
import math
import copy
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
        # get input x1-x10
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

# TO split into learn and train
def splitDataset(dataset, splitRatio):
    learnSize = int(len(dataset) * splitRatio)
    learns = []
    trains = list(dataset)
    while len(learns) < learnSize:
        index = random.randrange(len(trains))
        learns.append(trains.pop(index))
    return [learns, trains]

# TO separate dataset by class value
def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated

def mean(numbers):
    return sum(numbers)/len(numbers)

def var(numbers):
    avg = mean(numbers)
    # variance = sum([pow(x-avg,2) for x in numbers])/(float(len(numbers)-1))
    a = []
    for x in numbers:
        a.append(pow(x-avg,2))
    variance = sum(a)/float(len(numbers))
    return variance

def getModel(dataset,y):
    # x1 - x10
    summaries = []
    for i in range(len(dataset[y])):
        x = []
        # loop to bottom
        for n in range(len(dataset)):
            x.append(dataset[n][i])
        summaries.append((mean(x), var(x)))
    # delete the last index because its y value is the data class
    del summaries[-1]
    return summaries

def modelByClass(dataset):
    model = {}
    for y, xs in dataset.iteritems():
        # print('dataset[{1}]: {0}').format(xs,y)
        model[y] = getModel(xs,int(y))
    return model

def probabilities(x,mean,variance):
    # print('x: {0} mean: {1} var: {2}').format(x,mean,variance)
    return math.exp(-(pow(x-mean,2))/(2*pow(variance,2))) / float(variance*math.sqrt(2*math.pi))

def predictAll(modelDataset,trainDataset):
    trainPredict = []
    for train in trainDataset:
        posteriors = []
        for y in range(len(modelDataset)):
            # loop to all x on train
            pY = 1/float(len(modelDataset))
            for x in range(len(train)-1):
                pY *= probabilities(train[x],modelDataset[y][x][0],modelDataset[y][x][1])
            posteriors.append(pY)
        # get highest posterior
        highest = max(posteriors)
        y = posteriors.index(highest)
        pred = copy.copy(train)
        pred[-1] = float(y)
        trainPredict.append(pred)
    return trainPredict

def getAccuracy(trainDataset,trainPredict):
    correct = 0.0
    for i in range(len(trainDataset)):
        if trainDataset[i][-1] == trainPredict[i][-1]:
            correct += 1
    print('correct: {0}').format(correct)
    return (correct/len(trainDataset))*100.0

def main():
    # open file
    splitRatio = 0.75
    with open('Train.csv', 'rb') as csvfile:
        print('1. Please wait ...')
        # Get Data
        dataset = readFile(csvfile)
        # Split into learn and train
        learnDataset, trainDataset = splitDataset(dataset,splitRatio)
        print('Split {0} rows into learn={1} and train={2} rows').format(len(dataset), len(learnDataset), len(trainDataset))
        # Split learnDataset by output y
        learnSeparatedDataset = separateByClass(learnDataset)
        # Summarize learnDataset mean and variance for all x on each y
        modelDataset = modelByClass(learnSeparatedDataset)
        # Test the prediction on trainDataset
        trainPredict = predictAll(modelDataset,trainDataset)
        # Evaluate Accuracy
        accuracy = getAccuracy(trainDataset,trainPredict)
        print('accuracy: {0}').format(accuracy)
        # close file
        csvfile.close()

        # Set y value on Test dataset
        with open('Test.csv', 'rb') as csvfile:
            print('2. Please wait ...')
            # Get Data
            dataset = readTestFile(csvfile)
            # Give the prediction on testDataset
            testPredict = predictAll(modelDataset,dataset)
            # Separate by y value and print total of each y
            testSeparatedDataset = separateByClass(testPredict)
            for y, xs in testSeparatedDataset.iteritems():
                print('y[{0}]: {1}').format(y,len(xs))
            # close file
            csvfile.close()

main()
