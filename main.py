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
def startParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",
                        help="The input file path and name",
                        type=str,
                        default='indata/anonimizza_test1.json')
    parser.add_argument("-e", "--extension",
                        help="Expected file extension",
                        type=str,
                        default='json')
    parser.add_argument("-o", "--output",
                        help="The output file path and name",
                        type=str)
    return parser.parse_args()

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


def getBaseFilePath(fullPath, extension):
    extensionsStartsAt = fullPath.find(extension)
    if extensionsStartsAt == -1:
        raise IndexError
    return inputFile[:extensionsStartsAt]


def argsOrDefault(arg, default, append):
    if arg is not None:
        return arg + append
    else:
        return default + append

if __name__ == '__main__':
    args = startParser()
    inputFile=args.input
    print(inputFile)
    try:
        basePath = getBaseFilePath(inputFile, args.extension)
    except IndexError:
        print(IndexError.__name__, "\nError! the given fileName doesn't contains the specified extension")
        exit()
    logFile = argsOrDefault(args.output, basePath, "_anonymized")
    codeFile = argsOrDefault(args.output, basePath, "_codeFile")
    toManipulate = readJsonFile(inputFile)
    idToNameAssociation = anonymizeAndGetAssociations(toManipulate)
    saveJsonFile(logFile+args.extension, toManipulate)
    saveJsonFile(codeFile+args.extension, idToNameAssociation)
