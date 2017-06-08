"""
##########################################################################
####                                                                  ####
####                     save graphs                                  ####
####                                                                  ####
####        This will create a dot file to open with graphviz         ####
####                                                                  ####
##########################################################################
"""


from copy import deepcopy



def create_graph(expression, filename):
    stack = []
    f = open(filename, 'w')
    f.write('strict graph G {\n')
    components=list()
    components=deepcopy(expression)
    result=list()
    result[:]=[]

    for n,val in enumerate(components):
        components[n]=[n,val]

    stack = []
    for val in components:
        if val[1] in ['-', '+', '*', '/']:
            op1 = stack.pop()
            op2 = stack.pop()
            nop1 = 'node' + str(op1[0])
            nop2 = 'node' + str(op2[0])
            nval = 'node' + str(val[0])
            f.write(nval + '[label=\"' + str(val) + '\"]\n')
            f.write(nop1 + '[label=\"' + str(op1[1]) + '\"]\n')
            f.write(nop2 + '[label=\"' + str(op2[1]) + '\"]\n')
            f.write(nval + '--' + nop1 + '\n')
            f.write(nval + '--' + nop2 + '\n')
            stack.append(val)
        else:
            stack.append(val)
    f.write('}\n')
    f.close()
