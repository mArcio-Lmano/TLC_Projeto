import re

DIR = r"processos.txt"

def cleanNames(names_str):
    nomes = {}
    match = re.split(r' ', names_str)
    index = 0

    for s_match in match:
        nomes[index] = s_match
        index += 1

    return nomes


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
    """Função que dada uma string, limpa a mesma, separando nomes, graus de
    parentesco e número de processo, qualquer infromação que não corresponda
    a nenhum dos parametros do de cima será apagada

    pessoas_str :: string

    outout :: dicionário de pessoas 
    """
    pessoas = {}
    pattern =  r"(([A-Z][a-z]+ *){2,})(,([A-Z][A-z ]+). Proc.([0-9]+))?"
    match = re.findall(pattern, pessoas_str)
   
    index = 1
    for s_match in match:
        #print(s_match)
        pessoa = {}
        pessoa["nome"] = s_match[0]
        pessoa["grau parentesco"] = s_match[3]
        pessoa["processo"] = s_match[4]
        pessoas["pessoa" + str(index)] = pessoa
        index += 1

    return pessoas

def match_line(n_linha):
    """Função que dáda um linha vai ao documento txt, ler essa linha e cria 
    um sub-dicinário referente a essa linha

    n_linha :: linha que queremos ler

    output :: dicionário da linha
    """

    reg_exp = r"([0-9]+)::([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})::(.+)"
    registo = {}
    
    match = re.search(reg_exp, readline(DIR, n_linha))

    if match:
        registo["idd"] =  match.group(1)
        registo["data"] = match.group(2)
        registo["pessoas"] = cleanPersons(match.group(3))
        return registo

def creat_jSon (info):
    """Função que recebe um dicionário python, transforma esse 
    dicionário numa string e escreve a string num ficheiro do tipo 
    Json, dá return a uma mensagem a avisar que o ficheiro Json 
    foi criado
    """ 

    with open("data.json", "w") as file_json:
        json_str_Dq = str(info)
        json_str_Sq = re.sub("\'", "\"", json_str_Dq)
        file_json.write(str(json_str_Sq))

    return print("Ficheiro Criado")

def filtra_ano (registo): #funcao que recebe o registo e filtra o ano da expressão da data
    line= registo["data"]
    match =re.search(r"[0-9]{4}",line)
    return match.group()


def freq_proc(reg,dic_proc): #funçao que recebe uma linha e preenche o dicionario com o nº de proc e pessoas no ano respetivo
    index=1
    rex=r"[0-9]+"
    ano=str(filtra_ano(reg))
    dic_proc[ano]={}
    dic_proc[ano]["total"]=0
    dic_proc[ano]["processos"]=0

    if str(ano) in dic_proc:
        while "pessoa" + str(index) in reg["pessoas"]:
            match_proc = re.fullmatch(rex, str(reg["pessoas"]\
                                                    ["pessoa" + str(index)]["processo"]) )
            dic_proc[ano]["total"]+=1
            if match_proc:
                dic_proc[ano]["processos"]+=1
            index+=1
            
    else:
        while "pessoa" + str(index) in reg["pessoas"]:
            
            match_proc = re.fullmatch(rex, str(reg["pessoas"]\
                                                    ["pessoa" + str(index)]["processo"]) )
            dic_proc[ano]["total"]= 1    #dic[str(newReg["ano"])][0]
            if match_proc:
                dic_proc[ano]["processos"]+=1
            index+=1
    #print(dic)
    return (dic_proc)

def calcula_freq (dic_proc): #funçao que dado um dicionario com o nº de proc e de pessoas associado calcula a media
    for key in dic_proc:
        freq={}
        freq[key]=dic_proc[key]["processos"]/dic_proc[key]["total"]
        print(freq)
    return (freq)


