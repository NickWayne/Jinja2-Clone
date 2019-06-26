def evalVars(var: str):
    lst = []
    while var != "":
        dot = var.find(".")
        bracket = var.find("[")
        if ((dot != -1 and dot < bracket) or (dot != -1 and bracket == -1)):
            lst.append(var[:dot])
            var = var[dot+1:]
        elif ((bracket != -1 and bracket < dot)  or (bracket != -1 and dot == -1)):
            lst.append(var[:bracket])
            var = var[bracket+2:var.find("]")-1] + var[var.find("]")+1:]
        else:
            lst.append(var)
            var = ""
    return lst

print(evalVars("test.apple['total money']['gosh'].wow['please']"))