from ply.lex import lex

# define reserved word
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN',
    'rec' : 'REC'
}

# All tokens must be named in advance.
tokens = (
    # lambda
    "LAMBDA",
    # constants
    'NAT', 'ID',
    # binary operator
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    # conparison
    'LT', 'LE', 'GT', 'GE', 'EQ', 'NEQ',
    # conditional
    'IF', 'THEN', 'ELSE',
    # recursive function
    'REC'
)

# Ignored characters
t_ignore = ' \t'

# literals
literals = ['(', ')', '.']

# Token matching rules are written as regexs
t_LAMBDA = r'\\'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_LE = r'<='
t_LT = r'<'
t_GE = r'>='
t_GT = r'>'
t_EQ = r'=='
t_NEQ = r'!='

# A function can be used if there is an associated action.
# Write the matching regex in the docstring.
def t_NAT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # 检查是不是关键词，如果不是，那么默认返回，NAME，
    t.type = reserved.get(t.value, 'ID')
    return t


# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)
lexer = lex()


# Build & Test
if __name__ == '__main__':
    lexer = lex()
    while True:
        s = input(">>>")
        lexer.input(s)

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
