import random
import copy
import operator
# ------------------------------------------------------
# TODO : main program
# ------------------------------------------------------
data = ['S','A','B','C','D','E','F','G']
rulesRoute = [
         [0,1,1,1,0,0,0,0],
         [0,0,1,0,1,0,0,0],
         [0,1,0,1,0,1,0,0],
         [0,0,1,0,0,0,1,0],
         [0,0,0,0,0,1,0,1],
         [0,0,0,0,1,0,1,1],
         [0,0,0,0,0,1,0,1],
         [0,0,0,0,0,0,0,0]
         ]
rulesWeight = [
          [0,0.1,0.23,0.167,0,0,0,0],
          [0,0,0.1,0,0.4,0,0,0],
          [0,0.1,0,0.067,0,0.25,0,0],
          [0,0,0.067,0,0,0,0.3,0],
          [0,0,0,0,0,0.067,0,0.15],
          [0,0,0,0,0.067,0,0.067,0.15],
          [0,0,0,0,0,0.067,0,0.15],
          [0,0,0,0,0,0,0,0]
          ]

def initPopulation(n,k):
    population = []
    for i in range(n):
        kromosom = []
        preIndex = 0
        for j in range(k):
            rulesOK = False
            while rulesOK != True:
                index = random.randint(1,k)
                if len(kromosom) == 0:
                    if rulesRoute[preIndex][index] == 1:
                        rulesOK = True
                        preIndex = index
                else:
                    if 7 not in kromosom:
                        if rulesRoute[preIndex][index] == 1 and index not in kromosom :
                            rulesOK = True
                            preIndex = index
                    else:
                        if index not in kromosom:
                            rulesOK = True
                            preIndex = index
            kromosom.append(index)
        kromosom.insert(0,0)
        population.append(kromosom)
    print('population: {0}').format(population)
    return population

def getFitness(population):
    fitPopulation = []
    for i in range(len(population)):
        fitness = 0
        for j in range(len(population[i])):
            if population[i][j] == 7:
                break
            fromIndex = population[i][j]
            toIndex = population[i][j+1]
            fitness += 1/((rulesWeight[fromIndex][toIndex]+0.01))
        fitPopulation.append((fitness, population[i]))
    print('fitPopulation: {0}').format(fitPopulation)
    return fitPopulation

def getPercentage(fitPopulation):
    total = sum([pops[0] for pops in fitPopulation])
    print('total fitness: {0}').format(total)
    fitPercentage = []
    preRange = 0
    for i in range(len(fitPopulation)):
        preRange += fitPopulation[i][0]/total
        fitPercentage.append((preRange, fitPopulation[i][1]))
    print('fitPercentage: {0}').format(fitPercentage)
    return fitPercentage

def doRoulette(fitPercentage):
    index = 0
    ind = random.uniform(0.0,1.0)
    for j in range(len(fitPercentage)):
        if ind <= fitPercentage[j][0]:
            index = j
            break
    return index

def getCouples(fitPopulation):
    couples = []
    # dapatkan persentase fitness
    fitPercentage = getPercentage(fitPopulation)
    # lakukan roulette
    for i in range(len(fitPopulation)/2):
        ind1 = doRoulette(fitPercentage)
        ind2 = ind1
        while ind1 == ind2:
            ind2 = doRoulette(fitPercentage)
        couples.append((fitPopulation[ind1],fitPopulation[ind2]))
    print('couples: {0}').format(couples)
    return couples

def orderCrossOver(couple):
    size = len(couple[0][1])
    ind1 = copy.copy(couple[0][1])
    ind2 = copy.copy(couple[1][1])
    print('couple parent')
    print('ind1: {0}').format(ind1)
    print('ind2: {0}').format(ind2)

    # init individu baru
    ind1C = []
    for i in range(0,2):
        ind1C.append(ind1[i])
    ind2C = []
    for i in range(0,2):
        ind2C.append(ind2[i])

    # cross over
    # ind1C
    for i in range(2,size):
        if ind2[i] in ind1C:
            continue
        ind1C.append(ind2[i])
    # jika panjang kromosom belum 7
    for i in range(size-len(ind1C)):
        ind1C.append(ind2[i])
    # ind2C
    for i in range(2,size):
        if ind1[i] in ind2C:
            continue
        ind2C.append(ind1[i])
    # jika panjang kromosom belum 7
    for i in range(size-len(ind2C)):
        ind2C.append(ind1[i])

    print('twin child')
    print('ind1C: {0}').format(ind1C)
    print('ind2C: {0}').format(ind2C)
    return [ind1C,ind2C]

def getChild(couples):
    childPopulation = []
    for i in range(len(couples)):
        ind1,ind2 = orderCrossOver(couples[i])
        childPopulation.append(ind1)
        childPopulation.append(ind2)
    print('childPopulation: {0}').format(childPopulation)
    return childPopulation

def runGA(fitPopulation):
    # roulette wheel | nilai fitness yang lebih besar persentasenya lebih besar -> pasangan kromosom
    couples = getCouples(fitPopulation)
    # cross over pasangan | pengecekan terhubung tidaknya
    childPopulation = getChild(couples)
    # TODO mutasi kromosom

    # elitisme -> mendapatkan populasi baru dengan mengambil nilai fitness tertinggi
    childFitPopulation = getFitness(childPopulation)
    currentPopulation = fitPopulation + childFitPopulation
    # currentPopulation.sort(key=operator.itemgetter(0),reverse=True)
    currentPopulation.sort(key=operator.itemgetter(0))
    newPopulation = []
    for i in range(len(currentPopulation)/2):
        newPopulation.append(currentPopulation[i])
    print('new population: {0}').format(newPopulation)
    return newPopulation

def main():
    # total population = n
    n = 4
    # panjang kromosom
    k = len(data)-1
    # representasi kromosom | pengecekan terhubung tidaknya
    population = initPopulation(n,k)
    # TODO lakukan GA
    # hitung nilai fitness | jumlahkan total bobotnya
    fitPopulation = getFitness(population)
    for i in range(500):
        fitPopulation = runGA(fitPopulation)
    print('final population: {0}').format(fitPopulation)
    solution = ""
    for i in range(len(fitPopulation[0][1])):
        solution += data[fitPopulation[0][1][i]]+", "
        if data[fitPopulation[0][1][i]] == "G":
            break
    print('Best solution : {0}').format(solution)

main()
