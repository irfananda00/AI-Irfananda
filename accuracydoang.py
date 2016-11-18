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
        if 'x1' in row:
            continue
        # get input x1-x10 and y
        inp = []
        for r in range(0,len(row)):
            inp.append(float(row[r]))
        dataset.append(inp)
    return dataset

def getAccuracy(trainDataset,trainPredict):
    correct = 0.0
    for i in range(len(trainDataset)):
        if trainDataset[i][-1] == trainPredict[i][-1]:
            correct += 1
    print('correct: {0}').format(correct)
    return (correct/len(trainDataset))*100.0

def main():
    # open file
    with open('2016_11_16 04_11_42 k9.csv', 'rb') as csvfile:
        # Get Data
        dataset1 = readFile(csvfile)

        with open('2016_11_16 11_37_01 k13.csv', 'rb') as csvfile:
            # Get Data
            dataset = readFile(csvfile)
            csvfile.close()
                
        # Evaluate Accuracy
        accuracy = getAccuracy(dataset1,dataset)
        print('accuracy: {0}').format(accuracy)
        csvfile.close()

main()
