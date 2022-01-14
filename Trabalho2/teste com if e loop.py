import ply.lex as lex
from ply import yacc
import sys

reserved = {
    #Tipos
    "INT" : "INT",
    "LIST" : "LISTA",
    #Basic progaming shit
    "is" : "IGUAL",
    "IF" : "IF",
    "THEN" : "THEN",
    "IFNOT" : "ELSE",
    "WHILE" : "WHILE",
    "DO" : "DO",
    "FOR" : "FOR",
    #Operações mat
    "SUM" : "PLUS",
    "SUB" : "MINUS",
    "MULT" : "MUL",
    "DIV" : "DIV",
    #Operações logicas
    "EQ" : "EQ",
    "BIG" : "BIG",
    "BIGEQ" : "BIGEQ",
    "SAMALL" : "SMALL",
    "SAMALLEQ" : "SMALLEQ",
    "AND" : "AND",
    "OR" : "OR"
    }


tokens = ["NINT", "ID", "NEWLINE", "VIRG"] + list(reserved.values())

literal = ["(", ")"]

t_VIRG = r','

t_NEWLINE = r';'

# spaces and tabs serão ignorados
t_ignore  =  " \t \n"

# Criar floast e inteiros
#def t_NFLOAT(t):
#    r"\d+\.\d+"
#    t.value = float(t.value)
#    return t
def t_NINT(t):
    r"-?\d+"
    t.value = int(t.value)
    return t

def t_ID(t):
    r"[A-z]+"
    t.type = reserved.get(t.value, "ID")
    return t

def t_COMMENT(t):
    r"(\"|').*(\"|')"
    pass
    # No return, ignorar os comentaários

def t_error(t):
    print(f"keyword not found: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()


#parsing
precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'MUL', 'DIV' ),
    ( 'nonassoc', 'UMINUS' )
)


def p_start(p): #permite chegar aos restantes simbolos
    '''start : expr
                | exprl
                | operation
                | if_then
                | if_ifnot
                | while
                | for
                | list
                | decl
                '''
    p[0] = p[1]

def p_decl(p):
    '''decl : ID IGUAL decl_type '''
    p[0] = p[3]

def p_decl_type(p):
    '''decl_type : LISTA
                    | NINT
                    '''
    p[0] = p[1]

def p_expression_ariop(p): #exprm?
    '''expr :  expr PLUS expr
                  | expr MINUS expr
                  | expr MUL expr
                  | expr DIV expr'''
    if p[2] == 'SUM'  : p[0] = p[1] + p[3]
    elif p[2] == 'SUB': p[0] = p[1] - p[3]
    elif p[2] == 'MULT': p[0] = p[1] * p[3]
    elif p[2] == 'DIV': p[0] = p[1] / p[3]

def p_expr2uminus( p ) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = - p[2]
    
def p_expr2NUM( p ) :
    'expr : NINT'
    p[0] = p[1]


def p_expression_logop(t): #exprl
    '''exprl : expr BIG expr
                  | expr SMALL expr
                  | expr BIGEQ expr
                  | expr SMALLEQ expr
                  | expr EQ expr
                  | expr AND expr
                  | expr OR expr
                  '''
    if t[2] == 'BIG'  : t[0] = t[1] > t[3]
    elif t[2] == 'SMALL': t[0] = t[1] < t[3]
    elif t[2] == 'BIGEQ': t[0] = t[1] >= t[3]
    elif t[2] == 'SMALLEQ': t[0] = t[1] <= t[3]
    elif t[2] == 'EQ': t[0] = t[1] = t[3]
    elif t[2] == 'AND': t[0] = t[1] and t[3]
    elif t[2] == 'OR': t[0] = t[1] or t[3]


#####################################################################

def p_operation(p):
    '''operation : exprl
                    | expr
                    | NINT
                    '''
    p[0] = p[1]

def p_operation_def(p):
    '''operations : operation NEWLINE operations
                    | operation
                    '''
    p[0] = p[3]



'''
def p_operations_newline(p):
    "operations : operations NEWLINE operation"
    p[0] = p[1] + p[3]
    
'''

def p_IF_IFNOT(t):
    "if_ifnot : IF exprl THEN operations ELSE operations"
    if t[2]==True: t[0] = t[4]
    else: t[0] = t[6]

def p_IF(t):
    "if_then : IF exprl THEN operations"
    if t[2]==True: t[0] = t[4]

def p_while(t):
    "while : WHILE exprl DO operations"
    if t[2]==True: t[0] = t[4]

def p_for(t):
    "for : FOR exprl DO operations"
    if t[2]==True: t[0] = t[4]


def p_list(p):
    "list : ID IGUAL LISTA list_nint "
    p[0] = p[3]

def p_list_nint(p):
    '''list_nint : NINT
                    | NINT VIRG list_nint
                    '''
    p[0] = p[1]

###########################################################################



def p_error(p):
    parser.success = False
    print('Syntax error!')


###inicio do parsing
parser = yacc.yacc()

for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)
    if parser.success:
       print(parser.parse(linha))
       