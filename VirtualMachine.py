from quad_generator import Variable, Quadruple, QuadGenerator



class VirtualMachine():
    def __init__(self):
        self.quadruples = []
        self.pc = 0

    def readFiles(self):
        cont = 0
        f = open('output.cob', 'r')
        for line in f:
            # print(line),
            q = line[1:-2].split(',')
            quad = Quadruple(cont, q[0], q[1], q[2], q[3])
            cont += 1
            self.quadruples.append(quad)
        f.close()
    
    def run(self):
        self.readFiles()

        while self.quadruples[self.pc].op != 'END':
            quad = self.quadruples[self.pc]
            
            op = quad.op
            if op == 'Print':
                print("{0}{1}").format(quad.left_operand, quad.right_operand[2:-1])
            #basic operations +, - , *, /
            elif op == '+':
                pass
            elif op == '-':
                pass
            elif op == '*':
                pass
            elif op == '/':
                pass
            elif op == '=':
                pass
                #accede a memoria y establece un valor
            #logic operations
            elif op == 'and':
                pass
            elif op == 'or':
                pass
            elif op == '>=':
                pass
            elif op == '<=':
                pass
            elif op == '==':
                pass
            elif op == '>':
                pass
            elif op == '<':
                pass
            # gotos
            elif op == 'Goto':
                self.pc = int(self.quadruples[self.pc].res)
                continue
            elif op == 'GotoF':
                dir = quad.left_operand
                # if memory.getVal(dir) == 'false':
                #     self.pc = quad.res
            elif op == 'GotoV':
                dir = quad.left_operand
                # if memory.getVal(dir) == 'true':
                #     self.pc = quad.res

            # print self.quadruples[self.pc].printeame()
            self.pc += 1

vm = VirtualMachine()
vm.run()