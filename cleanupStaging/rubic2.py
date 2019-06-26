from pipes import Pipes
class Rubic2(Object):

    def __init__(self, vars: dict):
        self.vars = vars # all local variables
        self.render = True # control flow render
        self.loop = False # Inside a loop block, add lines
        self.loopLines = [] # Lines inside loop block
        self.loopData = "" # List, range
        self.loopVar = "" # Loop Var Name
        self.pipes = { # Pipe names mapped to the function
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
            out.write("\n")
        elif (self.render):
            if (self.loop): # TODO Add true range support
                self.loopLines.append(line)
            elif (len(self.loopLines) != 0):
                if (isinstance(self.loopData, int)):
                    for i in range(self.loopData):
                        for line in self.loopLines:
                            out.write(self.bindExpressions(line))
                else:
                    for data in self.loopData:
                        self.vars[self.loopVar] = data
                        for line in self.loopLines:
                            out.write(self.bindExpressions(line))
                self.loopLines = [] # Clear looped lines 
            else:
                out.write(self.bindExpressions(line))
        else:
            out.write("\n")

    def controlFlow(self, line: str):
        if (not self.render):
            if (line.find("endif") != -1):
                self.render = True
                return
        # not eval() takes the boolean expressions from the if statement and evaluates based on the vars
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
                self.loopData = int(line[ran+6 : line.find(")")])
            else: 
                # Grab the var that the for loop is looping over
                data = line[line.find("in ")+2 : line.find("}")].strip()
                self.loopData = self.varLookup(data)
                # Grab the variable name of the for loop
                self.loopVar = line[line.find("for ") + 4 : line.find("in")].strip()
            
    def bindExpressions(self, line: str):
        lst = []
        while line != "":
            startIndex = line.find("{{")
            # There is an expresison left in the line
            if (startIndex != -1):
                # Everything before the expression
                lst.append(line[:startIndex])
                endIndex = line.find("}}")
                # The expression itself, then remove curly braces and whitespace then replace the expression with it's value
                lst.append(self.varLookup(line[startIndex:endIndex+2][2:-2].strip()))
                # remove everything before the end of the expression from the line
                line = line[endIndex+2:]
            # No more expressions left in the line
            else:
                # Add the remaining text and empty the string
                lst.append(line)
                line = ""
        # Join the list back up into a single string and return
        return "".join(map(str, lst))

    def varLookup(self, var: str):
        pipes = var.split("|")
        var = pipes[0].strip()
        if (len(pipes > 1)):
            pipes.pop(0) # Removes the variable from the pipes list
            pipes = map(str.strip, pipes)
            return self.applyPipes(self.expandDotBracketNotation(var), pipes)
        else:
            return self.expandDotBracketNotation(var)

    def expandDotBracketNotation(self, var: str):
        lst = []
        while var != "":
            dot = var.find(".")
            bracket = var.find("[")
            # Dot notation closer than bracket or dot exists and bracket doesn't
            if ((dot != -1 and dot < bracket) or (dot != -1 and bracket == -1)):
                # Append everything before the dot from string
                lst.append(var[:dot])
                # String becomes everything after the dot
                var = var[dot+1:]
            # Bracket notation closer than dot or bracket exists and dot doesn't            
            elif ((bracket != -1 and bracket < dot)  or (bracket != -1 and dot == -1)):
                # Append everything before the bracket from string
                lst.append(var[:bracket])
                # String in the brackets gets expanded
                # Ex: "['test here']['orange']" -> "test here['orange']"
                var = var[bracket+2:var.find("]")-1] + var[var.find("]")+1:]
            # Dot and bracket do not exist
            else:
                # Add the rest and empty the string
                lst.append(var)
                var = ""
        return objectCLassExpansion(lst)

    def objectCLassExpansion(self, lst):
        # Local var to hold the varlist to be mutated
        data = self.vars
        for atr in lst:
            # Data is a class(Must inherit from object), and the atr is not first in the list
            if (isinstance(data, object) and atr != lst[0] and not isinstance(data, dict)):
                # There is a function call in the expression
                if (atr.find("(") != -1):
                    # Get an array of the arguments in the function
                    args = self.parseArguments(atr)
                    # Grab the function from the class
                    func = getattr(data, atr[:atr.find("(")])
                    # Call the function with the expanded args
                    data = func(*args)
                else:
                    # Drill down into the data structure
                    data = getattr(data,atr)
            else:
                # Drill down into the data structure
                data = data[atr]
        return data

    def parseArguments(self, args):
        # Split the argument list and strip the values
        args = list(map(str.strip, args[args.find("(")+1:-1].split(",")))
        if (len(args) == 1 and args[0] == ''):
            # No arguments so return empty list
            return []
        else:
            argReturn = []
            for arg in args:
                # if the argument is a string, remove the quotes
                if (arg.startswith("\"") or arg.startswith("'")):
                    argReturn.append(arg[1:-1])
                else:
                    argReturn.append(self.varLookup(arg))
            return argReturn

    def applyPipes(self, var, pipes):
        for pipe in pipes:
            # Set pipe equal to the Pipe function associated with the pipe string
            pipe = self.pipes.get(pipe)
            if (pipe != None):
                var = pipe(var)
        return var
