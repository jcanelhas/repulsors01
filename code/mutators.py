"""
##########################################################################
####                                                                  ####
####                     Mutation                                     ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""

from random import random, randint
import random
#import copy
from commonfunctions import getTreeDepth, traverse, getRandomOperator, validateRPN, checkRPN
from commonfunctions import isOperator
from generators import generate_RPN_expr

def Mutate(individual, maxtreedepth, mode, nvars, varratio):

    if len(individual)==0:
        print()

    overgrown = True
    while overgrown: # do while overgrown == True

        try:
            mutatepos = random.randint(0, len(individual) - 1)
        except ValueError:
            print("MUTATOR ERRADO")
            print(individual)
            print(mode)
            print(nvars)
            print(varratio)

        # output tree
        output = list()
        output[:] = []

        tmpind=list()
        tmpind[:]=[]


        #Subtree mutation replaces a randomly selected subtree with another randomly created subtree (Koza, 1992, page 106)
        #AKA standard mutation
        if mode=='subtree':
            tmpind = individual[:]
            subtree = traverse(tmpind, mutatepos)

            subtreedepth = getTreeDepth(subtree,'treedepth')-1


            #verificar se esolhemos um operador ou um nó terminal
            prevstep='subtree op'
            #gerar uma
            tmptreerpn=generate_RPN_expr('',subtreedepth,'full',nvars,varratio)
            tmptreerpn = tmptreerpn[0:len(tmptreerpn)-1]
            tmptree = [''.join(i) for i in tmptreerpn.split(' ')]

            i1p1 = tmpind[:len(tmpind) - len(subtree) - mutatepos]
            i1p2 = tmptree#subtree
            i1p3 = tmpind[len(i1p1) + len(subtree):]
            output = i1p1+i1p2+i1p3

            tmpind = output[:]
            #tmpind=copy.deepcopy(output)

        # Node replacement mutation (also known as point mutation) is similar to bit string mutation in that
        # it randomly changes a point in the individual. In linear GAs the change would be a bit flip.
        # In GP, instead, a node in the tree is randomly selected and randomly changed. To ensure the tree remains legal,
        #  the replacement node has the same number of arguments as the node it is replacing,
        #  e.g. (McKay, Willis, and Barton, 1995, page 488).
        elif mode=='point':
            tmpind = individual[:]
            if isOperator(tmpind[mutatepos]) == True:
                prevstep = 'point op'
                tmpind[mutatepos]=getRandomOperator()
            else:
                prevstep = 'point term'
                if random.random() >= 0.5:
                    tmpind[mutatepos] = str(random.randint(-5,5))
                else:
                    tmpind[mutatepos] = selectRandomVariable(nvars)
        else:
            print ("nunca aqui devia ter chegado")

        if getTreeDepth(tmpind,'treedepth') > maxtreedepth:
            overgrown=True
            print("!", end='')

        else:
            overgrown=False


    return tmpind



def selectRandomVariable(nvars):
    """Return random variable name between x0 and X_nvars"""
    #from random import randint
    return 'x'+str(randint(0,nvars-1))