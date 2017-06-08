# coding=utf-8
import datetime
import time
from random import random

from GP_CLASSIC import exec_GP_Classic
from GP_CLASSIC_LEARNONLY import exec_GP_ClassicLearnOnly
from GP_REPULSORS_04 import exec_GP_repulsors_04
from GP_REPULSORS_05 import exec_GP_repulsors_05
from GP_REPULSORS_07 import exec_GP_repulsors_07
from GP_REPULSORS_08 import exec_GP_repulsors_08
from GP_REPULSORS_09 import exec_GP_repulsors_09

soldic = {'jorge':0}

###GLOBAIS
START_TIME = time.time()
RUN_ID = (datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))  # acrescentar %f se for preciso mais grnularidade
USE_SOLUTION_DICTIONARY = True

# PARAMETERS
PROGRAM_DEPTH = 6 # acima de 3
MAX_PROGRAM_DEPTH = 12
POPULATION_SIZE = 200
TOURNMENT_SIZE = 4  # 2 é bom
REPULSOR_TOURNMENT_SIZE = 2
MAX_GENERATIONS = 100  # minimo 150
TREE_GENERATION_MODE = 'rhah'
MUTATION_MODE = 'subtree'
BLOAT_CONTROL_METHOD = 'treedepth' #Can be stacksize, treedepth or NONE
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.01
ELITISM = True
PENALIZE_ASYMPTOTES = False
ROUNDRESULTTOINTEGER=False
METHOD = 'GP_CLASSIC' #'GP_REPULSORS_09'#'GP_REPULSORS_08'# 'GP_CLASSIC_LEARNONLY'#
N_VARIABLES = 1#total number of variables being evaluated
DATASETPERCENTAGETOUSE = 1 #0.5 #1 # how much of the data set is to be used
TRAININGTESTRATIO = 0.8  # percentage of samples that go into the training set : 0.7 means 70% to training and 30 to test set
VALIDATIONSETSIZE = 0.3  # after the removal of the test set , percentage of data to use for validation purposes
VARIABLERATIO = 0.99  # percentage of variables/constants in generation of trees
DATAFILENAME = 'datasets/fittable_sin.txt'
FITNESSTHRESHOLD = 0.00000001
#For repulsor use
OVERFITTHRESHOLD=0
# Logging
SAVE_POPULATION = True # False# Save the whole population sample in the run ? wow much disk many memory such population
SAVE_PLOTS = True  # Savesum(nruns) the figure (sorted 2D only)
SAVE_GRAPHS = True
OUTPUT_FILE_NAME = 'workfile.csv' + str(random()) + '.txt'
OUTPUT_FILE_NAME_FITNESS = 'fitfile_' + str(RUN_ID) + '.txt'


# Create dictionary with run parameters
runparameters = dict()
runparameters['START_TIME'] = START_TIME
runparameters['RUN_ID'] = RUN_ID
runparameters['PROGRAM_DEPTH'] = PROGRAM_DEPTH
runparameters['MAX_PROGRAM_DEPTH'] = MAX_PROGRAM_DEPTH
runparameters['POPULATION_SIZE'] = POPULATION_SIZE
runparameters['TOURNMENT_SIZE'] = TOURNMENT_SIZE
runparameters['REPULSOR_TOURNMENT_SIZE'] = REPULSOR_TOURNMENT_SIZE
runparameters['MAX_GENERATIONS'] = MAX_GENERATIONS
runparameters['TREE_GENERATION_MODE'] = TREE_GENERATION_MODE
runparameters['MUTATION_MODE'] = MUTATION_MODE
runparameters['CROSSOVER_RATE'] = CROSSOVER_RATE
runparameters['MUTATION_RATE'] = MUTATION_RATE
runparameters['ELITISM'] = ELITISM
runparameters['BLOAT_CONTROL_METHOD'] = BLOAT_CONTROL_METHOD
runparameters['METHOD'] = METHOD
runparameters['PENALIZE_ASYMPTOTES'] = PENALIZE_ASYMPTOTES
runparameters['ROUNDRESULTTOINTEGER'] = ROUNDRESULTTOINTEGER
runparameters['N_VARIABLES'] = N_VARIABLES
runparameters['TRAININGTESTRATIO'] = TRAININGTESTRATIO
runparameters['DATASETPERCENTAGETOUSE'] = DATASETPERCENTAGETOUSE
runparameters['VALIDATIONSETSIZE'] = VALIDATIONSETSIZE
runparameters['VARIABLERATIO'] = VARIABLERATIO
runparameters['DATAFILENAME'] = DATAFILENAME
runparameters['USE_SOLUTION_DICTIONARY'] = USE_SOLUTION_DICTIONARY
runparameters['FITNESSTHRESHOLD'] = FITNESSTHRESHOLD
runparameters['OVERFITTHRESHOLD'] = OVERFITTHRESHOLD
runparameters['SAVE_POPULATION'] = SAVE_POPULATION
runparameters['SAVE_PLOTS'] = SAVE_PLOTS
runparameters['SAVE_GRAPHS'] = SAVE_GRAPHS
runparameters['OUTPUT_FILE_NAME'] = OUTPUT_FILE_NAME
runparameters['OUTPUT_FILE_NAME_FITNESS'] = OUTPUT_FILE_NAME_FITNESS


def main():


#    K = [1.01, 1.5, 2.5]
#    for n in K:
#        OVERFITTHRESHOLD = n
#        runparameters['OVERFITTHRESHOLD'] = OVERFITTHRESHOLD
    for i in range(0,1):
        START_TIME = time.time()
        RUN_ID = (datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))  # acrescentar %f se for preciso mais grnularidade

        runparameters['START_TIME'] = START_TIME
        runparameters['RUN_ID'] = RUN_ID

        if runparameters['METHOD'] == 'GP_CLASSIC_LEARNONLY':
            exec_GP_ClassicLearnOnly(runparameters, 0)
        if runparameters['METHOD'] == 'GP_CLASSIC':
            exec_GP_Classic(runparameters, 0)
        if runparameters['METHOD'] == 'GP_REPULSORS_04':
            exec_GP_repulsors_04(runparameters, 0)
        if runparameters['METHOD'] == 'GP_REPULSORS_05':
            exec_GP_repulsors_05(runparameters, 0)
        if runparameters['METHOD'] == 'GP_REPULSORS_07':
            exec_GP_repulsors_07(runparameters, 0)
        if runparameters['METHOD'] == 'GP_REPULSORS_08':
            exec_GP_repulsors_08(runparameters, 0)
        if runparameters['METHOD'] == 'GP_REPULSORS_09':
            exec_GP_repulsors_09(runparameters, 0)

if __name__ == "__main__":
    main()