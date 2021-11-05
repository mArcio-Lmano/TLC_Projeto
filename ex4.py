import re

DIR = r"processos.txt"

def readline (file_dir, n_line):

    with open(file_dir) as file_txt:
        line = file_txt.readlines()

    return line[n_line]

def cleanName(pessoa_name):
    
    if pessoa_name[0] == ".":
        expre = r"[\. ]+([A-z ]+),([A-z ]+)"
        match = re.search(expre, pessoa_name)
        nome = match.group(1)
        grauPara = match.group(2)

    else:
        expre_1 = r"(([A-Z][a-z]+ ?){2,})(,([A-z ]+))?"
        expre = r"([A-z ]+)(,([A-z]+))?"
        match = re.search(expre_1, pessoa_name)
        nome = match.group(1)
        grauPara = match.group(4)

    return nome, str(grauPara)

def cleanPerson (pessoas_str):
    pessoas = {}
    pattern =  r"([A-z  \.,]+)([0-9]+)?"
    match = re.findall(pattern, pessoas_str)
    index = 1

    for s_match in match:
        pessoa = {}

        if s_match[0] != ".":
            nome, grau = cleanName(s_match[0])
            pessoa["nome"] = nome
            pessoa["grau parentesco"] = grau
            pessoa["processo"] = s_match[1]
            pessoas["pessoa" + str(index)] = pessoa 
            index += 1

    return pessoas

def creat_jSon (info):

    with open("teste.json", "w") as file_json:
        file_json.write(str(info))

    return print("Ficheiro Criado")


def main():
    print("Exercício 4 do projeto\n")
    line_num = 0
    j_inf = {}
    r = r"([0-9]+)::([0-9]{4}-[0-9]{2}-[0-9]{2})::([A-z ,\.:0-9]+)"

    while len(j_inf) < 20:
        line  = readline(DIR, line_num)
        line_num += 1
        match = re.search(r, line)
        processo = {}

        if match:
            idd = match.group(1)
            data = match.group(2)
            pessoas = cleanPerson(match.group(3))
            
            while idd in j_inf:
                print("Erro o id já existe")

                if pessoas == j_inf[idd]["pessoas"]: # Falta ver datas
                    print("Registo duplicado")
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

    str_json = str(j_inf)
    str_json_inf = re.sub("\'", "\"",str_json)
    creat_jSon (str_json_inf)

if __name__ == "__main__":
    main()
