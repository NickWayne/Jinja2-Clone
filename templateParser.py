import re
from pipes import Pipes

class Parser(object):

    def __init__(self, vars: dict):
        self.vars = vars
        self.toggled = False
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
                out.write(self.ruleParser(line))   

                

    def ruleParser(self, line: str):
        if (line.find("{%") != -1):
            self.controlFlow(line.strip()[2:-2])
        elif (not self.toggled):
            return self.insertParameter(line)
        return "\n"

    def controlFlow(self, line: str):
        if (self.toggled):
            if (line.find("endif") != -1):
                self.toggled = False       
        elif (line.find("endif") == -1 and line.find("if") != -1 and not eval(line[4:], self.vars)):
            self.toggled = True
            
        
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
        else:
            return None

    def applyPipes(self, var, pipes):
        for pipe in pipes:
            pipe = self.pipes.get(pipe)
            if (pipe != None):
                var = pipe(var)
        
        return var
