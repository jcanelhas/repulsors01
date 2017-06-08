"""
##########################################################################
####                                                                  ####
####                     Crossovers                                   ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""
import random

from commonfunctions import getTreeDepth,getRandomOperator,traverse,isOperator#*


def crossover(individual1,individual2,maxtreedepth):

    outdepth = 0# 10*10**10
    overgrown = True

    while overgrown == True:
        try:
            cxposindividual1 = random.randint(0, len(individual1) - 1)
            cxposindividual2 = random.randint(0, len(individual2) - 1)
        except:
            print("Crossover Error - Returning empty individuals with 0 on them")
            _=input("Press the <ENTER> key to continue...")
            return ([0],[0])

        subtree1 = traverse(individual1, cxposindividual1)
        subtree2 = traverse(individual2, cxposindividual2)

        #output tree
        output1=list()
        output1[:]=[]

        output2=list()
        output2[:]=[]

        i1p1 = individual1[:len(individual1) - len(subtree1) - cxposindividual1]
        i1p2 = subtree2
        i1p3 = individual1[len(i1p1) + len(subtree1):]

        i2p1 = individual2[:len(individual2) - len(subtree2) - cxposindividual2]
        i2p2 = subtree1
        i2p3 = individual2[len(i2p1) + len(subtree2):]

        output1 = i1p1+i1p2+i1p3
        output2 = i2p1+i2p2+i2p3
        if getTreeDepth(output1,'treedepth') > maxtreedepth or getTreeDepth(output2,'treedepth') > maxtreedepth:
            overgrown = True
            print (".", end="")
        else:
            overgrown = False


    if len(output1) == 2 or len(output2) == 2:
        print('2 ops, lost 1 in cx') # problema !!!!
    if isOperator(output1[0]):
        print('op at wrongpos in cx>>>')  # problema !!!!

    return (output1,output2)



