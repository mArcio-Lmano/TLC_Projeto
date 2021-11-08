import re
from re_TLC import *

DIR = r"processos.txt"

def main():
    print("Exercício 4 do projeto\n")
    
    json_info = {}
    line = 1
    while len(json_info) < 20:
        reg = match_line(line)
        print(reg)
        if reg != None:
            json_info[str(reg["idd"])] = reg
        
        line += 1

    creat_jSon (json_info)

if __name__ == "__main__":
    main()
