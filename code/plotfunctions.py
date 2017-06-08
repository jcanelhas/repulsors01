"""
##########################################################################
####                                                                  ####
####                    Plotting                                      ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""

import matplotlib.pyplot as plt
from commonfunctions import parseRPN


def saveplotregressionresults(formula, fittable, iternum, runid):

    #todo reparar o graphsave
    from random import randint
    x=list()
    x[:]=[]
    y1=list()
    y1[:]=[]
    y2=list()
    y2[:]=[]
    xx=0
    nvars = len(fittable[0]) - 1  # numero de colunas de cada linha
    for line in fittable:
        xx=xx+1
        tmpfmla = formula[:]
        #for i in range(0, nvars):
        #    tmpfmla = [line[i] if n == 'x' + str(i) else n for n in tmpfm
        # la]
        for n in range(0,len(tmpfmla)):
            if tmpfmla[n][0]=='x':
                value=line[int(tmpfmla[n][1:])]
               # print (value)
                tmpfmla[n]=str(value)
                #print(tmpfmla)

        tmpfmla1 = parseRPN(tmpfmla)
        tmpfmla2 = line[len(line)-1]
        y1.append(tmpfmla1)# parse_rpn([i if n == 'x' else n for n in target_formula])
        y2.append(tmpfmla2)
        #x.append(tmpfmla2)# fitness=fitness+sqrt((tmpfmla2-tmpfmla1)**2)
        x.append(xx)  # fitness=fitness+sqrt((tmpfmla2-tmpfmla1)**2)
    plt.clf()
    plt.plot(x, y1,x, y2)
    plt.savefig(str(runid) + '/plots/' + str(iternum) + 'FINAL.png')

