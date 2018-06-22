
def getInputValues(file, ignoreValues):
    valuesToWrite = {}
    with open(file, "r") as f:
        for line in f:
            # skip comments
            if line.startswith("#"):
                continue
            # skip empty lines
            if len(line.strip()) == 0:
                continue
            # skip blank properties
            if len(line.split("=", 1)) != 2:
                continue
            key, value = line.split("=", 1)
            # skip ignored properties
            if key in ignoreValues:
                continue
            valuesToWrite[key] = value
    return valuesToWrite


def replaceValues(data, values):
    data = str(data)
    # make edits: oldValue|newValue
    for change in values:
        data = data.replace((change.split("|"))[0], (change.split("|"))[1])
    data = eval(data)
    return data


def writeOutputValues(valuesToWrite, file):
    with open(file, "r") as f:
        buf = f.readlines()
    with open("Output.txt", "w+") as f:
        for line in buf:
            if line.startswith("#"):
                f.write(line)
                continue
            if len(line.strip()) == 0:
                f.write(line)
                continue
            key, value = line.split("=",1)
            if key not in valuesToWrite:
                f.write(line)
                continue
            if key in valuesToWrite:
                line = key + "=" + valuesToWrite[key]
                del valuesToWrite[key]
                f.write(line)
        if len(valuesToWrite) > 0:
            f.write("\n\n # Properties unique to copied file\n")
            for key, value in valuesToWrite.items():
                f.write("%s=%s" % (key, value))


def copyPasteValues(inputFile, outputFile, ignoreValues, changeValues):
    copiedValues = getInputValues(inputFile, ignoreValues)
    copiedValues = replaceValues(copiedValues, changeValues)
    writeOutputValues(copiedValues, outputFile)


# Set variables here
inputFile = "CopyFromFile.txt"
outputFile = "CopyToFile.txt"
changeValues = ["apples|oranges",
                "potatoe|potato",
                "strawberry|blueberry"
                ]
ignoreValues = ["MASTER_HOST",
                "MASTER_PORT",
                "MASTER_DIR"
                ]

print("Running Script")
copyPasteValues(inputFile, outputFile, ignoreValues, changeValues)
print("Script has finished")





