import re
from re_TLC import *

DIR = r"processos.txt"

def main():
    print("Exercício 1 do projeto\n")
    
    json_info = {}
    dic={}
    line = 0
    index = 1
    nlinhas=60 #37889
    while line <= nlinhas:
        reg = match_line(line)
        if reg != None:
            idd = reg["idd"]

            while reg["idd"] in json_info:

                if reg["pessoas"] == json_info[idd]["pessoas"]\
                    and reg["data"] == json_info[idd]["data"]:
                    print("Registo duplicado")
                    break
                else:        
                    idd += f".{index}"
                    reg["idd"] = idd

            else:
                json_info[idd] = reg
                #print(reg)
                freq_proc(reg,dic)
                     
            line += 1
                
        else:

            line+=1
    calcula_freq (dic)
    
       
if __name__ == "__main__":
    main()
