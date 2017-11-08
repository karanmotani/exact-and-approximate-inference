import sys
import random
from functools import reduce

# +b = (B,t)
# -b = (B,f)
import itertools

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

    print(countB, countE, countA, countJ, countM)

    return samples


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


def getProbability(truthtable, qe):
    probability = 0
    for k,v in truthtable.items():
        temp = list(k)
        if (all(x in temp for x in qe)):
            probability += v
    return probability

    '''
    for k,v in truthtable.items():
        temp = list(k)
        if (all(x in temp for x in qe)):
            exactProb+= v

    print(exactProb)
    '''


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


def prior(samples, evidenceList, queryList, truthtable):

    priorSamplesProb = []
    priorProbTemp = []
    exactProbTemp = []
    exactProbFinal = []
    qe = evidenceList

    priorProb = 0
    exactProb = 0

    print('Evidences: ', evidenceList)
    print('Queries: ', queryList)


    # --------------------------- Prior Probability ----------------------------

    # for s in samples:
    #     temp = list(s)
    #     if (all(x in temp for x in evidenceList)):
    #         priorSamples.append(s)
    #
    #
    # for b, e, a, j, m in priorSamples:
    #     probability = burglary[b] * earthquake[e] * alarm[(b,e,a)] * johnCalls[(a,j)] * maryCalls[(a,m)]
    #     priorProb += probability
    #
    # print('Prior Probability: ', priorProb)


    for i in queryList:

        qe.append(i[0])
        # print('Joint Evidence and Query list: ', qe)

        pos = getSampleProbability(samples, qe)
        qe.pop()

        qe.append(i[1])
        # print('Joint Evidence and Query list: ', qe)

        neg = getSampleProbability(samples, qe)
        qe.pop()

        priorProbTemp.append((len(pos), len(neg)))

        posTemp = len(pos)/(len(pos)+len(neg))
        negTemp = len(neg)/(len(pos)+len(neg))

        priorSamplesProb.append((posTemp, negTemp))

        # priorProbTemp.append(len(pos))
    print('Prior probability:', priorSamplesProb)




    # --------------------------- Exact Probability ----------------------------

    for i in queryList:

        qe.append(i[0])
        # print('Joint Evidence and Query list: ', qe)

        pos = getProbability(truthtable, qe)
        qe.pop()

        qe.append(i[1])
        # print('Joint Evidence and Query list: ', qe)

        neg = getProbability(truthtable, qe)
        qe.pop()

        exactProbTemp.append((pos, neg))

    # print('Exact probability: α', exactProbTemp)

    for p, n in exactProbTemp:
        pos = p/(p+n)
        neg = n/(p+n)
        exactProbFinal.append((pos, neg))

    print('Exact probability:', exactProbFinal)


# Reading the inputs:
# Evidence and Query
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
    prior(samples, evidenceList, queryList, truthtable)

