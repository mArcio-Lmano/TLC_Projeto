from lexer import tokens
from ply import yacc
import sys

#precedência: ordem correta das operações matemáticas (multiplicação/divisão fazem-se antes de soma/subtração)
precedence = (
    ( 'left', 'PLUS' ),
    ( 'left', 'MUL', 'DIV' )
)

#ficheiro de extração do código assembly terá o nome out.vm
out_file = open("out.vm", "w+")
#programa assembly começa com START
out_file.write("START\n")

#esta função permite chegar à função operations
def p_start(p):
    "start : operations"
    p[0] = p[1]
    out_file.write(str(p[0]))

#associa uma variável previamente declarada a uma expressão
def p_atrib(p):
    "atrib : ID IGUAL expr"
    if p[1] in p.parser.registers:
        p[0] = p[3] + "STOREG " + str(p.parser.registers[p[1]][0]) + "\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

#função para o usuário poder escrever no programa, dar input a um valor da forma Input(valor)
def p_INPUT(p):
    "IN : Input LP ID RP"
    if p[3] in p.parser.registers:
        p[0] = "READ\n" + "STOREG " + str(p.parser.registers[p[3]][0]) + "\nPUSHG " \
            +str(p.parser.registers[p[3]][0])+ "\nATOI" + "\nSTOREG " \
            + str(p.parser.registers[p[3]][0]) + "\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

#Função que permite imprimir o texto que está dentro dela no terminal assembly, usa-se Write(texto)
def p_PRINT(p):
    "PRINT : Write LP TEXTO RP"
    p[0] = p[3]

#Função para imprimir uma variável ID
def p_PRINT_ID(p):
    "TEXTO : ID"
    if p[1] in p.parser.registers:
        p[0] = "PUSHG "+ str(p.parser.registers[p[1]][0]) + "\nWRITEI\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

#função para imprimir um elemento "ind" de uma lista "ID"
def p_PRINT_list_elem(p):
    "TEXTO : PRE ind PRD ID"
    if p[4] in p.parser.registers and p.parser.registers[p[4]][1] == "list":
        p[0] = "PUSHG "+ str(p.parser.registers[p[4]][0] + p[2]) + "\nWRITEI\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis ou a variável não é do tipo LIST")
        p_error(p)

#função para imprimir uma string
def p_PRINT_TXT(p):
    "TEXTO : TEXT"
    p[0] = "PUSHS "+ str(p[1]) + "\nWRITES\n"

#função para declarar uma variável com um número inteiro da forma "variável is INT número"
def p_decl_int_NINT(p):
    "decl : ID IGUAL INT NINTdec "
    if p[1] in p.parser.registers:
        p[0] = "PUSHI " + p[4] + "\n" + "STOREG " + str(p.parser.registers[p[1]][0]) + "\n"
    else:
        p.parser.registers[p[1]] = (p.parser.gp, 'int', 1)
        p[0] = f'PUSHI {p[4]}\n'
        p.parser.gp += 1

#permite que variável do tipo INT possa ser definida logo como um número ou só como o seu tipo
def p_decl_int(p):
    """NINTdec : NINT
                | """
    try:
        p[0] = str(p[1])
    except:
        p[0] = "0"

#função para declarar uma variável com uma lista da forma "variável is LIST lista"
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

#elementos da lista (list_nint) são números inteiros (NINT)
def p_list_nint(p):
    "list_nint : NINT"
    p.parser.arrp = p.parser.gp
    p[0] = "PUSHI " + str(p[1]) + "\n" + "STOREG " + str(p.parser.arrp) 
    p.parser.arrp += 1    

#definição de uma lista: números inteiros separados por vírgulas
def p_list_tailList(p):
    "list_nint : list_nint VIRG NINT"
    p[0] =  p[1] + "\n" + "PUSHI " + str(p[3]) + "\n" + "STOREG " + str(p.parser.arrp)
    p.parser.arrp += 1 

#função que exprime as operações matemáticas soma, subtração, multiplicação, divisão e mod em números inteiros ou grupos
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

#uma expressão pode ser um número inteiro
def p_expr2NUM_nint(p) :
    'expr : NINT'
    p[0] = "PUSHI " + str(p[1]) + "\n"

#uma expressão pode ser um elemento de uma lista, da forma "{índice do elemento}lista"
def p_expr_list(p):
    "expr : PRE indecl PRD ID "
    if p[4] in p.parser.registers and p.parser.registers[p[4]][1] == "list":
        p[0] = "PUSHGP\n" + "PUSHI " + str(p.parser.registers[p[4]][0]) + "\n" + "PADD\n" \
        + p[2] + "LOADN\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis ou a variável não é do tipo LIST")
        p_error(p)

#pode ser atribuído a um elemento da lista uma expressão, da forma "{índice do elemento}lista is expressão"
def p_decl_list_elem(p):
    "atrib : PRE indecl PRD ID IGUAL expr"
    if p[4] in p.parser.registers and p.parser.registers[p[4]][1] == "list":
        p[0] = "PUSHGP\n" + "PUSHI " + str(p.parser.registers[p[4]][0]) + "\n" + "PADD\n" \
        + p[2] + p[6] + "STOREN\n"
    else:
        print("ERRO: A variável não se encontra na lista de variáveis ou a variável não é do tipo LIST")
        p_error(p)

