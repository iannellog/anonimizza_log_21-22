"""
Created on Oct. 29, 2021
by Giulio Iannello

Programma che anonimizza un file di log prdotto da moodle
"""

import json

fin = open('/Users/iannello/Home/Didattica/Programmazione/code/[21-22]/anonimizza_log_21-22/indata/anonimizza_test1.json')
log_list = json.load(fin)
fin.close()

log_list = log_list[0]

tab_codici = {}
codice = 1
for log in log_list:
    if not log[1] in tab_codici:
        tab_codici[log[1]] = str(codice).zfill(5)
        codice += 1

for i, log in enumerate(log_list):
    log[1] = tab_codici[log[1]]
    log_list[i].pop(2)

fout = open('/Users/iannello/Home/Didattica/Programmazione/code/[21-22]/anonimizza_log_21-22/indata/anonimizza_test1_tab_codici.json', 'w')
json.dump(tab_codici, fout, indent=3)
fout.close()

fout = open('/Users/iannello/Home/Didattica/Programmazione/code/[21-22]/anonimizza_log_21-22/indata/anonimizza_test1_anonimizzato.json', 'w')
json.dump(log_list, fout, indent=3)
fout.close()

print('Fine')