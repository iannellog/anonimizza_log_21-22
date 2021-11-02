"""
Created on Nov. 1, 2021
by Simone Pio Caronia

Programma che anonimizza un file di log prodotto da moodle

Info on Json:
    - Data/Ora
    - Nome completo dell'utente
    - Utente coinvolto
    - Contesto dell'evento
    - Componente
    - Evento
    - Descrizione
    - Origine
    - Indirizzo IP
"""

import json
import uuid

INDEX_COMPLETE_NAME = 1
INDEX_AFFECTED_USER = 2
NO_USER = "no-user"


def read_and_return_json(path):
    try:
        f_in = open(path)
        data = json.load(f_in)
        f_in.close()
        return True, data
    except:
        return False, []


def get_logs_and_users_dict(json_logs_from_file):
    dict_user = dict()
    anonymous_all_logs = list()

    for logs_list in json_logs_from_file:
        anonymous_logs = list()

        for log in logs_list:
            user_id = get_user_anonymous_uuid_and_insert_if_not_present(log, dict_user)
            log[INDEX_COMPLETE_NAME] = user_id  # anonymous uuid in place of "Nome completo dell'utente"
            del log[INDEX_AFFECTED_USER]  # removing "Utente coinvolto"
            anonymous_logs.append(log)

        anonymous_all_logs.append(anonymous_logs)

    return anonymous_all_logs, dict_user


def get_user_anonymous_uuid_and_insert_if_not_present(log, dict_user):
    user = log[INDEX_COMPLETE_NAME] if log[INDEX_COMPLETE_NAME] != '-' else log[INDEX_AFFECTED_USER]
    if user == '-':
        user = NO_USER  #giving default value if not present in both elements of log

    if user in dict_user.keys():
        return dict_user[user]
    else:
        new_id = uuid.uuid5(uuid.NAMESPACE_URL, user)  #creation of UUID value based on user value
        dict_user[user] = str(new_id)
        return dict_user[user]


def save_to_path(values, path, indent=3):
    success = True
    try:
        f_out = open(path, 'w')
        json.dump(values, f_out, indent=indent)
        f_out.close()
    except:
        success = False

    return success


if __name__ == '__main__':
    print('Starting to anonymize logs...')
    ok, jsonData = read_and_return_json('indata/anonimizza_test1.json')
    if not ok:
        print('Ops! Something went wrong during reading file!')
        exit()

    logs, users_dict = get_logs_and_users_dict(jsonData)
    if save_to_path(logs, 'indata/anonimizza_test1_anonimizzato.json') \
            and save_to_path(users_dict, 'indata/anonimizza_test1_tab_codici.json'):
        print('Operations completed successfully!')
    else:
        print('Ops! Something went wrong during writing files!')
