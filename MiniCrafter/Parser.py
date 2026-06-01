from error import MiniSyntaxError


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # Get current token
    def current(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    # Consume token
    def eat(self, token_type):

        tok = self.current()

        if tok and tok[0] == token_type:
            self.pos += 1
            return tok

        raise MiniSyntaxError(
            f"Syntax Error: Expected {token_type}, got {tok}"
        )

    # Parse full program
    def parse(self):

        statements = []

        while self.current():
            statements.append(self.statement())

        return statements

    # Parse statement
    def statement(self):

        tok = self.current()

        if tok is None:
            raise MiniSyntaxError(
                "Syntax Error: Unexpected end of input"
            )

        # Integer declaration
        if tok[0] == 'INT':
            return self.declaration()

        # String declaration
        elif tok[0] == 'STRING_TYPE':
            return self.string_declaration()

        # Print statement
        elif tok[0] == 'PRINT':
            return self.print_stmt()

        # If statement
        elif tok[0] == 'IF':
            return self.if_stmt()

        else:
            raise MiniSyntaxError(
                f"Invalid statement: {tok}"
            )

    # Integer declaration
    def declaration(self):

        self.eat('INT')

        name = self.eat('ID')[1]

        self.eat('ASSIGN')

        expr = self.expression()

        # Type checking
        if isinstance(expr, str):

            raise MiniSyntaxError(
                f"Type Error: Cannot assign string to int variable '{name}'"
            )

        return ('DECLARE', name, expr)

    # String declaration
    def string_declaration(self):

        self.eat('STRING_TYPE')

        name = self.eat('ID')[1]

        self.eat('ASSIGN')

        expr = self.expression()

        # Type checking
        if not isinstance(expr, str):

            raise MiniSyntaxError(
                f"Type Error: String variable '{name}' requires string value"
            )

        return ('STRING_DECLARE', name, expr)

    # Print statement
    def print_stmt(self):

        self.eat('PRINT')

        self.eat('LPAREN')

        expr = self.expression()

        self.eat('RPAREN')

        return ('PRINT', expr)

    # If statement
    def if_stmt(self):

        self.eat('IF')

        left = self.expression()

        op = self.eat('COMPARE')[1]

        right = self.expression()

        true_branch = self.statement()

        false_branch = None

        if self.current() and self.current()[0] == 'ELSE':

            self.eat('ELSE')

            false_branch = self.statement()

        return (
            'IF',
            (op, left, right),
            true_branch,
            false_branch
        )

    # Parse expressions
    def expression(self):

        left = self.term()

        while self.current() and self.current()[0] == 'OP':

            op = self.eat('OP')[1]

            right = self.term()

            left = (op, left, right)

        return left

    # Parse terms
    def term(self):

        tok = self.current()

        if tok is None:
            raise MiniSyntaxError(
                "Syntax Error: Unexpected end of input"
            )

        # Integer literal
        if tok[0] == 'NUMBER':

            return int(self.eat('NUMBER')[1])

        # String literal
        elif tok[0] == 'STRING_LITERAL':

            return self.eat('STRING_LITERAL')[1]

        # Variable
        elif tok[0] == 'ID':

            return ('VAR', self.eat('ID')[1])

        # Parenthesized expression
        elif tok[0] == 'LPAREN':

            self.eat('LPAREN')

            expr = self.expression()

            self.eat('RPAREN')

            return expr

        else:
            raise MiniSyntaxError(
                f"Invalid expression: {tok}"
            )