import re
from re_TLC import *

DIR = r"processos.txt"


def main():
    print("Exercício 2 do projeto\n")
    nomesTotais = {}
    json_info = {}
    line = 0
    index = 1
    #while (line <= 1000):
    while (line <= 37889):
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

    for reg in json_info:
        for pessoa in json_info[reg]["pessoas"]:
            #print(json_info[reg]["pessoas"][pessoa]["nome"])
            nome = json_info[reg]["pessoas"][pessoa]["nome"]
            #print (cleanNames(nome))
            for nom in cleanNames(nome):
                nome_split = cleanNames(nome)[nom]

                if len(nome_split) > 0:
                        if str(nome_split) in nomesTotais:
                            nomesTotais[nome_split] = nomesTotais[nome_split] + 1
                        else:
                            nomesTotais[nome_split] = 1
    print(nomesTotais)

if __name__ == "__main__":
    main()
