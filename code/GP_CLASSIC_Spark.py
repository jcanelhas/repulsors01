#importar ficheiros
import copy
import os
import time
import shutil
from commonfunctions import getRPNdepth
from crossovers import crossover
from datasetreaders import *
from fitnessevaluators import getfitness,regressioncomparator,saveresulttable
from generators import *
from graphfunctions import create_graph
from mutators import Mutate
from population_selectors import tournment_selection
from db_operations import dblog_startgpjob,dblog_insertgpjobdetails,dblog_finishgpjob,dblog_insertgpjobregressioniteration,dblog_insertgpjobiterationpopulationfitness
from math import log2
from plotfunctions import saveplotregressionresults
from math import log2, inf



population=list()


def exec_GP_Classic_spark(runparameters, _):

    print(runparameters)


    global soldic

    if runparameters['USE_SOLUTION_DICTIONARY']:
        soldic={}


    #Create Directories
    if not os.path.exists(str(runparameters['RUN_ID'])):
        os.makedirs(str(runparameters['RUN_ID']))
        os.makedirs(str(runparameters['RUN_ID'] + '/plots'))
        os.makedirs(str(runparameters['RUN_ID'] + '/graphs'))
        os.makedirs(str(runparameters['RUN_ID'] + '/generations'))
        os.makedirs(str(runparameters['RUN_ID'] + '/resulttables'))

    #save run parameter file
    paramfile = open(str(runparameters['RUN_ID']) + '/runparameters.csv','w')
    for param in runparameters.items():
        paramfile.write(str(param)+'\n')
    paramfile.close()


    #log the start of the job
    JOBDBID = dblog_startgpjob(runparameters)

    datafile=readdatafile(runparameters['DATAFILENAME'],1,1)
    originaldatafile=readdatafile(runparameters['DATAFILENAME'],1,1)
    #choose how much of the original dataset will be used
    tmpdataset=datasetslicer(datafile,runparameters['DATASETPERCENTAGETOUSE'],'random')

    trainingset,testset=datasetsplitter(tmpdataset,runparameters['TRAININGTESTRATIO'],'random')

    #save the training, test and validation files
    trainingsetfile = open(str(runparameters['RUN_ID']) + '/trainingset.txt', 'w')
    for elem in trainingset:
        trainingsetfile.write(str(elem) + "\n")
    trainingsetfile.close()
    testsetfile = open(str(runparameters['RUN_ID']) + '/testset.txt', 'w')
    for elem in testset:
        testsetfile.write(str(elem) + "\n")
    testsetfile.close()

    print(trainingset,testset)


    #fittable=generate_fnresult_table(target)

    outfile=open(str(runparameters['RUN_ID']) + '/' + runparameters['OUTPUT_FILE_NAME'],'w')
    outfile.write("----------GLOBALS--------------\n")
    for param in runparameters.items():
        outfile.write(str(param)+'\n')
    outfile.write("-------------------------------\n")
    outfile.write(str(time.localtime())+'\n')
    outfile.write("-------------------------------\n")
    outfile.close()

    #gerar populacao inicial
    population=list()
    population[:]=[]
    population = GeneratePopulation(runparameters['POPULATION_SIZE'], runparameters['PROGRAM_DEPTH'], runparameters['TREE_GENERATION_MODE'], runparameters['N_VARIABLES'], runparameters['VARIABLERATIO'])

    if runparameters['SAVE_POPULATION']==True:
        genfile = open(str(runparameters['RUN_ID']) + '/generations/' + '0.txt', 'w')
        for ind in population:
            genfile.write(str(ind) + '\n')
        genfile.close()
        #para a DB
        inum = 0
        for ind in population:
            inum=inum+1
            testsetfitness = getfitness(ind, testset, {}, False)
            trainingsetfitness = getfitness(ind,trainingset, {}, False)
            dblog_insertgpjobiterationpopulationfitness(JOBDBID,str(runparameters['RUN_ID']),0,inum,ind,trainingsetfitness,testsetfitness,0)




    runbestelementfitness=10*10**200
    runbestelement=list()
    runbestelement[:]=[]
    runbestelementiteration=0

    iterbestelement=list()


    outfitfile = open(str(runparameters['RUN_ID']) + '/' + runparameters['OUTPUT_FILE_NAME_FITNESS'], 'w')
    outfitfile.write('iteration;trainingsetfitness;validationsetfitness;testsetfitness;trainingsetentropy;validationsetentropy;testsetentropy\n')
    outfitfile.close()

    ###LET THE GAMES BEGIN
    tmppopulation=list()
    tmppopulation[:]=[]

    FOUNDSOLUTION=False
    overfitting=False
    testfit=10*10**300 #dont use inf due to mysql log float(inf)

    trainingentropy=0
    testentropy=0
    validationentropy=0

    for n in range (1,runparameters['MAX_GENERATIONS']+1):  #Repeat iterations

        print(str(runparameters['RUN_ID']) + '----------------------' + str(n) + " / Dictionary size : " + str(len(soldic)))
        #debug
        iterbestelement[:] = []
        iterbestelementfitness=10*10**200 #very big and unfit number

        tmppopulation[:] = []

        for m in range(0, int(runparameters['POPULATION_SIZE'] / 2)):
            #print('----------------------' + str(len(population)))
            tournementchamp1, tournementchamp1fitness = tournment_selection(population, runparameters['TOURNMENT_SIZE'],trainingset)
            tournementchamp2, tournementchamp2fitness = tournment_selection(population, runparameters['TOURNMENT_SIZE'],trainingset)
            #crossovers
            if random() < runparameters['CROSSOVER_RATE']  and m>0:
                newind1, newind2=crossover(tournementchamp1,tournementchamp2,runparameters['MAX_PROGRAM_DEPTH'])
            else:
                newind1 = tournementchamp1[:]
                newind2 = tournementchamp2[:]
            #mutation
            if random() > runparameters['MUTATION_RATE']:
                newind1 = Mutate(newind1, runparameters['MAX_PROGRAM_DEPTH'], runparameters['MUTATION_MODE'], runparameters['N_VARIABLES'],runparameters['VARIABLERATIO'])
            if random() > runparameters['MUTATION_RATE']:
                newind2 = Mutate(newind2, runparameters['MAX_PROGRAM_DEPTH'], runparameters['MUTATION_MODE'],runparameters['N_VARIABLES'], runparameters['VARIABLERATIO'])

            #recalcular fitnesses
            newind1fitness = getfitness(newind1, trainingset, soldic)
            newind2fitness = getfitness(newind2, trainingset, soldic)

            tmppopulation.append(newind1)
            tmppopulation.append(newind2)

            if newind1fitness<newind2fitness:
                cyclebestelement = newind1[:]
                cyclebestelementfitness=newind1fitness
            else:
                cyclebestelement = newind2[:]
                cyclebestelementfitness = newind2fitness

            #iteracao
            if cyclebestelementfitness<iterbestelementfitness:
                iterbestelement=cyclebestelement[:]
                iterbestelementfitness=cyclebestelementfitness
                iterbesttestfitness=getfitness(iterbestelement, testset, {}, False)
            #global
            if iterbestelementfitness<runbestelementfitness:
                runbestelement=iterbestelement[:]
                runbestelementfitness=iterbestelementfitness
                besttestfitness=(runbestelement, testset, {}, False)
                runbestelementiteration = n
                print(str(m) + ":" + str(n) + ">>>" + str(runbestelementfitness))

                #log if needed...
                #if runparameters['SAVE_PLOTS']:
                #    saveplotregressionresults(runbestelement, trainingset, "++" + str(n) + "_" + str(m), runparameters['RUN_ID'])
                #SaveResultTable(runbestelement, trainingset, "train__" + str(n) + "_" + str(m), runparameters['RUN_ID'])
                # dblog_insertgpjobregressioniteration(JOBDBID, RUN_ID, n, bestelement, trainingset)
                #if runparameters['SAVE_GRAPHS']:
                #    create_graph(runbestelement, str(runparameters['RUN_ID']) + '/graphs/' + str(n) + '.dot')


            #dblog_insertgpjobregressioniteration(JOBDBID, runparameters['RUN_ID'], n, iterbestelement, trainingset)


            if cyclebestelementfitness<runparameters['FITNESSTHRESHOLD']:
                print("Perfect fit fount --- ")
                print(str(m) + ":" + str(n) + ">>>" + str(runbestelementfitness))
                FOUNDSOLUTION=True

            if FOUNDSOLUTION==True:
                break
        print(str(runparameters['DATAFILENAME']) + " ------------------------")

        population = copy.deepcopy(tmppopulation)

        if runparameters['ELITISM']==True:
            population[0]=runbestelement
        rpnbest=''
        iterrpnbest=''
        for i in runbestelement:
            rpnbest=rpnbest+i+' '
        for i in iterbestelement:
            iterrpnbest=iterrpnbest+i+' '



        outfile = open(str(runparameters['RUN_ID']) + '/' + runparameters['OUTPUT_FILE_NAME'], 'a')
        outfile.write('---('+ str(n) +')-------------------------------------------------\n')
        outfile.write('localtime: ' + str(time.localtime()) + '\n')
        outfile.write('runtime:' + str(time.time()-runparameters['START_TIME']) + '\n')
        outfile.write('Best fit at iteration : ' + str(n) + "=" + str(iterbestelementfitness) + "\n")
        outfile.write("Best individual at iteration : " + iterrpnbest + "\n")
        outfile.write('Current best fit      : ' + str(n) + "=" + str(runbestelementfitness) + "\n")
        outfile.write("Best individual so far       : " + str(rpnbest) + '\n')
        outfile.close()



        if runparameters['SAVE_POPULATION'] == True:
            genfile=open(str(runparameters['RUN_ID']) + '/generations/' + str(n) + '.txt','w')
            for ind in population:
                genfile.write(str(ind) + '\n')
            genfile.close()

            # #ocupa demasiado espaço
            # #para a DB
            # inum = 0
            # for ind in population:
            #     inum=inum+1
            #     testsetfitness = getfitness(ind, testset, {}, False)
            #     trainingsetfitness = getfitness(ind,trainingset, {}, False)
            #
            #     dblog_insertgpjobiterationpopulationfitness(JOBDBID,str(runparameters['RUN_ID']),n,inum,ind,trainingsetfitness,testsetfitness,0)

        #calculate fitnesses
        testsetfitness=getfitness(runbestelement, testset,{},False)
        validationsetfitness=0
        #calculate entropy
        #in training set
        trainingentropy=trainingentropy+runbestelementfitness*log2(runbestelementfitness)
        #in the testset
        testentropy=testentropy+testsetfitness*log2(testsetfitness)
        #in the validationset
        validationentropy=0


        outfitfile = open(str(runparameters['RUN_ID']) + '/' + runparameters['OUTPUT_FILE_NAME_FITNESS'], 'a')
        outfitfile.write(str(n) + ';' +str(runbestelementfitness) + ";" + str(validationsetfitness) +";" + str(testsetfitness) +';' +str(trainingentropy) + ";" + str(validationentropy) +";" + str(testentropy) + "\n" )
        outfitfile.close()

        #write to db
        dblog_insertgpjobdetails(JOBDBID, runparameters['RUN_ID'], n, runbestelementfitness, validationsetfitness, testsetfitness,trainingentropy, validationentropy, testentropy, runbestelement, iterbestelement,iterbestelementfitness, 0, iterbesttestfitness, 0)

        saveplotregressionresults(runbestelement, trainingset, str(n), runparameters['RUN_ID'])
        saveresulttable(runbestelement, trainingset, "train_" + str(n), runparameters['RUN_ID'])
        saveresulttable(runbestelement, testset, "test_" + str(n), runparameters['RUN_ID'])

        if runparameters['SAVE_GRAPHS']:
            create_graph(runbestelement, str(runparameters['RUN_ID']) + '/graphs/' + str(n) + '.dot')


        if FOUNDSOLUTION == True:
            break

    print(runbestelement)
    print(str(runparameters['DATAFILENAME']) +" ------------------------")
    print(runbestelement)
    print ('Training Fitness:')
    print (getfitness(runbestelement, trainingset,{},False))
    print ('Test Fitness:')
    print (getfitness(runbestelement, testset,{},False))


    if runparameters['SAVE_PLOTS']:
        saveplotregressionresults(runbestelement, trainingset, "FINAL_TRAINING_" + str(m), runparameters['RUN_ID'])
        saveplotregressionresults(runbestelement, testset, "FINAL_TEST_" + str(m), runparameters['RUN_ID'])
        saveresulttable(runbestelement, trainingset, "Final_Training", runparameters['RUN_ID'])
        saveresulttable(runbestelement, testset, "Final_Test", runparameters['RUN_ID'])

    outfmlfile = open(str(runparameters['RUN_ID']) + '/result_fmla.txt', 'w')
    outfmlfile.write(str(runbestelement) + "\n")
    outfmlfile.close()

    clean = ''
    for i in runbestelement:
        clean = clean + i + ' '
        dblog_finishgpjob(JOBDBID, "True", str(FOUNDSOLUTION), n, clean, runbestelementfitness,getfitness(runbestelement, testset, {}, False),0, len(runbestelement),runbestelementiteration,0,getRPNdepth(runbestelement))

    regcomp=regressioncomparator(runbestelement, originaldatafile)

    outregfile = open(str(runparameters['RUN_ID']) + '/regcomparisson.txt', 'w')
    for elem in regcomp:
        outregfile.write(str(elem[0]) + ";" + str(elem[1]) + "\n")
    outregfile.close()



    if runparameters['SAVE_POPULATION'] == True:
        n=n+1
        genfile = open(str(runparameters['RUN_ID']) + '/generations/' + str(n) + '.txt', 'w')
        for ind in population:
            genfile.write(str(ind) + '\n')
        genfile.close()
        # # Save to DB
        # inum = 0
        # for ind in population:
        #     inum = inum + 1
        #     testsetfitness = getfitness(ind, testset, {}, False)
        #     trainingsetfitness = getfitness(ind, trainingset, {}, False)
        #     dblog_insertgpjobiterationpopulationfitness(JOBDBID, str(runparameters['RUN_ID']), n, inum, ind,trainingsetfitness, testsetfitness, 0)

    tmppopulation[:] = []


    print("--------------- FINISHED ---------------")
    shutil.move(str(runparameters['RUN_ID']), 'completedruns/' + str(runparameters['RUN_ID']))


    return 1



