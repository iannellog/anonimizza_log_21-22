# anonimizza_log_21-22
Esercizio per l'anonimizzazione di un file di log estratti da e-learning (Insegnamento di Programmazione, a.a. 21/22)

Scrivere un programma Python che legge una lista di log dal file “anonimizza_test1.json” (la struttura del file .json non è specificata e va preliminarmente determinata). 

Ciascun elemento della lista di log è costituito dalle seguenti 9 informazioni:

- Data/Ora
- Nome completo dell'utente
- Utente coinvolto
- Contesto dell'evento
- Componente
- Evento
- Descrizione
- Origine
- Indirizzo IP

Il programma deve anonimizzare la lista. In particolare:
- per ogni utente (campo “Nome completo dell'utente”) generare un identificatore unico (per esempio un numero progressivo) 
- sostituire nel log l’identificatore unico al nome dell’utente
- generare una tabella che mantiene l’informazione di quale identificatore è stato associato a ciascun utente
- eliminare da tutti i log il campo “Utente coinvolto”, che normalmente contiene la stringa “-“, ma potrebbe contenere anch’esso il nome dell’utente

Il programma infine deve salvare la lista di log anonimizzata nello stesso formato di partenza (json) e la tabella che associa ciascun utente al suo identificatore unico (anche la tabella va salvata in formato json). Il file di log anonimizzato va salvato come lista di log, e ciascun log come una lista di informazioni. 

Nel caso in campo 'Nome completo dell'utente' sia vuoto (contiene il carattere '-') si utilizzi il campo 'Utente coinvolto' per attribuire il log a un utente. 

Il programma richiede di passare su linea di comando il path e il nome del file di ingresso. I dati anonimizzati e la tabella che associa gli utenti all'identificatore unico sono salvati in due file .json il cui nome termina con le stringhe '_anonimizzato' e '_usercodes'

Ulteriori modifiche
- usare argparse per implementare una CLI più flessibile
