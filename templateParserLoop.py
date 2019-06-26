import re
from pipes import Pipes

class Parser(object):

    def __init__(self, vars: dict):
        self.vars = vars
        self.toggled = False
        self.loop = False
        self.loopLines = []
        self.loopData = ""
        self.pipes = {
            "split": Pipes.split,
            "length": Pipes.length,
            "str": Pipes.to_string,
            "max": Pipes.max,
            "min": Pipes.min
        }

    def updateVars(self, vars: dict):
        self.vars = vars

    def parseDocument(self, document: str, output: str = "out.html"):
        with open(document, 'r') as template, open(output, 'w') as out:
            for line in template:
                self.ruleParser(line, out) 

                

    def ruleParser(self, line: str, out):
        if (line.find("{%") != -1):
            self.controlFlow(line.strip()[2:-2])
        elif (not self.toggled):
            if (self.loop):
                self.loopLines.append(line)
            elif (not self.loop and len(self.loopLines) != 0):
                if (isinstance(self.loopData, int)):
                    for i in range(self.loopData):
                        for line in self.loopLines:
                            out.write(self.insertParameter(line))
                else:
                    for data in self.loopData:
                        self.vars[self.loopDataIdentifier] = data
                        for line in self.loopLines:
                            out.write(self.insertParameter(line))
                self.loopLines = []
            else:
                out.write(self.insertParameter(line))
        else:
            out.write("\n")

    def controlFlow(self, line: str):
        if (self.toggled):
            if (line.find("endif") != -1):
                self.toggled = False
                return       
        elif (line.find("endif") == -1 and line.find("if ") != -1 and not eval(line[4:], self.vars)):
            self.toggled = True
            return

        if (self.loop and line.find("endfor") != -1):
            self.loop = False
            return
        elif (line.find("for") != -1 ):
            self.loop = True
            ran = line.find("range(")
            if ran != -1:
                self.loopData = int(line[ran+6:line.find(")")])
            else: 
                data = line[line.find("in ")+2:line.find("}")].strip()
                self.loopData = self.varLookup(data)
                self.loopDataIdentifier = line[line.find("for ") + 4: line.find("in")].strip()
        
    def insertParameter(self, line: str):
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
            if lst[-1].startswith("{{"):
                lst[-1] = self.varLookup(lst[-1][2:-2].strip())


        return "".join(map(str, lst))

    def varLookup(self, var: str):
        pipes = []
        if (var.find("|") != -1):
            pipes = var.split("|")
            var = pipes[0].strip()
            pipes.pop(0)
        if (self.vars.get(var) != None):
            return self.applyPipes(eval(var, self.vars), map(str.strip, pipes))
            return self.applyPipes(self.evalVars(var), map(str.strip, pipes))
        else:
            return None

    # def evalVars(var: str):
    #     lst = []
    #     while var != "":
    #         dot = var.find(".")
    #         bracket = var.find("[")
    #         if (dot != -1 and dot < bracket):
            
    #         elif (bracket !=)

    def applyPipes(self, var, pipes):
        for pipe in pipes:
            pipe = self.pipes.get(pipe)
            if (pipe != None):
                var = pipe(var)
        
        return var