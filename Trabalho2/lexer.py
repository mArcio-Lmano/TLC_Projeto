import ply.lex as lex
import sys

reserved = {
    #Tipos
    "INT" : "INT",
    "NINT" : "FLOAT",
    "LIST" : "LISTA",
    #Basic progaming shit
    "is" : "IGUAL",
    "IF" : "IF",
    "THEN" : "THEN",
    "IFNOT" : "ELSE",
    "WHILE" : "WHILE",
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


tokens = ["NINT","NFLOAT", "ID"] + list(reserved.values())

literal = ["of", "(", ")"]

# spaces and tabs seráo ignorados
t_ignore  =  r" \n\t"

# Criar floast e inteiros
def t_NFLOAT(t):
    r"\d+\.\d+"
    t.value = float(t.value)
    return t

def t_NINT(t):
    r"\d+"
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

for line in sys.stdin:
    lexer.input(line)
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()   
