import json

"""
Inside json info:
Data/Ora,
Nome completo dell'utente
Utente coinvolto
Contesto dell'evento
Componente
Evento
Descrizione
Origine
Indirizzo IP

"""


def getJsonData(fileName):
    jsonFile = open(fileName)
    data = json.load(jsonFile)  # This is a list of lists
    jsonFile.close()
    return data


def anonymizeAndGetAssociations(jsonData):
    codeToUserName = {}
    userIndex = 1
    for logDays in jsonData:
        for userLog in logDays:
            codeToUserName[userIndex] = userLog[1]
            userLog[1] = userIndex  # User name
            userLog[2] = None
            userIndex += 1
    return codeToUserName


def saveOnFile(fileName, dumpData, indent=3):
    file = open(fileName, 'w')
    json.dump(dumpData, file, indent=indent)
    file.close()


if __name__ == '__main__':
    jsonFileName = 'indata/anonimizza_test1.json'
    toManipulate = getJsonData(jsonFileName)
    idToNameAssociation = anonymizeAndGetAssociations(toManipulate)
    saveOnFile('indata/anonymized.json', toManipulate)
    saveOnFile('indata/codeToUserName', idToNameAssociation)
