from ply.lex import lex

# define reserved word
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'then': 'THEN'
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
    # bracket
    'LPAREN', 'RPAREN',
    # conditional
    'IF', 'THEN', 'ELSE'
)

# Ignored characters
t_ignore = ' \t'

# Token matching rules are written as regexs
t_LAMBDA = r'\\'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
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

# Error handler for illegal characters
def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # 检查是不是关键词，如果不是，那么默认返回，NAME，
    t.type = reserved.get(t.value, 'ID')
    return t

lexer = lex()


# Build & Test
if __name__ == '__main__':
    lexer = lex()
    while True:
        s = input(">>>")
        lexer.input(s)

        for tok in lexer:
            if not tok:
                break
            print(tok)
