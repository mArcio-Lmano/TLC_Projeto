import re
from re_TLC import *

DIR = r"processos.txt"

nomesTotais = {}

def main():
    print("Exercício 3 do projeto\n")
    grausParentesco = {}
    json_info = {}
    line = 0
    index = 1
    while (line <= 30):
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
        #print (reg)
        #print(line)
        line += 1

    for reg in json_info:
        for pessoa in json_info[reg]["pessoas"]:
            #print(json_info[reg]["pessoas"][pessoa]["nome"])
            nome = json_info[reg]["pessoas"][pessoa]["nome"]
            for nome in cleanNames(nome):
                nome_split = nome = json_info[reg]["pessoas"][pessoa]["nome"][nome]
                if len(nome_split) > 0:
                        if str(nome_split) in nomesTotais:
                            nomesTotais[nome_split] = nomesTotais[nome_split] + 1
                        else:
                            nomesTotais[nome] = 1
    print(nomesTotais)



"""
def main_1():
    print("Exercício 3 do projeto\n")
    line_num = 0
    j_inf = {}
    r = r"([0-9]+)::([0-9]{4}-[0-9]{2}-[0-9]{2})::([A-z ,\.:0-9]+)"
    #while len(j_inf)<30:
    for a in open(DIR):
        line = readline(DIR, line_num)
        line_num += 1
        match = re.search(r, line)
        processo = {}

        if match:
            idd = match.group(1)
            data = match.group(2)
            pessoas = cleanPerson(match.group(3))

            while idd in j_inf:
                print("Erro o id já existe")

                if (pessoas == j_inf[idd]["pessoas"] and data == j_inf[idd]["data"]):
                    print("Registo duplicado")
                    processo["id"] = str(idd)
                    processo["data"] = str(data)
                    processo["pessoas"] = pessoas
                    break
                else:
                    print("Novo registo")
                    idd = idd + ".1"
                    processo["id"] = str(idd)
                    processo["data"] = str(data)
                    processo["pessoas"] = pessoas

            else:
                processo["id"] = str(idd)
                processo["data"] = str(data)
                processo["pessoas"] = pessoas

            j_inf[str(idd)] = processo
            print(processo)

    print(j_inf)

    for reg in j_inf:
        for pessoa in j_inf[reg]["pessoas"]:
            #print(j_inf[reg]["pessoas"][pessoa]["grau parentesco"])
            grau_parentesco = j_inf[reg]["pessoas"][pessoa]["grau parentesco"]
            if str(grau_parentesco) in grausParentesco:
                grausParentesco[grau_parentesco] = grausParentesco[grau_parentesco] + 1
            else:
                grausParentesco[grau_parentesco] = 1
    print(grausParentesco)

     
        grau_parentesco = str(j_inf[reg]["pessoas"]["pessoa" + str(index)]["grau parentesco"])
        if str(grau_parentesco) in grausParentesco:
            grausParentesco[grau_parentesco] = grausParentesco[grau_parentesco] + 1
            index += 1
        else:
            grausParentesco[grau_parentesco] = 1
            index += 1
    print(grausParentesco)


"""
if __name__ == "__main__":
    main()
