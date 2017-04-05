from quad_generator import Variable, Quadruple, QuadGenerator

quadruples = []
pc = 0

def readFile():
    cont = 0
    f = open('output.cob', 'r')
    for line in f:
        print(line),
        q = line[1:-2].split(',')
        quad = Quadruple(cont, q[0], q[1], q[2], q[3])
        cont += 1
        quadruples.append(quad)
    f.close()

readFile()

while quadruples[pc].op != 'end':
    quad = quadruples[pc]
    op = quad.op
    if op == 'print':
        print(quadruples[pc].left_operand)

    elif op == '=':
        pass
        #accede a memoria y establece un valor
    elif op == 'Goto':
        pc = quadruples[pc].res

    elif op == 'GotoF':
        dir = quad.left_operand 
        # if memory.getVal(dir) == 'false':
        #     pc = quad.res
    elif op == 'GotoV':
         dir = quad.left_operand 
        # if memory.getVal(dir) == 'true':
        #     pc = quad.res
    

    print quadruples[pc].printeame()
    pc += 1