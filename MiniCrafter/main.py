from lexer import tokenize
from Parser import Parser
from Compiler import Compiler
from vm import VM

code = """
"""

tokens = tokenize(code)
ast = Parser(tokens).parse()

compiler = Compiler()
bytecode = compiler.compile(ast)

print("BYTECODE:")
for i, instr in enumerate(bytecode):
    print(i, instr)

print("\nOUTPUT:")
vm = VM()
vm.run(bytecode)