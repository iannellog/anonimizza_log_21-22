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
import sys

# questo sottoprogramma legge il file json e salva i dati in una lista di liste

def read_json_file(file):
    try:
        fin = open(file)
        log_list = json.load(fin)
        fin.close()
        return log_list
    except:
        print('*** errore *** Non è stato caricato alcun file!')
        sys.exit()
        
# questo sottoprogramma salva i dati in un nuovo file json

def save_json_file(file, data):
    try:
        fout = open(file, 'w')
        json.dump(data,fout, indent=3)
        fout.close()
    except:
        print('*** errore *** Qualcosa è andato storto durante la creazione del nuovo file')
        sys.exit()
        
# questo sottoprogramma scambia l'user name con il dato involved user se il primo è uguale a '_'

def user_missing(log):
    if(log[INDEX_UserName]=='-' and log[INDEX_InvolvedUser]!='-'):
        log[INDEX_UserName],log[INDEX_InvolvedUser]=log[INDEX_InvolvedUser],log[INDEX_UserName]

    
JsonFile = 'indata/anonimizza_test1.json'
log_list = read_json_file(JsonFile)
log_list = log_list[0]
INDEX_UserName = 1 # quello che voglio anonimizzare
INDEX_InvolvedUser = 2 # quello che voglio eliminare

# creo un dizionario in cui metto tutti i nomi (secondo elemento -> 1)
tab_codici = {}
codice = 1

for log in log_list:
    user_missing(log)
    if not log[INDEX_UserName] in tab_codici: # considero il secondo (->1) elemento di ogni elemento
        tab_codici[log[INDEX_UserName]] = str(codice).zfill(5) #per riempire di zeri fino a 5 cifre
        codice += 1 
   
for i,log in enumerate(log_list): # enumerate mi permette di scorrere anche un indice     
    log[INDEX_UserName] = tab_codici[log[INDEX_UserName]] # lo sostituisco
    # per saltare il 3° elemento
    #log_list[i] = log_list[i][:2] + log_list[3:]
    log_list[i].pop(INDEX_InvolvedUser)

# salviamo tabella dei codici e file anonimizzato   
save_json_file('indata/tab_codici.json', tab_codici)
save_json_file('indata/lista_anonimizzata.json', log_list)

print('Fine')