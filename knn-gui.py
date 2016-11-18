import csv
import random
import math
import operator
import copy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
# ------------------------------------------------------
# TODO : main program
# ------------------------------------------------------
class KNN(Widget):
    def __init__(self, **kwargs):
        super(KNN, self).__init__(**kwargs)
        self.main()

    def readFile(self,csvfile):
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

    def readTestFile(self,csvfile):
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

    def minmax(self,dataset):
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
    def splitDataset(self,dataset, splitRatio):
        learnSize = int(len(dataset) * splitRatio)
        learns = []
        trains = list(dataset)
        while len(learns) < learnSize:
            index = random.randrange(len(trains))
            learns.append(trains.pop(index))
        return [learns, trains]

    def getAccuracy(self,trainDataset,trainPredict):
        correct = 0.0
        for i in range(len(trainDataset)):
            if trainDataset[i][-1] == trainPredict[i][-1]:
                correct += 1
        return (correct/len(trainDataset))*100.0

    def normalize(self,x,minX,maxX):
        return (x-minX) / ((maxX-minX)+0.0000001)

    def normalizeAll(self,dataset,minX,maxX):
        for i in range(len(dataset)):
            # x1-x10
            n = len(dataset[i])
            if n > 10:
                n = n-1
            for j in range(n):
                dataset[i][j] = self.normalize(dataset[i][j],minX[j],maxX[j])
        return dataset

    def getEuclideanDistance(self,train,learn,min1,max1,min2,max2):
        distance = 0
        # x1-x10
        for i in range(len(learn)-1):
            distance += pow(self.normalize(train[i],min1[i],max1[i]) - self.normalize(learn[i],min2[i],max2[i]), 2)
        return math.sqrt(distance)

    def getPrediction(self,learnDataset,trainDataset,k):
        prediciton = []
        # Normalize to get minX and maxX
        min1, max1 = self.minmax(trainDataset)
        min2, max2 = self.minmax(learnDataset)

        # Normalize all dataset
        trainDataset = self.normalizeAll(trainDataset,min1,max1)
        learnDataset = self.normalizeAll(learnDataset,min2,max2)

        # Draw all learnDataset
        self.drawPoints(learnDataset)

        for i in range(len(trainDataset)):
            # get distance between trainDataset[i] to all of the learnDataset
            distances = []
            for j in range(len(learnDataset)):
                distance = self.getEuclideanDistance(trainDataset[i],learnDataset[j],min1,max1,min2,max2)
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
            prediciton.append(tmp)
            self.drawPredict(tmp)
        return prediciton

    def mean(self,numbers):
        return sum(numbers)/len(numbers)

    def drawPredict(self,data):
        with self.canvas:
            if data[-1] == 0.0:
                Color(1, 1, 0)
            else:
                Color(0, 1, 1)
            d = 5.
            x = 0
            y = 0
            # x1 - x5
            for j in range(0,5):
                x += data[j]
            # x6 - x10
            for j in range(5,10):
                y += data[j]
            x = math.sqrt(pow(x * 150.0,2))
            y = math.sqrt(pow(y * 150.0,2))
            Ellipse(pos=(x, y), size=(d, d))

            # x1 - x10
            # for j in range(len(data)-1):
            #     x = math.sqrt(pow(data[j] * 500.0,2))
            #     j += 1
            #     y = math.sqrt(pow(data[j] * 500.0,2))
            #     Ellipse(pos=(x, y), size=(d, d))

            # x1 - x10
            # for j in range(len(data)-1):
            #     x += data[j]
            # x = math.sqrt(pow(x * 100.0,2))
            # y = math.sqrt(pow(data[-1] * 100.0,2))
            # Ellipse(pos=(x, y), size=(d, d))

    def drawPoint(self,data):
        with self.canvas:
            if data[-1] == 0.0:
                Color(1, 0, 0)
            else:
                Color(0, 0, 1)
            d = 5.
            x = 0
            y = 0
            # x1 - x5
            for j in range(0,5):
                x += data[j]
            # x6 - x10
            for j in range(5,10):
                y += data[j]
            x = math.sqrt(pow(x * 150.0,2))
            y = math.sqrt(pow(y * 150.0,2))
            Ellipse(pos=(x, y), size=(d, d))

            # x1 - x10
            # for j in range(len(data)-1):
            #     x = math.sqrt(pow(data[j] * 500.0,2))
            #     j += 1
            #     y = math.sqrt(pow(data[j] * 500.0,2))
            #     Ellipse(pos=(x, y), size=(d, d))

            # x1 - x10
            # for j in range(len(data)-1):
            #     x += data[j]
            # x = math.sqrt(pow(x * 100.0,2))
            # y = math.sqrt(pow(data[-1] * 100.0,2))
            # Ellipse(pos=(x, y), size=(d, d))

    def drawPoints(self,dataset):
        with self.canvas:
            for i in range(len(dataset)):
                self.drawPoint(dataset[i])

    def main(self):
        # open file
        splitRatio = 0.75
        with open('TrainMini.csv', 'rb') as csvfile:
            # Get Data
            dataset = self.readFile(csvfile)
            # Split into learn and train
            learnDataset, trainDataset = self.splitDataset(dataset,splitRatio)
            print('Split {0} rows into learn={1} and train={2} rows').format(len(dataset), len(learnDataset), len(trainDataset))
            # Predict output by learnDataset
            k = 3
            trainPredict = self.getPrediction(learnDataset,trainDataset,k)
            # Evaluate Accuracy
            accuracy = self.getAccuracy(trainDataset,trainPredict)
            print('accuracy: {0}').format(accuracy)
            csvfile.close()

            # Set y value on Test dataset
            with open('TestMini.csv', 'rb') as csvfile:
                # Get Data
                dataset = self.readTestFile(csvfile)
                # Test it
                testPredict = self.getPrediction(learnDataset,dataset,k)
                csvfile.close()

class KNNApp(App):
    def build(self):
        return KNN()

if __name__ == '__main__':
    KNNApp().run()
