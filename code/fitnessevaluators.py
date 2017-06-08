"""
##########################################################################
####                                                                  ####
####                     evaluate fitnesses                           ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""



from commonfunctions import *
#     return fitness

def getfitness(formula,fittable,resultdic={},usedictionary=True,mode='rms',roundtointeger=False ):
    #modes
    #rms default, root mean square
    if (str(formula) in resultdic) and usedictionary:
        return resultdic[str(formula)]

    fitness = 0
    tmpfmla = list()
    tmpfmla[:] = []
    nvars = len(fittable[0])-1 #numero de colunas de cada linha

    for line in fittable:
        tmpfmla = formula[:]

        for n in range(0,len(tmpfmla)):
            if tmpfmla[n][0]=='x':
                value=line[int(tmpfmla[n][1:])]
                tmpfmla[n]=str(value)

        tmpfmla1 = parseRPN(tmpfmla,roundtointeger)
        tmpfmla2 = line[nvars]  # parse_rpn([i if n == 'x' else n for n in target_formula])

        try:
            fitness = fitness + (tmpfmla2 - tmpfmla1) ** 2
        except OverflowError as e:            #pay attention to float overflow
            fitness=100000
            print(e)
            print('fitness :'+str(fitness))
            print('tmpfmla1:' + str(tmpfmla1))
            print('tmpfmla2:' + str(tmpfmla2))
            quit()
    fitness = sqrt(fitness / len(fittable))

#    if roundtointeger==True:
#        fitness=round(fitness)


    resultdic[str(formula)] = fitness

    return fitness



def regressioncomparator(formula, fittable):
    fitness = 0
    tmpfmla = list()
    tmpfmla[:] = []
    output = list()
    output[:] = []
    nvars = len(fittable[0])-1 #numero de colunas de cada linha
    for line in fittable:
        tmpfmla = formula[:]
        for n in range(0,len(tmpfmla)):
            if tmpfmla[n][0]=='x':
                value=line[int(tmpfmla[n][1:])]
               # print (value)
                tmpfmla[n]=str(value)
                #print(tmpfmla)
        tmpfmla1 = parseRPN(tmpfmla)
        tmpfmla2 = line[nvars]  # parse_rpn([i if n == 'x' else n for n in target_formula])
        output.append([tmpfmla2,tmpfmla1])
    return output


def getregressionresult(formula,fittable):
    fitness = 0
    tmpfmla = list()
    tmpfmla[:] = []
    output = list()
    output[:] = []
    nvars = len(fittable[0])-1 #numero de colunas de cada linha
    for line in fittable:
        tmpfmla = formula[:]
        for n in range(0,len(tmpfmla)):
            if tmpfmla[n][0]=='x':
                value=line[int(tmpfmla[n][1:])]
               # print (value)
                tmpfmla[n]=str(value)
                #print(tmpfmla)
        tmpfmla1 = parseRPN(tmpfmla)
        output.append(tmpfmla1)
    return output


def saveresulttable(formula, fittable, iternum, runid):
    xx=0
    nvars = len(fittable[0]) - 1  # numero de colunas de cada linha
    outfile = open(str(runid) + '/resulttables/' + str(iternum) + '.txt','w')
    outfile.write("elem;result;target\n")
    for line in fittable:
        xx=xx+1
        tmpfmla = formula[:]
        for n in range(0,len(tmpfmla)):
            if tmpfmla[n][0]=='x':
                value=line[int(tmpfmla[n][1:])]
                tmpfmla[n]=str(value)
        tmpfmla1 = parseRPN(tmpfmla)
        tmpfmla2 = line[len(line)-1]
        outfile.write(str(xx) + ";" + str(tmpfmla1) + ";" + str(tmpfmla2) + "\n")
    outfile.close()