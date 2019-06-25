def insertParameter(line: str):
    lst = []
    while line != "":
        startIndex = line.find("{{")
        if (startIndex != -1):
            lst.append(line[:startIndex])
            endIndex = line.find("}}")
            lst.append(line[startIndex:endIndex+2])
            line = line[endIndex+2:]
        else:
            lst.append(line)
            line = ""

insertParameter("<p>Hello World! {{ arr | length}} elements in the array: {{arr}}</p>")