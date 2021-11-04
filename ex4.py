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
    j_inf = []

    while len(j_inf) < 20:
        line  = readline(DIR, line_num)
        line_num += 1

        #print(line)

        j_inf.append(line)

    
    print(j_inf)
    creat_jSon (j_inf)

if __name__ == "__main__":
    main()
