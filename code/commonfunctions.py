"""
##########################################################################
####                                                                  ####
####                     Function used in several modules             ####
####                                                                  ####
####                                                                  ####
####                                                                  ####
##########################################################################
"""

from math import *
import operator
#import pytest

"""RPN PARSER"""

def parseRPN(expression,roundtointeger=False):
    """Parses and calculates the result of a RPN expression
        takes a list in the form of ['2','2','*']
        returns 4
    """""

    def safe_divide(darg1, darg2):
        ERROR_VALUE = 1.
        # ORIGINAL ___ Here we can penalize asymptotes with the var PENALIZE_ASYMPITOTES

        try:
            return darg1 / darg2
        except ZeroDivisionError:
            return ERROR_VALUE

    function_twoargs = {'*': operator.mul, '/': safe_divide, '+': operator.add, '-': operator.sub}
    function_onearg = {'sin': sin, 'cos': cos}
    stack = []
    for val in expression:
        result = None
        if val in function_twoargs:
            arg2 = stack.pop()
            arg1 = stack.pop()
            result = function_twoargs[val](arg1, arg2)
        elif val in function_onearg:
            arg = stack.pop()
            result = function_onearg[val](arg)
        else:
            result = float(val)
        stack.append(result)

    if roundtointeger == True:
        result=stack.pop()
        result=round(result)
    else:
        result=stack.pop()
    return result



def isOperator(expression):
    """Function that returns if the current symbol is a valid operator that can be processed by the
    fitness calculation function"""
    if expression in ['-', '+', '*', '/']:
        return True
    else:
        return False

def getRandomOperator():
    """function to return a random valid operator"""
    #todo, improve function
    from random import random
    tmprnd=random()
    if tmprnd < 0.25:
        return '+'
    elif tmprnd < 0.5:
        return '*'
    elif tmprnd < 0.75:
        return '-'
    else:
        return '/'

def getArity(operator):
    """Function that returns the arity of an operator"""
    if operator in ['-', '+', '*', '/', '**']:
        return 2
    elif operator in ['sin', 'cos']:
        return 1
    else:
        print ('Arity Error')
        quit()

def checkRPN(expression):
    """check if the rpn instruction has a valid format"""
    counter=0
    for val in expression:
        if isOperator(val):
            counter=counter-getArity(val)
        else:
            counter=counter+1

    if counter>1:
        print ('nonvalid rpn fn:check_rpn')
    return counter





def printAllSubTrees(individual):
    """returns all subtrees in a RPN Expression"""
    for i in range(len(individual)):
        print("#: {}, subtree= {}".format(i, traverse(individual, i)))

def traverse(inputexpr,start):
    components=list()
    components[:]=[]

    components=inputexpr[0:len(inputexpr)-start]
    components.reverse()

    pos=0
    result=list()
    result[:]=[]
    score=0
    if isOperator(components[pos]):
        result.append(components[pos])
        score=score+getArity(components[pos])
    else:
        result.append(components[pos])
        score=score -1
    pos=pos+1
    while score>0:
        if isOperator(components[pos]):
            result.append(components[pos])
            score = score + getArity(components[pos])-1
        else:
            result.append(components[pos])
            score = score - 1
        pos = pos + 1
    #print(components)
    result.reverse()
    return result


def getTreeDepth(expression,method):
    if method == 'treedepth':
        return getRPNdepth(expression)
    if method == 'stacksize':
        return getRPNStackdepth(expression)



def getRPNStackdepth(expression):
    #This fucntions calculates the depth of the stack needed
    tmpexp = expression
    maxstacksize = 0
    tmpfmla = [1 if n[0] == 'x' else n for n in tmpexp]
    try:
        stack = []
        for val in tmpfmla:
            if val in ['-', '+', '*', '/']:
                op1 = stack.pop()
                op2 = stack.pop()
                if val == '-': result = op2 - op1
                if val == '+': result = op2 + op1
                if val == '*': result = op2 * op1
                if val == '/':
                    if op1 == 0:
                        result = 1
                    else:
                        result = op2 / op1
                stack.append(result)

            else:
                stack.append(float(val))

            if len(stack) > maxstacksize:
                maxstacksize = len(stack)

        return abs(maxstacksize)
    except:
        print('error validate rpn>' + str(expression))
        return 0




def getRPNdepth(expression):
    stack = []
    for val in expression:
        if val in ['-', '+', '*', '/']:
            stack.append(max(stack.pop(),stack.pop())+1)
        else:
            stack.append(1)
        #print(str(stack));
    return stack.pop()


def validateRPN(expression):
    #old
    #todo upgrade this function
    tmpexp=expression
    tmpfmla = [1 if n == 'x' else n for n in tmpexp]
    try:
        stack = []
        for val in tmpfmla:
            if val in ['-', '+', '*', '/']:
                op1 = stack.pop()
                op2 = stack.pop()
                if val == '-': result = op2 - op1
                if val == '+': result = op2 + op1
                if val == '*': result = op2 * op1
                if val == '/':
                    if op1 == 0:
                        result = 1
                    else:
                        result = op2 / op1
                stack.append(result)
            elif val in ['sin', 'cos']:
                op1 = stack.pop()
                if val == 'sin': result = sin(op1)
                if val == 'cos': result = cos(op1)
                stack.append(result)
            else:
                stack.append(float(val))
        return True
    except:
        print('error validate rpn>' + str(expression))
        return False



def TreeSizer(expression):
    #old
    #todo upgrade this function
    treesize=0
    maxtreesize=treesize
    tmpexp=expression
    tmpfmla = [1 if n == 'x' else n for n in tmpexp]
    try:
        stack = []
        for val in tmpfmla:
            if val in ['-', '+', '*', '/']:
                treesize=treesize+1
                op1 = stack.pop()
                op2 = stack.pop()
                if val == '-': result = op2 - op1
                if val == '+': result = op2 + op1
                if val == '*': result = op2 * op1
                if val == '/':
                    if op1 == 0:
                        result = 1
                    else:
                        result = op2 / op1
                stack.append(result)
            elif val in ['sin', 'cos']:
                op1 = stack.pop()
                treesize=treesize+1
                if val == 'sin': result = sin(op1)
                if val == 'cos': result = cos(op1)
                stack.append(result)
            else:
                treesize=treesize-1
                stack.append(float(val))
            if treesize>maxtreesize:
                maxtreesize=treesize
        return treesize
    except:
        print('error validate rpn>' + str(expression))
        return -1