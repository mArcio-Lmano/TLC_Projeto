from lexer import tokens
from ply import yacc
import sys

precedence = (
    ( 'left', 'PLUS' ),
    ( 'left', 'MUL', 'DIV' )
)

out_file = open("out.vm", "w+")
out_file.write("START\n")

def p_start(p):
    "start : operations"
    p[0] = p[1]
    out_file.write(str(p[0]))

def p_atrib(p):
    "atrib : ID IGUAL expr"
    if p[1] in p.parser.registers:
        p[0] = p[3] + "STOREG " + str(p.parser.registers[p[1]][0]) + "\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

def p_INPUT(p):
    "IN : Input LP ID RP"
    if p[3] in p.parser.registers:
        p[0] = "READ\n" + "STOREG " + str(p.parser.registers[p[3]][0]) + "\nPUSHG " \
            +str(p.parser.registers[p[3]][0])+ "\nATOI" + "\nSTOREG " \
            + str(p.parser.registers[p[3]][0]) + "\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

def p_PRINT(p):
    "PRINT : Write LP TEXTO RP"
    p[0] = p[3]

def p_PRINT_ID(p):
    "TEXTO : ID"
    if p[1] in p.parser.registers:
        p[0] = "PUSHG "+ str(p.parser.registers[p[1]][0]) + "\nWRITEI\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

def p_PRINT_list_elem(p):
    "TEXTO : PRE ind PRD ID"
    if p[4] in p.parser.registers and p.parser.registers[p[4]][1] == "list":
        p[0] = "PUSHG "+ str(p.parser.registers[p[4]][0] + p[2]) + "\nWRITEI\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis ou a variável não é do tipo LIST")
        p_error(p)

def p_PRINT_TXT(p):
    "TEXTO : TEXT"
    p[0] = "PUSHS "+ str(p[1]) + "\nWRITES\n"

def p_decl_int_NINT(p):
    "decl : ID IGUAL INT NINTdec "
    if p[1] in p.parser.registers:
        p[0] = "PUSHI " + p[4] + "\n" + "STOREG " + str(p.parser.registers[p[1]][0]) + "\n"
    else:
        p.parser.registers[p[1]] = (p.parser.gp, 'int', 1)
        p[0] = f'PUSHI {p[4]}\n'
        p.parser.gp += 1

def p_decl_int(p):
    """NINTdec : NINT
                | """
    try:
        p[0] = str(p[1])
    except:
        p[0] = "0"

def p_decl_list(p):
    "decl : ID IGUAL LISTA list_nint"
    if p[1] not in p.parser.registers:
        p.parser.registers[p[1]] = (p.parser.gp, 'list', p.parser.arrp - p.parser.gp)
        p[0] = "PUSHN " + str(p.parser.arrp - p.parser.gp) + "\n" + p[4] + "\n"
        p.parser.gp += p.parser.arrp
    elif p.parser.registers[p[1]][1] == "list" and p.parser.arrp - p.parser.gp == p.parser.registers[p[1]][2]:
        p[0] = p[4] + "\n"
    else:
        print("ERRO: A variável não é do tipo LIST ou a nova lista não tem o tamanho da lista anterior da variável")
        p_error(p)

def p_list_nint(p):
    "list_nint : NINT"
    p.parser.arrp = p.parser.gp
    p[0] = "PUSHI " + str(p[1]) + "\n" + "STOREG " + str(p.parser.arrp) 
    p.parser.arrp += 1    

def p_list_tailList(p):
    "list_nint : list_nint VIRG NINT"
    p[0] =  p[1] + "\n" + "PUSHI " + str(p[3]) + "\n" + "STOREG " + str(p.parser.arrp)
    p.parser.arrp += 1 

def p_expression_op_mat(p):
    '''expr : expr PLUS expr
                  | expr MINUS expr
                  | expr MUL expr
                  | expr DIV expr
                  | expr MOD expr
                  '''
    if p[2] == 'SUM':
        p[0] = p[1] + p[3] + "ADD\n"
    elif p[2] == 'SUB':
        p[0] = p[1] + p[3] + "SUB\n"
    elif p[2] == 'MULT':
        p[0] = p[1] + p[3] + "MUL\n"
    elif p[2] == 'MOD':
        p[0] = p[1] + p[3] + "MOD\n"
    elif p[2] == 'DIV':
        p[0] = p[1] + p[3] + "DIV\n"

def p_expr2NUM_nint(p) :
    'expr : NINT'
    p[0] = "PUSHI " + str(p[1]) + "\n"

