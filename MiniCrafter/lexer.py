import re
from error import MiniLexicalError

TOKEN_SPECIFICATION = [

    ('STRING_LITERAL', r'"[^"]*"'),
    ('NUMBER',         r'\d+'),

    ('ID',             r'[a-zA-Z_]\w*'),

    ('ASSIGN',         r'='),
    ('OP',             r'[+\-*/]'),
    ('COMPARE',        r'[><]'),

    ('LPAREN',         r'\('),
    ('RPAREN',         r'\)'),

    # Ignore spaces, tabs, carriage returns
    ('SKIP',           r'[ \t\r]+'),

    # New lines
    ('NEWLINE',        r'\n'),

    # Catch invalid characters
    ('MISMATCH',       r'.'),
]

KEYWORDS = {
    'int',
    'string',
    'print',
    'if',
    'else'
}


def tokenize(code):

    tokens = []

    tok_regex = '|'.join(
        f'(?P<{name}>{pattern})'
        for name, pattern in TOKEN_SPECIFICATION
    )

    for mo in re.finditer(tok_regex, code):

        kind = mo.lastgroup
        value = mo.group()

        # Number
        if kind == 'NUMBER':

            tokens.append(
                ('NUMBER', int(value))
            )

        # String literal
        elif kind == 'STRING_LITERAL':

            tokens.append(
                ('STRING_LITERAL', value[1:-1])
            )

        # Keywords
        elif kind == 'ID' and value in KEYWORDS:

            if value == 'string':
                tokens.append(('STRING_TYPE', value))

            else:
                tokens.append((value.upper(), value))

        # Variable names
        elif kind == 'ID':

            tokens.append(('ID', value))

        # Ignore spaces/newlines
        elif kind in ['SKIP', 'NEWLINE']:
            continue

        # Invalid character
        elif kind == 'MISMATCH':

            raise MiniLexicalError(
                f"Invalid character: {value}"
            )

        else:

            tokens.append((kind, value))

    return tokens