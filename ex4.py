import re
from re_TLC import *

DIR = r"processos.txt"

def main():
    print("Exercício 4 do projeto\n")
    
    json_info = {}
    line = 0
    index = 1
    while len(json_info) < 300:
        reg = match_line(line)

        if reg != None:
            idd = reg["idd"]

            while reg["idd"] in json_info:

                if reg["pessoas"] == json_info[idd]["pessoas"] and reg["data"] == json_info[idd]["data"]:
                    print("Registo duplicado")
                    break
                else:        
                    idd += f".{index}"
                    reg["idd"] = idd

            else:
                json_info[idd] = reg
                
        line += 1

    creat_jSon (json_info)

if __name__ == "__main__":
    main()