def p_expr_list(p):
    "expr : PRE indecl PRD ID "
    if p[4] in p.parser.registers and p.parser.registers[p[4]][1] == "list":
        p[0] = "PUSHGP\n" + "PUSHI " + str(p.parser.registers[p[4]][0]) + "\n" + "PADD\n" \
        + p[2] + "LOADN\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis ou a variável não é do tipo LIST")
        p_error(p)

def p_decl_list_elem(p):
    "atrib : PRE indecl PRD ID IGUAL expr"
    if p[4] in p.parser.registers:
        p[0] = "PUSHGP\n" + "PUSHI " + str(p.parser.registers[p[4]][0]) + "\n" + "PADD\n" \
        + p[2] + p[6] + "STOREN\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

def p_indecl_NINT(p):
    "indecl : NINT"
    p[0] = "PUSHI " + str(p[1]) + "\n"

def p_indecl_NINT(p):
    "indecl : ID"
    if p[1] in p.parser.registers:
        p[0] = "PUSHG " + str(p.parser.registers[p[1]][0]) + "\n"

def p_ind_list_NINT(p):
    "ind : NINT"
    p[0] = p[1]

def p_ind_list_ID(p):
    "ind : ID"
    if p[1] in p.parser.registers:
        p[0] = int(p.parser.registers[p[1]][3])
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

def p_expr2NUM_var(p) :
    "expr : ID"
    if p[1] in p.parser.registers:
        p[0] = "PUSHG " + str(p.parser.registers[p[1]][0]) + "\n"

def p_exp2goup(p):
    'expr : LP expr RP'
    p[0] = p[2]

def p_expression_logop(p):
    '''exprl : expr BIG expr
                  | expr SMALL expr
                  | expr BIGEQ expr
                  | expr SMALLEQ expr
                  | expr EQ expr
                  | exprl AND exprl
                  | exprl OR exprl
                  '''
    if p[2] == 'BIG' : p[0] = p[1] + p[3] + "SUP\n"
    elif p[2] == 'SMALL': p[0] = p[1] + p[3] + "INF\n"
    elif p[2] == 'BIGEQ': p[0] = p[1] + p[3] + "SUPEQ\n"
    elif p[2] == 'SMALLEQ': p[0] = p[1] + p[3] + "INFEQ\n"
    elif p[2] == 'EQ': p[0] = p[1] + p[3] + "EQUAL\n"
    elif p[2] == 'AND': p[0] = p[1] + p[3] + "MUL\n"
    elif p[2] == 'OR': p[0] = p[1] + "\nNOT\n" + p[3] + "\nNOT\nMUL\n NOT\n"

def p_operation_def(p):
    "operations : operations NEWLINE operation"
    p[0] = p[1] + p[3]

def p_operations_newline(p):
    "operations : operation"
    p[0] = p[1]

def p_op(p):
    """
    operation : IN
                | PRINT 
                | atrib 
                | exprl 
                | expr 
                | if_ifnot 
                | decl 
                | if_then 
                | for
    """
    p[0] = p[1]

def p_IF_IFNOT(p):
    "if_ifnot : IF exprl THEN operations ELSE operations"
    p[0] = p[2] + f"JZ IFNOT{p.parser.count_if}\n" + p[4] \
    + f"JUMP ENDIF{p.parser.count_if}\nIFNOT{p.parser.count_if}:\n" + p[6] \
    + f"ENDIF{p.parser.count_if}:\n"
    p.parser.count_if += 1

def p_IF(p):
    "if_then : IF exprl THEN operations"
    p[0] = p[2] + f"JZ ENDIF{p.parser.count_if}\n" + p[4] \
    + f"ENDIF{p.parser.count_if}:\n"
    p.parser.count_if += 1

def p_for(p):
    "for : FOR exprl DO operations"
    p[0] = f"FOR{p.parser.count_for}:\n" + p[2] + f"JZ ENDFOR{p.parser.count_for}\n" \
    + p[4] + f"JUMP FOR{p.parser.count_for}\n" + f"ENDFOR{p.parser.count_for}:\n" 
    p.parser.count_for += 1

def p_error(p):
    if p == None:
        pass
    else:
        print(f'Syntax error!')
        parser.success = False


###inicio do parsing
parser = yacc.yacc()
parser.registers = {}
parser.gp = 0
parser.arrp = 0
parser.num_linhas = 0
parser.count_for = 0
parser.count_if = 0
user_input = input("Que ficheiro pretende ler? ")

parser.success = True



file = open(f"codes/code{user_input}.txt","r")
for linha in file:
    parser.num_linhas += 1
    result = parser.parse(linha)
    if not parser.success:
        print(f"Erro na linha {parser.num_linhas} :: {linha}")

if parser.success:
    print("Código compilado com sucesso")

file.close()
out_file.write("STOP")
out_file.close()