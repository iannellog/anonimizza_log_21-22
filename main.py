import json
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


def initializeParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help="The input/output file path",
                        type=str,
                        default='indata/')
    parser.add_argument("-i", "--input",
                        help="The input file name, no extension",
                        type=str,
                        default="anonimizza_test1"
                        )
    parser.add_argument("-e", "--extension",
                        help="Input/output file extension, including dot (Es -> .json)",
                        type=str,
                        default='.json')
    parser.add_argument("-o", "--output",
                        help="The output file name, no extension, Default = \'output\'",
                        type=str,
                        default='output')
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
    except json.JSONDecodeError:
        print('Error! The specified input file doesn\'t contains info in json format.')
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
    if userLog[1].lower() in userNameToCode:
        return userNameToCode[userLog[1].lower()], userIndex
    currentUserIndex = str(userIndex).zfill(5)
    userNameToCode[userLog[1].lower()] = currentUserIndex  # Create a string of 5 characters adding missing zero before the number
    userIndex += 1
    return currentUserIndex, userIndex


def anonymizeAndGetAssociations(jsonData):
    userNameToCode = {}
    userIndex = 1
    jsonData = jsonData[0]  # Removing useless list
    for userLog in jsonData:
        reformatUserNameAndCompleteUserInfo(userLog)
        currentUserIndex, userIndex = getUserIndex(userLog, userNameToCode, userIndex)
        userLog[1] = currentUserIndex
        userLog.remove(userLog[2])  # Removing involved user info
    return userNameToCode


def formatFilePath(args):
    # Check if last words contains a dot
    filePath = args.path
    inputFileName = args.input if '.' not in args.input else args.input.split('.')[0]
    fileExtension = args.extension if '.' not in args.input else '.' + args.input.split('.')[1]
    pathSlices = filePath.split('/')
    lastIndex = len(pathSlices) - 1
    if '.' in pathSlices[lastIndex]:  # Means that the last element is a file name including extension
        fileNameAndExtension = pathSlices[lastIndex].split('.')
        inputFileName = fileNameAndExtension[0]
        fileExtension = '.' + fileNameAndExtension[1]
        del pathSlices[lastIndex]
        filePath = ''.join([(element + '/') for element in pathSlices])
    return filePath, inputFileName, fileExtension


if __name__ == '__main__':
    args = initializeParser()
    basePath, inputFile, extension = formatFilePath(args)
    logFile = args.output + '_anonymize'
    codeFile = args.output + '_codeFile'
    toManipulate = readJsonFile(basePath+inputFile+extension)
    idToNameAssociation = anonymizeAndGetAssociations(toManipulate)
    saveJsonFile(basePath+logFile+args.extension, toManipulate)
    saveJsonFile(basePath+codeFile+args.extension, idToNameAssociation)
