from lexer import tokens
from ply import yacc
import sys

precedence = (
    ( 'left', 'PLUS' ),
    ( 'left', 'MUL', 'DIV' )
)

out_file = open("out.vm", "w+")
out_file.write("START\n")

def p_start(p): #permite chegar aos restantes simbolos
    '''start : expr
                | exprl
                | operation
                | if_then
                | if_ifnot
                | for
                | decl
                '''
    p[0] = p[1]
    out_file.write(str(p[0]))

def p_op_User(p):
    '''
    operation : INPUT
                | PRINT
    '''
    p[0] = p[1]

def p_INPUT(p):
    "INPUT : Input LP ID RP"
    #if p[3] in p.parser.registers:
    print(p.parser.registers[p[3]])
    p[0] = "READ\n" + "STOREG " + str(p.parser.registers[p[3]][0]) + "\nPUSHG " \
        +str(p.parser.registers[p[3]][0])+ "\nATOI" + "\nSTOREG " \
        + str(p.parser.registers[p[3]][0]) + "\n"

def p_PRINT(p):
    "PRINT : Write LP ID RP"
    p[0] = "PUSHG "+ str(p.parser.registers[p[3]][0]) + "\nWRITEI\n"


def p_decl_int(p):
    '''decl : ID IGUAL INT NINT '''
    p.parser.registers[p[1]] = (p.parser.gp, 'int', 1)
    p[0] = f'PUSHI {p[4]}\n'
    p.parser.gp += 1


def p_decl_list(p):
    "decl : ID IGUAL LISTA list_nint"
    #p.parser.arrp = -p.parser.gp
    p[0] = "PUSHN " + str(p.parser.arrp) + "\n" + p[4] + "\n"

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
    "decl : ID IGUAL INT strint"
    p[0] = p[4]


def p_declaracao(p):
    'declaracao : NEW vars'
    p[0] = ''
    for var in p[2]:
        p.parser.registers[var] = (p.parser.gp, 'int', 1)
        p[0] += f'pushi 0\n'
        p.parser.gp += 1
'''


def p_expression_op_mat(t):
    '''expr : expr PLUS expr
                  | expr MINUS expr
                  | expr MUL expr
                  | expr DIV expr
                  '''
    if t[2] == 'SUM':
        t[0] = t[1] + t[3] + "ADD\n" # t[0] = t[1] + t[3]
    elif t[2] == 'SUB':
        t[0] = t[1] + t[3] + "SUB\n" # t[0] = t[1] - t[3]
    elif t[2] == 'MULT':
        t[0] = t[1] + t[3] + "MUL\n" # t[0] = t[1] / t[3]
    elif t[2] == 'DIV':
        if t[3] == 0:
            print("Can't divide by 0")
            raise ZeroDivisionError('integer division by 0')  # maybe mudar isto para nao dar erro mas so passar mensagem?
        t[0] = t[1] + t[3] + "DIV\n" # p[0] = p[1] + p[3] + 'div\n'


def p_expr2NUM_nint( p ) :
    'expr : NINT'
    p[0] = "PUSHI " + str(p[1]) + "\n" # p[0] = p[1]


def p_expr2NUM_var( p ) :
    'expr : ID'
    p[0] = p[1]
    if p[1] in p.parser.registers:
        p[0] = "PUSHG " + p[1] # p[0] = p[1]

    #ver se esta no p.parser.registos
    #PUSHG


def p_exp2goup(p):
    #'exprg : LP exprm RP'
    'expr : LP expr RP'
    p[0] = p[2]

def p_expression_logop(t): #exprl
    '''exprl : expr BIG expr
                  | expr SMALL expr
                  | expr BIGEQ expr
                  | expr SMALLEQ expr
                  | expr EQ expr
                  | exprl AND exprl
                  | exprl OR exprl
                  '''
    if t[2] == 'BIG'  : t[0] = t[1] + t[3] + "SUP\n" #int(t[1] > t[3])
    elif t[2] == 'SMALL': t[0] = t[1] + t[3] + "INF\n" #int(t[1] < t[3])
    elif t[2] == 'BIGEQ': t[0] = t[1] + t[3] + "SUPEQ\n" #int(t[1] >= t[3])
    elif t[2] == 'SMALLEQ': t[0] = t[1] + t[3] + "INFEQ\n" #int(t[1] <= t[3])
    elif t[2] == 'EQ': t[0] = t[1] + t[3] + "EQUAL\n" #int(t[1] == t[3])
    elif t[2] == 'AND': t[0] = t[1] + t[3] + "MUL\n" #int(t[1] and t[3])
    elif t[2] == 'OR': t[0] = t[1] + "\nNOT\n" + t[3] + "\nNOT\nMUL\n NOT\n" # int(t[1] or t[3])

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

'''
def p_while(t):
    "while : WHILE exprl DO operations"
    if t[2]==True: t[0] = t[4]
'''

def p_for(t):
    "for : FOR exprl DO operations"
    if t[2]==True: t[0] = t[4]


def p_list_nint(p):
    "list_nint : NINT"
    p.parser.arrp = p.parser.gp
    p[0] = "PUSHI " + str(p[1]) + "\n" + "STOREG " + str(p.parser.arrp) 
    p.parser.arrp += 1    

def p_list_tailList(p):
    "list_nint : list_nint VIRG NINT"
    p[0] =  p[1] + "\n" + "PUSHI " + str(p[3]) + "\n" + "STOREG " + str(p.parser.arrp)
    p.parser.arrp += 1 
###########################################################################



def p_error(p):
    parser.success = False
    print('Syntax error!')


###inicio do parsing
parser = yacc.yacc()
parser.registers = {}
parser.gp = 0
parser.arrp = 0

user_input = input()
while user_input != "":
    result = parser.parse(user_input)
    user_input = input()

out_file.write("STOP")
out_file.close()