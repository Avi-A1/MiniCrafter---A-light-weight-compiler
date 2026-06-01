from error import MiniRuntimeError

class VM:
    def __init__(self):
        self.stack = []
        self.vars = {}
        self.pc = 0

    def run(self, code):

        self.stack = []
        self.vars = {}
        self.pc = 0

        while self.pc < len(code):

            instr = code[self.pc]
            op = instr[0]

            if op == 'PUSH':
                self.stack.append(instr[1])

            elif op == 'LOAD':

                if instr[1] not in self.vars:
                    raise MiniRuntimeError(
                        f"Runtime Error: Undefined variable '{instr[1]}'"
                    )

                self.stack.append(
                    self.vars[instr[1]]
                )

            elif op == 'STORE':
                self.vars[instr[1]] = self.stack.pop()

            elif op == 'OP':

                b = self.stack.pop()
                a = self.stack.pop()

                if instr[1] == '+':
                    self.stack.append(a + b)

                elif instr[1] == '-':
                    self.stack.append(a - b)

                elif instr[1] == '*':
                    self.stack.append(a * b)

                elif instr[1] == '/':

                    if b == 0:
                        raise MiniRuntimeError(
                            "Runtime Error: Division by zero"
                        )

                    self.stack.append(a // b)

            elif op == 'CMP':

                b = self.stack.pop()
                a = self.stack.pop()

                if instr[1] == '>':
                    self.stack.append(a > b)

                elif instr[1] == '<':
                    self.stack.append(a < b)

            elif op == 'JUMP_IF_FALSE':

                if not self.stack.pop():
                    self.pc = instr[1]
                    continue

            elif op == 'JUMP':

                self.pc = instr[1]
                continue

            elif op == 'PRINT':
                print(self.stack.pop())

            self.pc += 1