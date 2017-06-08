"""
##########################################################################
####                                                                  ####
####                     Population selection                         ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""

from random import random, randint
from fitnessevaluators import getfitness
from math import *
from fitnessevaluators import getregressionresult





def tournment_selection(population,tournement_size,fittable,resultdic={},roundtointeger=False):


    tournementbestfitness=10*10**10
    tournement=list()
    tournementfitness=list()
    tournementbestelement=list()

    tournement[:] = []
    tournementfitness[:]=[]
    tournementbestfitness=10*10**350
    tournementbestelement[:]=[]

    for i in range(0,tournement_size):    #adicionar n individuos ao torneio
        randomindividual=population[randint(0,len(population)-1)][:]
        tournement.append(randomindividual)
        tmpfitness=getfitness(randomindividual,fittable,resultdic,True,'rms',roundtointeger)
        tournementfitness.append(tmpfitness)
        if tournementbestfitness>tmpfitness:
            tournementbestfitness=tmpfitness
            tournementbestelement=randomindividual[:]

    if len(tournementbestelement)==0:
        print("best fit  " + str(tournementbestfitness))
        print("best fit  " + str(tmpfitness))
        print("best element is null")
        quit()
    return (tournementbestelement,tournementbestfitness)

def proportional(population):
    #todo fitness proportional selection
    #maybe later
    print()




def multiobjective_scoring(pupulation, objectives):
    """To be done"""
    newpopulation=list()
    newpopulation[:]=[]

    return newpopulation



def getrepulsorlistdistancerms(individualresult, wallofshame, userepulsordistance=False):

    nresults=len(individualresult)
    nshames=len(wallofshame)
    distance=0
    for indshame in wallofshame:
        for n,resultshame in enumerate(indshame[1]):
            if userepulsordistance==True:
                distance = distance + sqrt((resultshame - individualresult[n]) ** 2)*indshame[2] ###isto nao faz mto sentido
            else:
                distance = distance + sqrt((resultshame - individualresult[n]) ** 2)
        distance=distance/nresults
    distance=distance/nshames
    return distance



def getrepulsorlistdistanceeuclidean(individualresult, wallofshame):

    def euclideandistance(a, b):
        dist = 0
        for idx, elem_b in enumerate(b):
            dist += (a[idx] - elem_b) ** 2
        dist = sqrt(dist)
        return dist


    distance=0
    for ind in wallofshame:


        distance = distance + euclideandistance(ind[1],individualresult)

    distance = distance / len(wallofshame)
    return distance



def repulsortournment(population,dtset,tournement_size,repulsorlist,distanceevaluationmethod='simple'):#,fittable,resultdic={}):
    #from random import randint

    bestrtelement=list()
    bestrtelement[:] = []
    bestrtelementfitness=0
    randomrtindividual=list()
    randomrtindividual[:]=[]
    randomrtindividualfitness=0

    #select random elements from population
    for i in range(0,tournement_size):
        randomrtindividual=population[randint(0, len(population) - 1)][:]
        if distanceevaluationmethod == 'euclidean':

            randomrtindividualfitness = getrepulsorlistdistanceeuclidean(getregressionresult(randomrtindividual, dtset), repulsorlist)
        else:
            randomrtindividualfitness = getrepulsorlistdistancerms(getregressionresult(randomrtindividual, dtset), repulsorlist, False)
        if i==0:
            bestrtelement=randomrtindividual[:]
            bestrtelementfitness=randomrtindividualfitness#getwallofshamedistance(bestelementfitness,repulsorlist)
        if randomrtindividualfitness>bestrtelementfitness:
            bestrtelement=randomrtindividual[:]
            bestrtelementfitness=randomrtindividualfitness#getwallofshamedistance(bestelementfitness,repulsorlist)

    return bestrtelement

def repulsortournment_distances01(population,dtset,tournement_size,repulsorlist):#,fittable,resultdic={}):
    #from random import randint
    #from fitnessevaluators import getregressionresult
    bestrtelement=list()
    bestrtelement[:] = []
    bestrtelementfitness=0
    randomrtindividual=list()
    randomrtindividual[:]=[]
    randomrtindividualfitness=0

    #select random elements from population
    for i in range(0,tournement_size):
        randomrtindividual=population[randint(0, len(population) - 1)][:]
        randomrtindividualfitness=getrepulsorlistdistancerms(getregressionresult(randomrtindividual, dtset), repulsorlist, True)
        if i==0:
            bestrtelement=randomrtindividual[:]
            bestrtelementfitness=randomrtindividualfitness#getwallofshamedistance(bestelementfitness,repulsorlist)
        if randomrtindividualfitness>bestrtelementfitness:
            bestrtelement=randomrtindividual[:]
            bestrtelementfitness=randomrtindividualfitness#getwallofshamedistance(bestelementfitness,repulsorlist)

    return bestrtelement