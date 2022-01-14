from lexer import tokens
from ply import yacc
import sys

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
                | decl
                '''
    p[0] = p[1]



def p_decl(p):
    '''decl : ID IGUAL INT NINT '''
    p.parser.registers[p[1]] = (p.parser.gp, 'int', 1)
    p[0] = f'pushi {p[4]}\n'
    p.parser.gp += 1

##FALTA FAZER PARA O TYPE LISTA



    '''  
registos = {}

registos_count = 0

    global registos
    global registos_count
    if p[1] not in registos:
        print(p[4])
        p[0] = 'pushi ' + str(p[4]) + '\n'
        registos[p[1]] = registos_count
        registos_count += 1


    
def p_decl_int(p):
    "decl : ID IGUAL INT NINT"
    p[0] = p[4]

def p_decl_list(p):
    "decl : ID IGUAL LISTA list_nint"
    p[0] = p[4]

def p_declaracao(p):
    'declaracao : NEW vars'
    p[0] = ''
    for var in p[2]:
        p.parser.registers[var] = (p.parser.gp, 'int', 1)
        p[0] += f'pushi 0\n'
        p.parser.gp += 1
'''

def p_expression_ariop(p): #exprm?
    '''expr :  expr PLUS expr
                  | expr MINUS expr
                  | expr MUL expr
                  | expr DIV expr'''
    if p[2] == 'SUM'  : p[0] = p[1] + p[3]
    elif p[2] == 'SUB': p[0] = p[1] - p[3]
    elif p[2] == 'MULT': p[0] = p[1] * p[3]
    elif p[2] == 'DIV': p[0] = p[1] / p[3]

#fazer expressoes grandes com parenteses

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
                  | exprl AND exprl
                  | exprl OR exprl
                  '''
    if t[2] == 'BIG'  : t[0] = int(t[1] > t[3])
    elif t[2] == 'SMALL': t[0] = int(t[1] < t[3])
    elif t[2] == 'BIGEQ': t[0] = int(t[1] >= t[3])
    elif t[2] == 'SMALLEQ': t[0] = int(t[1] <= t[3])
    elif t[2] == 'EQ': t[0] = int(t[1] == t[3])
    elif t[2] == 'AND': t[0] = int(t[1] and t[3])
    elif t[2] == 'OR': t[0] = int(t[1] or t[3])

#falta o NOT?
#o EQ tambem serve para exprl?

# o int() é para o if dar 1 ou 0 porque só assim funciona no assembly


#####################################################################

def p_operation(p):
    '''operation : exprl
                    | expr
                    | NINT
                    '''
    p[0] = p[1]

def p_operation_def(p):
    '''operations : operation NEWLINE operations
                    '''
    p[0] = str(p[1]) + str(p[3])


def p_operations_newline(p):
    "operations : operation"
    p[0] = p[1]




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
parser.registers = {}
parser.gp = 0


for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)
    if parser.success:
       print(parser.parse(linha))
       