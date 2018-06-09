from ipdb import set_trace
def count(line, prev):
    """
    @type line: str
    @type prev: tuple(int)
    """
    line = line.strip()
    leftnum = prev[0]
    rightnum = prev[1]
    condition = prev[2]
    i = 0
    while i < len(line):
        if condition == '"':
            if line[i] == "\\":
                i += 2
            elif line[i] == '"':
                condition = None
                i += 1
            else:
                i += 1
        elif condition == "'":
            if line[i] == "\\":
                i += 2
            elif line[i] == "'":
                condition = None
                i += 1
            else:
                i += 1
        else:
            if line[i] == "(":
                leftnum += 1
            elif line[i] == ")":
                rightnum += 1
            elif line[i] == '"':
                condition = '"'
            elif line[i] == "'":
                condition = "'"
            i += 1
    return (leftnum, rightnum, condition)


def getargument(lines):
    argdict = dict()
    conditionstack = list()
    temparg = ""
    tempargtype = ""
    argnum = -1
    for row, line in enumerate(lines):
        i = 0
        while i < len(line):
            if len(conditionstack) == 0:
                if line[i] == "(":
                    conditionstack.append("()")
                elif line[i:].startswith("->"):
                    conditionstack.append("->")
                    i += 1
                elif line[i] == ":" or (row == (len(lines) - 1) and i == (len(line) - 1)):
                    if tempargtype != "":
                        argdict[-1]["type"] = tempargtype

                i += 1
            elif conditionstack[-1] == "()":
                if line[i].isalpha():
                    tempargpos = (row, i)
                    argnum += 1
                    conditionstack.append("arg")
                elif line[i] == "=":
                    conditionstack.append("=")
                    i += 1
                elif line[i] == ",":
                    argdict[argnum] = dict()
                    argdict[argnum]["pos"] = tempargpos
                    argdict[argnum]["arg"] = temparg
                    if tempargtype != "":
                        argdict[argnum]["type"] = tempargtype
                    temparg = ""
                    tempargtype = ""
                    i += 1
                elif line[i] == ")":
                    if argnum >= 0:
                        argdict[argnum] = dict()
                        argdict[argnum]["pos"] = tempargpos
                        argdict[argnum]["arg"] = temparg
                        if tempargtype != "":
                            argdict[argnum]["type"] = tempargtype
                    conditionstack.pop()
                    argdict[-1] = dict()
                    argdict[-1]["pos"] = (row, i)
                    tempargtype = ""
                    temparg = ""
                elif line[i] == ":":
                    conditionstack.append(":")
                    i += 1
                else:
                    i += 1
            elif conditionstack[-1] == "arg":
                if line[i].isalpha() or line[i].isdigit() or line[i] == "_":
                    temparg += line[i]
                    i += 1
                elif line[i] == "=" or line[i] == " " or line[i] == "," or line[i] == ")":
                    conditionstack.pop()
                elif line[i] == ":":
                    conditionstack.append(":")
                    i += 1
                elif line[i] == ",":
                    conditionstack.pop()
                else:
                    i += 1
            elif conditionstack[-1] == ":":
                if line[i] != "," and line[i] != ")" and line[i] != " ":
                    tempargtype += line[i]
                if line[i] == '"':
                    conditionstack.append('"')
                elif line[i] == "'":
                    conditionstack.append("'")
                elif line[i] == "[":
                    conditionstack.append("[")
                elif line[i] == "{":
                    conditionstack.append("{")
                elif line[i] == "(":
                    conditionstack.append("(")
                elif line[i] == ")":
                    conditionstack.pop()
                    continue
                elif line[i] == ",":
                    conditionstack.pop()
                    continue
                i += 1
            elif conditionstack[-1] == "->":
                if line[i] != "," and\
                        line[i] != ")" and\
                        line[i] != " " and\
                        line[i] != ":":
                    tempargtype += line[i]
                if line[i] == '"':
                    conditionstack.append('"')
                elif line[i] == "'":
                    conditionstack.append("'")
                elif line[i] == "[":
                    conditionstack.append("[")
                elif line[i] == "{":
                    conditionstack.append("{")
                elif line[i] == "(":
                    conditionstack.append("(")
                elif line[i] == ":":
                    conditionstack.pop()
                    continue
                i += 1
            elif conditionstack[-1] == "=":
                if line[i] == '"':
                    conditionstack.append('"')
                elif line[i] == "'":
                    conditionstack.append("'")
                elif line[i] == "[":
                    conditionstack.append("[")
                elif line[i] == "{":
                    conditionstack.append("{")
                elif line[i] == "(":
                    conditionstack.append("(")
                elif line[i] == ")":
                    conditionstack.pop()
                    continue
                elif line[i] == ",":
                    conditionstack.pop()
                    continue
                i += 1
            elif conditionstack[-1] == '"' or conditionstack[-1] == "'":
                if line[i] == conditionstack[-1]:
                    conditionstack.pop()
                    i += 1
                elif line[i] == "\\":
                    i += 2
                else:
                    i += 1
            elif conditionstack[-1] == "[":
                if ":" in conditionstack or "->" in conditionstack:
                    tempargtype += line[i]
                if line[i] == '"':
                    conditionstack.append('"')
                elif line[i] == "'":
                    conditionstack.append("'")
                elif line[i] == "[":
                    conditionstack.append("[")
                elif line[i] == "{":
                    conditionstack.append("{")
                elif line[i] == "(":
                    conditionstack.append("(")
                elif line[i] == "]":
                    conditionstack.pop()
                i += 1
            elif conditionstack[-1] == "(":
                if line[i] == '"':
                    conditionstack.append('"')
                elif line[i] == "'":
                    conditionstack.append("'")
                elif line[i] == "[":
                    conditionstack.append("[")
                elif line[i] == "{":
                    conditionstack.append("{")
                elif line[i] == "(":
                    conditionstack.append("(")
                elif line[i] == ")":
                    conditionstack.pop()
                i += 1
            elif conditionstack[-1] == "{":
                if line[i] == '"':
                    conditionstack.append('"')
                elif line[i] == "'":
                    conditionstack.append("'")
                elif line[i] == "[":
                    conditionstack.append("[")
                elif line[i] == "{":
                    conditionstack.append("{")
                elif line[i] == "(":
                    conditionstack.append("(")
                elif line[i] == "}":
                    conditionstack.pop()
                i += 1
    return argdict






if __name__ == "__main__":
    print(count("def f(a=\"(\"", (0, 0, None)))
    print(getargument(["def f(a =1) -> int:"]))
    print(getargument(["def f() -> int:"]))
    print(getargument(["def f(a, b_t) -> int:"]))
    print(getargument(["def f(a: int, b) -> int:"]))
    print(getargument(["def f(a = \"hello\", b)"]))
    print(getargument(["def f(a = (1, 2, 3), b = [4, 5, 6])"]))
    print(getargument(["def f(a = \"()))\")"]))
    print(getargument(["def f(a=10, ", "    b: int)"]))
    print(getargument(["    def __init__(self, varname='?', freqs=None):"]))
