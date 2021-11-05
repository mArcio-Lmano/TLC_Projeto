import re

DIR = r"processos.txt"

def readline (file_dir, n_line):
    with open(file_dir) as file_txt:
        line = file_txt.readlines()
    return line[n_line]

#print(readline(DIR, 2))

def creat_jSon (info):
    with open("teste.json", "w") as file_json:
        file_json.write(str(info))

    return print("Ficheiro Criado")


def main():
    print("Exercício 4 do projeto\n")
    
    proc_numb = 20
    
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
            pessoas = match.group(3)
            
            processo["id"] = str(idd)
            processo["data"] = str(data)
            processo["pessoas"] = str(pessoas)

        j_inf[str(idd)] = processo
 
    str_json = str(j_inf)
    str_json_inf = re.sub("\'", "\"",str_json)
    creat_jSon (str_json_inf)

if __name__ == "__main__":
    main()
