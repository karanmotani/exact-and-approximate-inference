import sys
import random
from functools import reduce
import itertools
from copy import deepcopy

# +b = (B,t)
# -b = (B,f)
burglary = {'+b': 0.001, '-b': 0.999}

# +e = (E,t)
# -e = (E,f)
earthquake = {'+e': 0.002, '-e': 0.998}

# +a = (A,t)
# -a = (A,f)
alarm = {('+b','+e','+a'): 0.95, ('+b','-e','+a'): 0.94, ('-b','+e','+a'): 0.29, ('-b','-e','+a'): 0.001,
         ('+b','+e','-a'): 0.05, ('+b','-e','-a'): 0.06, ('-b','+e','-a'): 0.71, ('-b','-e','-a'): 0.999}

# +j = (J,t)
# -j = (J,f)
johnCalls = {('+a','+j'): 0.9, ('-a','+j'): 0.05,
             ('+a','-j'): 0.1, ('-a','-j'): 0.95}

# +m = (M,t)
# -m = (M,f)
maryCalls = {('+a','+m'): 0.7, ('-a','+m'): 0.01,
             ('+a','-m'): 0.3, ('-a','-m'): 0.99}


# Generating samples based on random number generation
def sampling():
    samples = []

    for i in range(10000):

        b = random.uniform(0, 1)
        e = random.uniform(0, 1)
        a = random.uniform(0, 1)
        j = random.uniform(0, 1)
        m = random.uniform(0, 1)


        # Samples for burglary
        for key, value in burglary.items():
            if key.__contains__('+b'):
                # print(key, value)
                if b < value:
                    B = '+b'
                else:
                    B = '-b'


        # Samples for earthquake
        for key, value in earthquake.items():
            if key.__contains__('+e'):
                # print(key, value)
                if e < value:
                    E = '+e'
                else:
                    E = '-e'


        # Samples for alarm
        for key, value in alarm.items():
            if key.__contains__(B):
                if key.__contains__(E):
                    if key.__contains__('+a'):
                        # print(key, value)
                        if a < value:
                            A = '+a'
                        else:
                            A = '-a'


        # Samples for johnCalls
        for key, value in johnCalls.items():
            if key.__contains__(A):
                if key.__contains__('+j'):
                    # print(key, value)
                    if j < value:
                        J = '+j'
                    else:
                        J = '-j'


        # Samples for maryCalls
        for key, value in maryCalls.items():
            if key.__contains__(A):
                if key.__contains__('+m'):
                    # print(key, value)
                    if m < value:
                        M = '+m'
                    else:
                        M = '-m'

        samples.append((B,E,A,J,M))

    countB = 0
    countE = 0
    countA = 0
    countJ = 0
    countM = 0

    for i in range(len(samples)):
        if samples[i][0] == '+b':
            countB += 1
        if samples[i][1] == '+e':
            countE += 1
        if samples[i][2] == '+a':
            countA += 1
        if samples[i][3] == '+j':
            countJ += 1
        if samples[i][4] == '+m':
            countM += 1

    print('B', 'E', 'A', 'J', 'M')
    print(countB, countE, countA, countJ, countM)

    return samples


# Generating true probabilities for all the entire bayesian network
def getTruthtable():
    truthtable = {}
    table = list(itertools.product([False, True], repeat=5))

    for b, e, a, j, m in table:

        if b == False:
            b = '-b'
        else:
            b = '+b'

        if e == False:
            e = '-e'
        else:
            e = '+e'

        if a == False:
            a = '-a'
        else:
            a = '+a'

        if j == False:
            j = '-j'
        else:
            j = '+j'

        if m == False:
            m = '-m'
        else:
            m = '+m'

        truthtable[(b, e, a, j, m)] = burglary[b] * earthquake[e] * alarm[(b, e, a)] * johnCalls[(a, j)] * maryCalls[
            (a, m)]

    return truthtable


# Getting the Exact probability for enumeration
def getTrueProbability(truthtable, qe):
    probability = 0
    for k,v in truthtable.items():
        temp = list(k)
        if (all(x in temp for x in qe)):
            probability += v
    return probability


# Getting the probability of Samples for Prior Sampling
def getSampleProbability(samples, qe):
    priorSamples = []
    priorSamplesList = []
    for s in samples:
        temp = list(s)
        if (all(x in temp for x in qe)):
            priorSamples.append(s)

    for b, e, a, j, m in priorSamples:
        probability = burglary[b] * earthquake[e] * alarm[(b,e,a)] * johnCalls[(a,j)] * maryCalls[(a,m)]
        priorSamplesList.append(probability)

    return priorSamplesList


# Getting the Likelihood Weights of Samples for Likelihood Weighting
def getLikelihoodWeights(samples, qe, flagB, flagE, flagA, flagJ, flagM):
    lwSamples = []
    lwSamplesList = []
    prob = 1

    for s in samples:
        temp = list(s)
        if (all(x in temp for x in qe)):
            lwSamples.append(s)

    for b, e, a, j, m in lwSamples:

        if flagB is True:
            tempB = burglary[b]
        else:
            tempB = 1.0

        if flagE is True:
            tempE = earthquake[e]
        else:
            tempE = 1.0

        if flagA is True:
            tempA = alarm[(b,e,a)]
        else:
            tempA = 1.0

        if flagJ is True:
            tempJ = johnCalls[(a,j)]
        else:
            tempJ = 1.0

        if flagM is True:
            tempM = maryCalls[(a,m)]
        else:
            tempM = 1.0

        probability = tempB * tempE * tempA * tempJ * tempM

        lwSamplesList.append(probability)

        prob += probability

    # print(lwSamplesList)

    return lwSamplesList, prob

    # countB = 0
    # countE = 0
    # countA = 0
    # countJ = 0
    # countM = 0
    # count = 0
    #
    # for i in range(len(lwSamples)):
    #     if lwSamples[i][0] == '+b':
    #         countB += 1
    #     if lwSamples[i][1] == '+e':
    #         countE += 1
    #     if lwSamples[i][2] == '+a':
    #         countA += 1
    #     if lwSamples[i][3] == '+j':
    #         countJ += 1
    #     if lwSamples[i][4] == '+m':
    #         countM += 1
    #
    # print(countB, countE, countA, countJ, countM)
    #
    # for i in range(len(lwSamplesList)):
    #     if lwSamplesList[i] == 0.04995:
    #         count += 1
    #
    # print('Count is: ', count)


