"""
Created on Sun Nov  7 13:42:58 2021

@author: agnes
"""
'''Programma che anonimizza un file di log prdotto da moodle
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
'''

# importo i moduli
import json
import sys


# sottoprogramma che legge il file in formato json e crea una lista di liste 
def read_jsonfile(file):
    # eccezione
    try:
        fin = open(file)
        log_list = json.load(fin)
        fin.close()
        return log_list
    except:
        print('*** errore *** Non è stato trovato nessun file')
        sys.exit()

        # sottoprogramma che salva il nuovo file in formato json


def save_jsonfile(file, data):
    try:
        fout = open(file, 'w')
        json.dump(data, fout, indent=3)
        fout.close()
    except:
        print('*** errore *** Il salvataggio non è andato a buon fine')
        sys.exit()

        # sottoprogramma che scambia il campo UTENTE COINVOLTO con il campo NOME COMPLETO DELL'UTENTE 
        # se quest'ultimo è vuoto


def nomecompleto_mancante(log):
    if (log[INDEX_NomeCompletoUtente] == '-' and log[INDEX_UtenteCoinvolto] != '-'):
        log[INDEX_NomeCompletoUtente], log[INDEX_UtenteCoinvolto] = log[INDEX_UtenteCoinvolto], log[
            INDEX_NomeCompletoUtente]


# inizializzo il file, la lista di liste e dichiaro gli indici dei campi di interesse
JsonFile = 'indata/anonimizza_test1.json'
log_list = read_jsonfile(JsonFile)
log_list = log_list[0]
INDEX_NomeCompletoUtente = 1  # campo da anonimizzare (secondo campo => 1)
INDEX_UtenteCoinvolto = 2  # campo da escludere (terzo campo => 2)

# Creo la DICT e con un ciclo scorro tutta la lista di log 
tab_codici = {}
codice = 1

for log in log_list:
    nomecompleto_mancante(log)  # se il nome completo è vuoto interviene il sottoprogramma
    if not log[INDEX_NomeCompletoUtente] in tab_codici:  # controllo che il campo di interesse si trovi nelle chiavi della tabella
        # associo il secondo campo ad un codice che è una stringa di lunghezza fissa 5
        tab_codici[log[INDEX_NomeCompletoUtente]] = str(codice).zfill(5)
        codice += 1

    # controllo se l'i-esimo log è nella LISTA ENUMERATA ( oggetto assegnato a un indice ) 
# controllo se il secondo campo dei LOG si trova nella tabella
for i, log in enumerate(log_list):
    log[INDEX_NomeCompletoUtente] = tab_codici[log[INDEX_NomeCompletoUtente]]
    # per escludere il campo UTENTE COINVOLTO
    log_list[i].pop(INDEX_UtenteCoinvolto)

# salviamo tabella dei codici e file anonimizzato   
save_jsonfile('indata/tab_codici.json', tab_codici)
save_jsonfile('indata/lista_anonimizzata.json', log_list)

print('Fine')