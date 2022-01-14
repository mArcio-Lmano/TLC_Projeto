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
    "WHILE" : "WHILE",
    "DO" : "DO",
    "FOR", "FOR",
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

t_NEWLINE = ";"

t_NVIRG = ","

# spaces and tabs seráo ignorados
t_ignore = " \t\n"

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

for line in sys.stdin:
    lexer.input(line)
    tok = lexer.token()
    while tok:
        print(tok)
        tok = lexer.token()   
