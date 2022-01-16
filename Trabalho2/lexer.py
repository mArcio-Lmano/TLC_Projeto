import ply.lex as lex
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
    "DO" : "DO",
    "FOR" : "FOR",
    "Input" : "Input",
    "Write" : "Write",
    #Operações mat
    "SUM" : "PLUS",
    "SUB" : "MINUS",
    "MULT" : "MUL",
    "DIV" : "DIV",
    "MOD" : "MOD",
    #Operações logicas
    "EQ" : "EQ",
    "BIG" : "BIG",
    "BIGEQ" : "BIGEQ",
    "SMALL" : "SMALL",
    "SMALLEQ" : "SMALLEQ",
    "AND" : "AND",
    "OR" : "OR"
    }


tokens = ["NINT", "ID", "NEWLINE", "VIRG","LP","RP", "TEXT", "PRD", "PRE"] + list(reserved.values())

t_NEWLINE = ";"
t_LP = r'\('
t_RP = r'\)'
t_VIRG = ","
t_TEXT = r"\"([^\"]+)\""
t_PRD = r"}"
t_PRE = r"{"

# spaces and tabs serão ignorados
t_ignore = " \t\n"

#números inteiros
def t_NINT(t):
    r"-?\d+"
    t.value = int(t.value)
    return t

#variáveis
def t_ID(t):
    r"[A-z]+"
    t.type = reserved.get(t.value, "ID")
    return t

#comentários
def t_COMMENT(t):
    r"(').*(')"
    pass
    # No return, ignorar os comentaários

def t_error(t):
    print(f"ERRO: Token não encontrada: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

#for line in sys.stdin:
#    lexer.input(line)
#    tok = lexer.token()
#    while tok:
#        print(tok)
#        tok = lexer.token()   
