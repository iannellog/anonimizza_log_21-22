"""
Created on Oct. 29, 2021
by Giulio Iannello

Programma che anonimizza un file di log prdotto da moodle
"""

import json

fin = open('/Users/mariaelenacontini/Desktop/programmazione/anonimizza_git/anonimizza_log_21-22/indata/anonimizza_test1.json')
log_list = json.load(fin)
log_list = log_list[0]

# creo un dizionario in cui metto tutti i nomi (secondo elemento -> 1)
tab_codici = {}
codice = 1


for log in log_list:
    #inverto i 2° ed il 3° se il 2° è uguale a '-'
    if(log[1]=='-' and log[2]!='-'):
        log[1],log[2]=log[2],log[1]
    if not log[1] in tab_codici: # considero il secondo (->1) elemento di ogni elemento
        tab_codici[log[1]] = str(codice).zfill(5) #per riempire di zeri fino a 5 cifre
        codice += 1 
 
  # enumerate mi permette di scorrere anche un indice      
for i,log in enumerate(log_list):
    log[1] = tab_codici[log[1]] # lo sostituisco
     # per saltare il 3° elemento
    #log_list[i] = log_list[i][:2] + log_list[3:]
    log_list[i].pop(2)
 # salviamo tabella dei codici e file anonimizzato   
fout = open('/Users/mariaelenacontini/Desktop/programmazione/anonimizza_git/anonimizza_log_21-22/indata/tab_codici.json', 'w')
json.dump(tab_codici,fout, indent=3 )
fout.close()

fout = open('/Users/mariaelenacontini/Desktop/programmazione/anonimizza_git/anonimizza_log_21-22/indata/lista_anonimizzata.json', 'w')
json.dump(log_list,fout, indent=3 )
fout.close()


print('Fine')