# Setting the Evidence variables for Likelihood Weighting
def getFlags(qe):
    flagB = False
    flagE = False
    flagA = False
    flagJ = False
    flagM = False

    for item in qe:
        if item.__contains__('b'):
            flagB = True

        if item.__contains__('e'):
            flagE = True

        if item.__contains__('a'):
            flagA = True

        if item.__contains__('j'):
            flagJ = True

        if item.__contains__('m'):
            flagM = True

    return flagB, flagE, flagA, flagJ, flagM


# Execution of Exact Inference by Enumeration
def enumeration(evidenceList, queryList):
    exactProbTemp = []
    exactProbFinal = []
    qe = deepcopy(evidenceList)

    print('\n-------------------------------- Exact Inference by Enumeration --------------------------------\n')

    for i in queryList:
        qe.append(i[0])
        pos = getTrueProbability(truthtable, qe)
        qe.pop()

        qe.append(i[1])
        neg = getTrueProbability(truthtable, qe)
        qe.pop()

        exactProbTemp.append((pos, neg))

        p = pos / (pos + neg)
        n = neg / (pos + neg)

        exactProbFinal.append((p, n))

    # print('Exact probability: α', exactProbTemp)
    print('Exact probability:', exactProbFinal)


# Execution of Prior Sampling
def priorSampling(samples, evidenceList, queryList, truthtable):
    priorSamplesProb = []
    priorProbTemp = []
    qe = deepcopy(evidenceList)

    print('\n---------------------------------------- Prior Sampling ----------------------------------------\n')

    for i in queryList:

        qe.append(i[0])
        pos = getSampleProbability(samples, qe)
        qe.pop()

        qe.append(i[1])
        neg = getSampleProbability(samples, qe)
        qe.pop()

        # priorProbTemp.append((len(pos), len(neg)))
        # print(i[0], len(pos))
        # print(i[1], len(neg))

        posTemp = len(pos)/(len(pos)+len(neg))
        negTemp = len(neg)/(len(pos)+len(neg))

        priorSamplesProb.append((posTemp, negTemp))

    print('Prior probability:', priorSamplesProb)


# Execution of Likelihood Weighting
def likelihoodWeighting(samples, evidenceList, queryList):
    lw = []
    qe = deepcopy(evidenceList)

    print('\n------------------------------------- Likelihood Weighting -------------------------------------\n')

    # Fixing the evidence
    flagB, flagE, flagA, flagJ, flagM = getFlags(evidenceList)
    evidence, evidenceValue = getLikelihoodWeights(samples, evidenceList, flagB, flagE, flagA, flagJ, flagM)

    # Fixing the evidence and the query
    for i in queryList:
        qe.append(i[0])
        flagB, flagE, flagA, flagJ, flagM = getFlags(qe)
        pos, posValue = getLikelihoodWeights(samples, qe, flagB, flagE, flagA, flagJ, flagM)
        qe.pop()

        qe.append(i[1])
        flagB, flagE, flagA, flagJ, flagM = getFlags(qe)
        neg, negValue = getLikelihoodWeights(samples, qe, flagB, flagE, flagA, flagJ, flagM)
        qe.pop()

        lw.append((posValue/evidenceValue, negValue/evidenceValue))

    print('Likelihood Weighting:', lw)


# Reading the inputs: Evidence and Query
# Make Evidence list and Query list
def readInput():
    evidence = []
    evidenceList = []
    queryList = []

    # qe = sys.argv[1]
    qe = '[< A,f >][B,J]'
    qe = qe.replace('[','').replace('<','').replace('>','').replace(']','').split(' ')
    for i in qe:
        if i != '':
            evidence.append(i)

    query = evidence.pop()
    query = query.split(',')


    # Get the evidence List
    for e in evidence:
        if 'B' in e:
            if 't' in e:
                B = '+b'
            else:
                B = '-b'
            evidenceList.append(B)

        if 'E' in e:
            if 't' in e:
                E = '+e'
            else:
                E = '-e'
            evidenceList.append(E)

        if 'A' in e:
            if 't' in e:
                A = '+a'
            else:
                A = '-a'
            evidenceList.append(A)

        if 'J' in e:
            if 't' in e:
                J = '+j'
            else:
                J = '-j'
            evidenceList.append(J)

        if 'M' in e:
            if 't' in e:
                M = '+m'
            else:
                M = '-m'
            evidenceList.append(M)


    # Get the query List
    for i in query:
        if 'B' == i:
            queryList.append(('+b', '-b'))
        if 'E' == i:
            queryList.append(('+e', '-e'))
        if 'A' == i:
            queryList.append(('+a', '-a'))
        if 'J' == i:
            queryList.append(('+j', '-j'))
        if 'M' == i:
            queryList.append(('+m', '-m'))

    return evidenceList, queryList


# Main function
if __name__ == '__main__':

    evidenceList, queryList = readInput()
    truthtable = getTruthtable()
    samples = sampling()
    enumeration(evidenceList, queryList)
    priorSampling(samples, evidenceList, queryList, truthtable)
    likelihoodWeighting(samples, evidenceList, queryList)
