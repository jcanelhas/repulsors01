from random import random,randint,randint,uniform

from commonfunctions import getRandomOperator

def GeneratePopulation(popsize, progdepth, method, nvars, varratio):
    pop=list()
    components=list()
    pop[:]=[]

    if method is 'grow' or method is 'full':
        for i in range(0,popsize):
            tmp=generate_RPN_expr("",progdepth,method,nvars,varratio)
            tmp=tmp[0:len(tmp)-1]
            #components[:]=[]
            components = [''.join(i) for i in tmp.split(' ')]
            if len(components)==2:
                print('error generate init pop >>> 2')
            if len(components)==0:
                print('error generate init pop >>> 0')
            pop.append(components)
    elif method is 'rhah':
        #todo fix population size problem
        #dividir a populacao em degraus
        nsteps=int(popsize/progdepth)
        for i in range(0,progdepth):
            for k in range(0,nsteps):
                ##dois em dois
                if k%2==0:
                    tmp = generate_RPN_expr("", i, 'grow',nvars,varratio)
                else:
                    tmp = generate_RPN_expr("", i, 'full',nvars,varratio)

                tmp = tmp[0:len(tmp) - 1]
                # components[:]=[]
                components = [''.join(i) for i in tmp.split(' ')]
                if len(components) == 2:
                    print('error generate init pop >>> 2')
                if len(components) == 0:
                    print('error generate init pop >>> 0')
                pop.append(components)

    return pop


def generate_RPN_expr(prevtree,depth,growthtype,nvars,varratio):
    tmptree=""
    if growthtype=='full':
        if depth>0:
            if random()>=0.5 or prevtree=="":
                #cria subtree
                tmptree=str(generate_RPN_expr(tmptree,depth-1,growthtype,nvars,varratio)) + str(generate_RPN_expr(tmptree,depth-1,growthtype,nvars,varratio)) + str(getRandomOperator()) + " " + tmptree
            else:
                #assigna valor
                tmptree=(str(uniform(-5,5))) + " " + tmptree
        else:
            if random()>=varratio:
                tmptree=(str(uniform(-5,5))) + " " + tmptree
            else:
                tmptree=selectRandomVariable(nvars) + " " + tmptree
        #tmptree=tmptree[0:len(tmptree)-1]

    elif growthtype=='grow':
        if depth > 0:
            if random() >= 0.5 :
                # cria subtree
                #leftside
                tmptree = str(generate_RPN_expr(tmptree, depth - 1,growthtype,nvars,varratio)) + str(generate_RPN_expr(tmptree, depth - 1,growthtype,nvars,varratio)) + str(getRandomOperator()) + " " + tmptree
            else:
                # assigna valor
                if random() >= varratio:
                    tmptree = (str(uniform(-5,5))) + " " + tmptree
                else:
                    tmptree = selectRandomVariable(nvars) + " " + tmptree
        else:
            if random() >= varratio:
                tmptree = (str(uniform(-5,5))) + " " + tmptree
            else:
                tmptree = selectRandomVariable(nvars) + " " + tmptree
                # tmptree=tmptree[0:len(tmptree)-1]

    else:
        print ('EEEKKKKKKKKKKKK EL PROBLEMO !!!')
    return tmptree #"(" + tmptree + ")"

def selectRandomVariable(nvars):
    """Return random variable name between x0 and X_nvars"""
    #from random import randint,uniform
    return 'x'+str(randint(0,nvars-1))