from ply.yacc import yacc
from my_lexer import tokens
import Abstact_Syntax_Tree as AST

'''
E | F
  | E F
  | E + E | E - E | E * E | E / E | E % E
  | E < E | E <= E | E > E | E >= E | E == E | E != E
  | -E | +E
  | IF (E) THEN E ELSE E
F | ID
  | NAT
  | (E)
  | lambda ( ID . E )
  | rec ID . lambda ( ID . E )
'''

'''
terminal states:
V
NAT
lambda ( ID . E )
(V|NAT)*
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
)

def p_start(p):
    '''
    expr : factor
    '''
    p[0] = p[1]

def p_expr_ID(p):
    '''
    factor : ID
    '''
    p[0] = AST.Variable(p[1])


def p_expr_NAT(p):
    '''
    factor : NAT
    '''
    p[0] = int(p[1])


def p_expr_if(p):
    '''
    expr : IF '(' expr ')' THEN expr ELSE expr
    '''
    p[0] = AST.CondBranch(p[3],p[6],p[8])


def p_expr_paren(p):
    '''
    factor : '(' expr ')'
    '''
    p[0] = p[2]


def p_expr_function_app(p):
    '''
    expr : expr factor
    '''
    p[0] = AST.Application(p[1], p[2])


def p_expr_function_abs_normal(p):
    '''
    factor : LAMBDA '(' ID '.' expr ')'
    '''
    p[0] = AST.Abstraction(AST.Variable(p[3]), p[5])


def p_expr_function_abs_rec(p):
    '''
    factor : REC ID '.' LAMBDA '(' ID '.' expr ')'
    '''
    p[0] = AST.Recursive(AST.Variable(p[2]),AST.Variable(p[6]),p[8])


def p_expr_arith(p):
    '''
    expr : expr PLUS expr
          | expr MINUS expr
          | expr TIMES expr
          | expr DIVIDE expr
          | expr MOD expr
    '''
    if p[2] not in ('+','-','*','/','%'):
        print("error!")
        exit(0)
    elif p[2] == '/' and p[3] == 0:
        print("division by zero!")
        exit(0)
    elif p[2] == '%' and p[3] == 0:
        print("division by zero!")
        exit(0)
    else:
        p[0] = AST.BinOps(p[1],p[3],p[2])


def p_expr_comparisons(p):
    '''
    expr  : expr LT expr
          | expr LE expr
          | expr GT expr
          | expr GE expr
          | expr EQ expr
          | expr NEQ expr
    '''
    p[0] = AST.BinOps(p[1],p[3],p[2])


def p_expr_UMINUS(p):
    """expr : MINUS expr %prec UMINUS"""
    p[0] = AST.UniOps(p[2],'-')


def p_expr_UPLUS(p):
    """expr : PLUS expr %prec UPLUS"""
    p[0] = AST.UniOpsh(p[2],'+')


# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Syntax error in input!")

parser = yacc()

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
