"""
Created on Oct. 29, 2021
by Giulio Iannello

Programma che anonimizza un file di log prdotto da moodle

   I dati nel file json sono composti da: 
    
Data/Ora,
Nome completo dell'utente
Utente coinvolto
Contesto dell'evento
Componente
Evento
Descrizione
Origine
Indirizzo IP

Anonimizzo il file ed elimono il dato 'Utente coinvolto';
Se non è possibile individuare l'utente con 'Nome completo dell'utente'
(poiche uguale a '-'), lo scambio con 'Utente coinvolto'
"""

import json

fin = open('indata/anonimizza_test1.json')
log_list = json.load(fin)
log_list = log_list[0]

INDEX_UserName = 1 # quello che voglio anonimizzare
INDEX_InvolvedUser = 2 # quello che voglio eliminare

# creo un dizionario in cui metto tutti i nomi (secondo elemento -> 1)
tab_codici = {}
codice = 1

for log in log_list:
    #inverto i 2° ed il 3° se il 2° è uguale a '-'
    if(log[INDEX_UserName]=='-' and log[INDEX_InvolvedUser]!='-'):
        log[INDEX_UserName],log[INDEX_InvolvedUser]=log[INDEX_InvolvedUser],log[INDEX_UserName]
    if not log[1] in tab_codici: # considero il secondo (->1) elemento di ogni elemento
        tab_codici[log[INDEX_UserName]] = str(codice).zfill(5) #per riempire di zeri fino a 5 cifre
        codice += 1 
 
   
for i,log in enumerate(log_list): # enumerate mi permette di scorrere anche un indice     
    log[INDEX_UserName] = tab_codici[log[INDEX_UserName]] # lo sostituisco
    # per saltare il 3° elemento
    #log_list[i] = log_list[i][:2] + log_list[3:]
    log_list[i].pop(INDEX_InvolvedUser)

# salviamo tabella dei codici e file anonimizzato   

fout = open('indata/tab_codici.json', 'w')
json.dump(tab_codici,fout, indent=3 )
fout.close()

fout = open('indata/lista_anonimizzata.json', 'w')
json.dump(log_list,fout, indent=3 )
fout.close()

print('Fine')