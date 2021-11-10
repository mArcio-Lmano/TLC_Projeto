import re
from re_TLC import *

DIR = r"processos.txt"


def main():
    print("Exercício 3 do projeto\n")
    grausParentesco = {}
    json_info = {}
    line = 0
    index = 1
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
        print (reg)
        print(line)
        line += 1

    for reg in json_info:
        for pessoa in json_info[reg]["pessoas"]:
            #print(json_info[reg]["pessoas"][pessoa]["grau parentesco"])
            grau_parentesco = json_info[reg]["pessoas"][pessoa]["grau parentesco"]
            if len(grau_parentesco) > 0:
                if str(grau_parentesco) in grausParentesco:
                    grausParentesco[grau_parentesco] = grausParentesco[grau_parentesco] + 1
                else:
                    grausParentesco[grau_parentesco] = 1
    print(grausParentesco)


if __name__ == "__main__":
    main()
