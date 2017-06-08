"""
##########################################################################
####                                                                  ####
####                     Database operations                          ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""


import pymysql
import platform
from commonfunctions import *


DBHOSTNAME= IP ADDRESS
DBUSER=USER
DBPASS=PASS
DBNAME=DBNAME


def dblog_startgpjob(runparameters):

    conn = pymysql.connect(host=DBHOSTNAME, user=DBUSER, passwd=DBPASS, db=DBNAME)
    x = conn.cursor()

    computername=platform.uname()[1]

    try:
        sql="INSERT INTO gp_log2.tbl_runs (runid,PROGRAM_DEPTH,MAX_PROGRAM_DEPTH,POPULATION_SIZE,TOURNMENT_SIZE,REPULSOR_TOURNMENT_SIZE,MAX_ITERATIONS,TREE_GENERATION_MODE,BLOATCONTROLMETHOD,MUTATION_MODE,CROSSOVER_RATE,MUTATION_RATE,ELITISM,N_VARIABLES,DATASETPERCENTAGETOUSE,TRAININGTESTRATIO,VALIDATIONSETSIZE,VARIABLERATIO,DATAFILENAME,FITNESSTHRESHOLD,METHOD,OVERFITTHRESHOLD,HOST,PENALIZE_ASYMPITOTES,starttime) VALUES ('%s',%s,%s,%s,%s,%s,%s,'%s','%s','%s',%s,%s,'%s',%s,%s,%s,%s,%s,'%s',%s,'%s',%s,'%s','%s',now());" % \
            (runparameters['RUN_ID'],runparameters['PROGRAM_DEPTH'],runparameters['MAX_PROGRAM_DEPTH'],runparameters['POPULATION_SIZE'],runparameters['TOURNMENT_SIZE'],runparameters['REPULSOR_TOURNMENT_SIZE'],runparameters['MAX_GENERATIONS'],runparameters['TREE_GENERATION_MODE'],runparameters['BLOAT_CONTROL_METHOD'],runparameters['MUTATION_MODE'],runparameters['CROSSOVER_RATE'],runparameters['MUTATION_RATE'],runparameters['ELITISM'],runparameters['N_VARIABLES'],runparameters['DATASETPERCENTAGETOUSE'],runparameters['TRAININGTESTRATIO'],runparameters['VALIDATIONSETSIZE'],runparameters['VARIABLERATIO'],runparameters['DATAFILENAME'],runparameters['FITNESSTHRESHOLD'],runparameters['METHOD'],runparameters['OVERFITTHRESHOLD'],computername,runparameters['PENALIZE_ASYMPTOTES'])
        x.execute(sql)

        conn.commit()
        lastid=x.lastrowid

        #parameters
        x = conn.cursor()
        for p in runparameters:
            sql = "INSERT INTO gp_log2.tbl_runs_parameters (parent_run,runid,parameter,value) VALUES (%s,'%s','%s','%s');" % \
                  (lastid, runparameters['RUN_ID'],p,runparameters[p])
            x.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()

    conn.close()
    return lastid


def dblog_finishgpjob(jobid, completed, solutionfound, iterations, bestelement, besttrainfit, besttestfit,bestvalidationfit, bestindividualsize,runbestelementiter,nrepulsors,solutiondepth):
    conn = pymysql.connect(host=DBHOSTNAME, user=DBUSER, passwd=DBPASS, db=DBNAME)
    x = conn.cursor()
    try:
        sql="UPDATE gp_log2.tbl_runs SET completed='%s',solutionfound='%s',iterations=%s,bestelement='%s',bestelementsize=%s,besttrainfitness=%s,besttestfitness=%s,bestvalidationfitness=%s,runbestelementiteration=%s,nrepulsors=%s,solutiondepth=%s,finishtime=NOW() WHERE idtbl_runs=%s;" % \
            (completed,solutionfound,iterations,bestelement,bestindividualsize,besttrainfit,besttestfit,bestvalidationfit,runbestelementiter,nrepulsors,solutiondepth,jobid)
        x.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()
    conn.close()


def dblog_insertgpjobdetails(jobid, parentjobid, iteration, trainfit,validationfit, testfit, trainentropy,validationentropy, testentropy, bestindividual,iter_bestindividual,iter_besttrainfitness,iter_bestvalidationfitness,iter_besttestfitness,overfitting):
    conn = pymysql.connect(host=DBHOSTNAME, user=DBUSER, passwd=DBPASS, db=DBNAME)
    x = conn.cursor()
    bestindividuallenght=len(bestindividual)
    bestindividualdepth=getRPNdepth(bestindividual)
    bestindividualclean = ''
    for i in bestindividual:
        bestindividualclean = bestindividualclean + i + ' '
    bestiterindividuallenght=len(iter_bestindividual)
    bestiterindividualclean = ''
    for i in iter_bestindividual:
        bestiterindividualclean = bestiterindividualclean + i + ' '
    try:
        sql="INSERT INTO gp_log2.tbl_runs_detail (parent_run,parent_runid,iteration,trainfitness,validationfitness,testfitness,trainentropy,testentropy,validationentropy,bestindividual,bestindividuallenght,overfitted,iter_bestindividual,iter_besttrainfitness,iter_bestvalidationfitness,iter_besttestfitness,iter_bestindividual_lenght,iter_bestindividual_depth,modtime) VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,'%s',%s,%s,%s,%s,%s,now());" % \
            (jobid,parentjobid,iteration,trainfit,validationfit,testfit,trainentropy,testentropy,validationentropy,bestindividualclean,bestindividuallenght,overfitting,bestiterindividualclean,iter_besttrainfitness,iter_bestvalidationfitness,iter_besttestfitness,bestiterindividuallenght,bestindividualdepth)
        x.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()
    conn.close()


def dblog_insertgpjobregressioniteration(jobid, parentjobid, iteration, formula, fittable):
    from commonfunctions import parseRPN
    conn = pymysql.connect(host=DBHOSTNAME, user=DBUSER, passwd=DBPASS, db=DBNAME)
    x = conn.cursor()
    xx=0
    try:
        for line in fittable:
            xx = xx + 1
            tmpfmla = formula[:]
            for n in range(0, len(tmpfmla)):
                if tmpfmla[n][0] == 'x':
                    value = line[int(tmpfmla[n][1:])]
                    tmpfmla[n] = str(value)
            tmpfmla1 = parseRPN(tmpfmla)
            tmpfmla2 = line[len(line) - 1]
            sql="INSERT INTO gp_log2.tbl_regressioniterations (parentrun,parent_runid,iteration,elemnum,result,target) VALUES (%s,'%s',%s,%s,%s,%s);" % \
                (jobid,parentjobid,iteration,xx,tmpfmla1,tmpfmla2)
            x.execute(sql)
            conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()
    conn.close()


def dblog_insertgpjobiterationpopulationfitness(jobid, parentjobid, iteration,individualnumber, individual, trainfitness,testfitness,validationfitness):
    conn = pymysql.connect(host=DBHOSTNAME, user=DBUSER, passwd=DBPASS, db=DBNAME)
    x = conn.cursor()
    xx=0
    individuallenght=len(individual)
    individualclean = ''
    for i in individual:
        individualclean = individualclean + i + ' '
    try:
        sql="INSERT INTO gp_log2.tbl_runs_populations (parent_run,iteration,parent_runid,individualnumber,individual,individuallenght,trainfitness,testfitness,validationfitness) VALUES ('%s',%s,'%s',%s,'%s',%s,%s,%s,%s);" % \
            (jobid,iteration,parentjobid,individualnumber,individualclean,individuallenght,trainfitness,testfitness,validationfitness)
        x.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()
    conn.close()


def dblog_insertrepulsor(jobid, parentjobid,iteration,individual,prevval,fitval):
    from commonfunctions import parseRPN
    conn = pymysql.connect(host=DBHOSTNAME, user=DBUSER, passwd=DBPASS, db=DBNAME)
    x = conn.cursor()
    xx=0
    individuallenght=len(individual)
    individualclean = ''
    for i in individual:
        individualclean = individualclean + i + ' '
    try:
        sql="INSERT INTO gp_log2.tbl_repulsors (parentrun,parent_runid,iteration,individual,prevval,fitval) VALUES (%s,'%s',%s,'%s',%s,%s);" % \
            (jobid,parentjobid,iteration,individualclean,prevval,fitval)
        x.execute(sql)
        conn.commit()
    except pymysql.Error as e:
        print(e)
        conn.rollback()
    conn.close()

