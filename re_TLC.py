import re

DIR = r"processos.txt"

def readline (file_dir, n_line):
    """Função que dáda um ficheiro e um numero vai buscar a infromação
    referente a essa linha

    file_dir :: Ficheiro que pretendemos ler
    n_linha :: Número relativo à linha que pretendemos ler
    """
    with open(file_dir) as file_txt:
        line = file_txt.readlines()

    return line[n_line]

def cleanPersons (pessoas_str):
    pessoas = {}
    pattern =  r"(([A-Z][a-z]+ ?){2,})((,[A-z ]+). Proc.([0-9]+))?"
    match = re.findall(pattern, pessoas_str)
   
    index = 1
    for s_match in match:
        pessoa = {}
        pessoa["nome"] = s_match[0]
        pessoa["grau parentesco"] = s_match[3]
        pessoa["processo"] = s_match[4]
        pessoas["pessoa" + str(index)] = pessoa
        index += 1

    return pessoas

def match_line(n_linha):
    reg_exp = r"([0-9]+)::([0-9]{4}-[0-9]{2}-[0-9]{2})::(.+)"
    registo = {}
    
    match = re.search(reg_exp, readline(DIR, n_linha))
    
    if match:
        registo["idd"] =  match.group(1)
        registo["data"] = match.group(2)
        registo["pessoas"] = cleanPersons(match.group(3))
        return registo

def creat_jSon (info):

    with open("teste.json", "w") as file_json:
        json_str_Dq = str(info)
        json_str_Sq = re.sub("\'", "\"", json_str_Dq)
        file_json.write(str(json_str_Sq))

    return print("Ficheiro Criado")


