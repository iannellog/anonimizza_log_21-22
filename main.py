import json
import sys
import argparse

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


def readJsonFile(fileName):
    try:
        jsonFile = open(fileName)
        data = json.load(jsonFile)  # This is a list of lists
        jsonFile.close()
        return data
    except OSError as e:
        print(e)
        exit()


def saveJsonFile(fileName, dumpData, indent=3):
    try:
        file = open(fileName, 'w')
        json.dump(dumpData, file, indent=indent)
        file.close()
    except OSError as e:
        print(e)
        exit()


def reformatUserNameAndCompleteUserInfo(userLog):
    if userLog[1] == '-' and userLog[2] != '-':
        userLog[1], userLog[2] = userLog[2], userLog[1]


def getUserIndex(userLog, userNameToCode, userIndex):  # TODO: Cange this variable with uuid
    if userLog[1] in userNameToCode:
        return userNameToCode[userLog[1]], userIndex
    currentUserIndex = str(userIndex).zfill(5)
    userNameToCode[
        userLog[1]] = currentUserIndex  # Create a string of 5 characters adding missing zero before the number
    userIndex += 1
    return currentUserIndex, userIndex


def anonymizeAndGetAssociations(jsonData):
    userNameToCode = {}
    userIndex = 1
    for logDays in jsonData:
        for userLog in logDays:
            reformatUserNameAndCompleteUserInfo(userLog)
            currentUserIndex, userIndex = getUserIndex(userLog, userNameToCode, userIndex)
            userLog[1] = currentUserIndex
            userLog.remove(userLog[2])  # Removing involved user info
    return userNameToCode


def getInputFIleName():
    for index, arg in enumerate(sys.argv):
        if arg == '-i' and not sys.argv[index + 1].startswith("-"):
            return sys.argv[index + 1]
    return "indata/anonimizza_test1.json"


def getBaseFilePath(fullPath):
    extension = ".json"
    extensionsStartsAt = inputFile.find(extension)
    if extensionsStartsAt == -1:
        raise IndexError
    return inputFile[:extensionsStartsAt], extension


if __name__ == '__main__':
    inputFile = getInputFIleName()
    try:
        basePath, extension = getBaseFilePath(inputFile)
    except IndexError:
        print(IndexError.__name__, "\nError! the given fileName doesn't contains the specified extension")
        exit()
    logFile = basePath + "_anonymized"
    codeFile = basePath + "_codeFile"
    toManipulate = readJsonFile(inputFile)
    idToNameAssociation = anonymizeAndGetAssociations(toManipulate)
    saveJsonFile(logFile+extension, toManipulate)
    saveJsonFile(codeFile+extension, idToNameAssociation)
