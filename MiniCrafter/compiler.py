class Compiler:
    def __init__(self):
        self.code = []

    def compile(self, ast):
        self.code = []

        for stmt in ast:
            self.gen(stmt)

        return self.code

    def gen(self, stmt):

        # Integer declaration
        if stmt[0] == 'DECLARE':

            _, name, expr = stmt

            self.gen_expr(expr)

            self.code.append(('STORE', name))

        # String declaration
        elif stmt[0] == 'STRING_DECLARE':

            _, name, value = stmt

            self.code.append(('PUSH', value))
            self.code.append(('STORE', name))

        # Print statement
        elif stmt[0] == 'PRINT':

            self.gen_expr(stmt[1])

            self.code.append(('PRINT',))

        # If-Else statement
        elif stmt[0] == 'IF':

            _, cond, t_branch, f_branch = stmt

            # Generate condition
            self.gen_condition(cond)

            # Placeholder for false jump
            jump_false = len(self.code)

            self.code.append(('JUMP_IF_FALSE', None))

            # True branch
            self.gen(t_branch)

            if f_branch:

                # Placeholder for end jump
                jump_end = len(self.code)

                self.code.append(('JUMP', None))

                # Fix false jump target
                self.code[jump_false] = (
                    'JUMP_IF_FALSE',
                    len(self.code)
                )

                # False branch
                self.gen(f_branch)

                # Fix end jump target
                self.code[jump_end] = (
                    'JUMP',
                    len(self.code)
                )

            else:
                # No else branch
                self.code[jump_false] = (
                    'JUMP_IF_FALSE',
                    len(self.code)
                )

    def gen_expr(self, node):

        # Integer literal
        if isinstance(node, int):

            self.code.append(('PUSH', node))

        # String literal
        elif isinstance(node, str):

            self.code.append(('PUSH', node))

        # Variable or operation
        elif isinstance(node, tuple):

            # Variable
            if node[0] == 'VAR':

                self.code.append(('LOAD', node[1]))

            # Arithmetic operation
            else:

                self.gen_expr(node[1])
                self.gen_expr(node[2])

                self.code.append(('OP', node[0]))

    def gen_condition(self, cond):

        op, left, right = cond

        self.gen_expr(left)
        self.gen_expr(right)

        self.code.append(('CMP', op))