"""
##########################################################################
####                                                                  ####
####                     read data from files                         ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""

"""this file will include dataset readers"""
from random import shuffle

def readdatafile(filename,startcol,endcol):
    """data should be separated by semicolons and the last column should be the result"""
    import csv
    with open(filename, 'r') as f:
        reader = csv.reader(f,delimiter=';')
        outp = [list(map(float,rec)) for rec in reader]
    return outp



"""Slip dataset in training and test sets"""

def datasetsplitter(inputdatset,splitracio,splitmode):

    """Returns 2 datasets training and test
        inputdataset = dataset to be splited
        splitracio = amount of training vs test data
        splitmode = random -> random pick, first ->pick first rows
    """
    nelements = len(inputdatset)
    ntrainingelements=int(nelements*splitracio)
    ntestelements=int(nelements*(1-splitracio))

    #todo verificar se o numero de elementos se mantem

    if splitmode=='random':
        shuffle(inputdatset)

    trainingset,testset = inputdatset[:ntrainingelements],inputdatset[ntrainingelements:]

    trainingset.sort()
    testset.sort()

    return trainingset,testset

"""Slip dataset in training and test sets"""

def datasetslicer(inputdatset,sliceratio,splitmode):
    #from random import shuffle
    """Returns 2 datasets training and test
        inputdataset = dataset to be splited
        splitracio = amount of training vs test data
        splitmode = random -> random pick, first ->pick first rows
    """
    nelements = len(inputdatset)
    noutelements=int(nelements*sliceratio)

    #todo verificar se o numero de elementos se mantem

    if splitmode=='random':
        shuffle(inputdatset)
        outset = inputdatset[:noutelements]
        outset.sort()
    elif splitmode=='first':
        outset = inputdatset[:noutelements]
    elif splitmode=='first':
        outset = inputdatset[:noutelements]
    elif splitmode=='last':
        outset = inputdatset[:nelements-noutelements]

    return outset