#um índice pode ser declarado como um número inteiro
def p_indecl_NINT(p):
    "indecl : NINT"
    p[0] = "PUSHI " + str(p[1]) + "\n"

#um índice pode ser declarado como uma variável com um número inteiro associado a ela
def p_indecl_ID(p):
    "indecl : ID"
    if p[1] in p.parser.registers:
        p[0] = "PUSHG " + str(p.parser.registers[p[1]][0]) + "\n"

#um índice pode ser um número inteiro
def p_ind_list_NINT(p):
    "ind : NINT"
    p[0] = p[1]

#um índice pode ser uma variável com um número inteiro associado a ela
def p_ind_list_ID(p):
    "ind : ID"
    if p[1] in p.parser.registers:
        p[0] = int(p.parser.registers[p[1]][3])
    else:
        print("ERRO: A variável não se encontra na lista de variáveis")
        p_error(p)

#uma expressão pode ser uma variável
def p_expr2NUM_var(p) :
    "expr : ID"
    if p[1] in p.parser.registers:
        p[0] = "PUSHG " + str(p.parser.registers[p[1]][0]) + "\n"

#uma expressão pode ser um grupo: esta função serve para fazer contas com parêntesis da  forma (expressão)
def p_exp2goup(p):
    'expr : LP expr RP'
    p[0] = p[2]

#função que define as operações lógicas:
#Para operações matemáticas: BIG (maior que), SMALL (menor que), BIGEQ (maior ou igual), SMALLEQ (menor ou igual), EQ (igual)
#Para outras expressões lógicas: AND ("e"), OR ("ou")
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

#estrutura "operations" serve para se poderem executar mais que uma operação no mesmo if/for
#esta funciona com o caractere NEWLINE=";", da forma "operação1 ; operação2 ; operação3"
def p_operation_def(p):
    "operations : operations NEWLINE operation"
    p[0] = p[1] + p[3]

def p_operations_newline(p):
    "operations : operation"
    p[0] = p[1]

#uma operação pode ser um índice(IN), um print(PRINT), uma atribuição(atrib), uma expressão lógica(exprl),
#uma expressão matemática(expr), um if(if_then), um if...else(if_ifnot), uma declaração(decl), ou um ciclo for(for)
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

#definição de um if...else da forma "IF expresão lógica THEN operações IFNOT operações"
def p_IF_IFNOT(p):
    "if_ifnot : IF exprl THEN operations ELSE operations"
    p[0] = p[2] + f"JZ IFNOT{p.parser.count_if}\n" + p[4] \
    + f"JUMP ENDIF{p.parser.count_if}\nIFNOT{p.parser.count_if}:\n" + p[6] \
    + f"ENDIF{p.parser.count_if}:\n"
    p.parser.count_if += 1

#definição de um if da forma "IF expressão lógica THEN operações"
def p_IF(p):
    "if_then : IF exprl THEN operations"
    p[0] = p[2] + f"JZ ENDIF{p.parser.count_if}\n" + p[4] \
    + f"ENDIF{p.parser.count_if}:\n"
    p.parser.count_if += 1

#definição de um ciclo for da forma "FOR expressão lógica DO operações"
def p_for(p):
    "for : FOR exprl DO operations"
    p[0] = f"FOR{p.parser.count_for}:\n" + p[2] + f"JZ ENDFOR{p.parser.count_for}\n" \
    + p[4] + f"JUMP FOR{p.parser.count_for}\n" + f"ENDFOR{p.parser.count_for}:\n" 
    p.parser.count_for += 1

#erro de sintaxe
def p_error(p):
    if p == None:
        pass
    else:
        print(f'Syntax error!')
        parser.success = False


#início do parsing
parser = yacc.yacc()

#iniciação de variáveis/dicionários a usar
parser.registers = {}
parser.gp = 0
parser.arrp = 0
parser.num_linhas = 0
parser.count_for = 0
parser.count_if = 0
parser.success = True

#utilizador começa por dar input ao ficheiro que pretende ler
#o ficheiro estará na pasta "codes" e o input corresponderá a codeINPUT
#por exemplo para ler o ficheiro "code1" terá de se dar input a "1"
user_input = input("Que ficheiro pretende ler? ")

file = open(f"codes/code{user_input}.txt","r")

#leitura do ficheiro e se houver um insucesso do parser declarar em que linha do ficheiro de texto ocorreu o erro
for linha in file:
    parser.num_linhas += 1
    result = parser.parse(linha)
    if not parser.success:
        print(f"Erro na linha {parser.num_linhas} :: {linha}")

#se for bem sucedido imprimirá esta mensagem
if parser.success:
    print("Código compilado com sucesso")

#fecha o ficheiro de texto a analisar
file.close()
#"STOP" termina o código assembly
out_file.write("STOP")
#fecha o ficheiro "out.vm" de output do código assembly
out_file.close()