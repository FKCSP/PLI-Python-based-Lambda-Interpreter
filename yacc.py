from ply.yacc import yacc
from lexer import tokens
# import ast as AST

'''
E | ID
  | NAT
  | IF (E) THEN E ELSE E
  | (E)
  | lambda ID . expr '(' expr ')'
  | lambda (ID.E)
  | rec ID . lambda ID . E
  | E + E | E - E | E * E | E / E | E % E
  | E < E | E <= E | E > E | E >= E | E == E | E != E
  | -E | +E



F : lambda ID.E
'''

precedence = (
    # comparisons
    ('left', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NEQ'),
    # binary operator low
    ('left', 'PLUS', 'MINUS'),
    # binary operator high
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    # then
    ('left', 'THEN'),
    # paren
    ('left', 'ELSE'),
    # unary operator
    ('right', 'UPLUS', 'UMINUS'),
    # parentheses
    ('left', '(', ')'),
    # lambda & recursive
    ('right', 'LAMBDA'),
    ('right', 'REC')
)


def p_expr_ID(p):
    '''
    expr : ID
    '''
    p[0] = p[1]


def p_expr_NAT(p):
    '''
    expr : NAT
    '''
    p[0] = p[1]


def p_expr_if(p):
    '''
    expr : IF '(' expr ')' THEN expr ELSE expr
    '''
    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[8]



def p_expr_paren(p):
    '''
    expr : '(' expr ')'
    '''
    p[0] = p[2]


def p_expr_function_app(p):
    '''
    expr : LAMBDA ID '.' expr '(' expr ')'
    '''
    pass


def p_expr_function_abs(p):
    '''
    expr : LAMBDA '('  ID '.' expr ')'
    '''
    pass


def p_expr_recursive(p):
    '''
    expr : REC ID '.' LAMBDA ID '.' expr
    '''
    pass


def p_expr_arith(p):
    '''
    expr : expr PLUS expr
          | expr MINUS expr
          | expr TIMES expr
          | expr DIVIDE expr
          | expr MOD expr
    '''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] + p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/' and p[3] != 0:
        p[0] = p[1] / p[3]
    elif p[2] == '%' and p[3] != 0:
        p[0] = p[1] % p[3]
    else:
        print("error!")
        exit(0)


def p_expr_comparisons(p):
    '''
    expr  : expr LT expr
          | expr LE expr
          | expr GT expr
          | expr GE expr
          | expr EQ expr
          | expr NEQ expr
    '''
    if p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    else:
        p[0] = p[1] != p[3]


def p_expr_UMINUS(p):
    """expr : MINUS expr %prec UMINUS"""
    p[0] = -p[2]


def p_expr_UPLUS(p):
    """expr : PLUS expr %prec UPLUS"""
    p[0] = p[2]


# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Syntax error in input!")



if __name__ == '__main__':
    # Build the parser
    parser = yacc()
    while True:
        try:
            s = input('>>>')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)
