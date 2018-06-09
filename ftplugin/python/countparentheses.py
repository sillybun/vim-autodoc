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
    """
    @type lines: list[str]
    """
    args = ""
    conditionstack = list()
    for line in lines:
        i = 0
        while i < len(line):
            if len(conditionstack) == 0:
                if line[i] == "(":
                    conditionstack.append("()")
                i += 1
            elif conditionstack[-1] == "()":
                if line[i].isalpha():
                    conditionstack.append("arg")
                elif line[i] == "=":
                    conditionstack.append("=")
                    i += 1
                elif line[i] == ",":
                    args += ","
                    i += 1
                elif line[i] == ")":
                    conditionstack.pop()
                    break
                else:
                    i += 1
            elif conditionstack[-1] == "arg":
                if line[i].isalpha():
                    args += line[i]
                    i += 1
                elif line[i] == "=" or line[i] == " " or line[i] == "," or line[i] == ")":
                    conditionstack.pop()
                elif line[i] == ":":
                    conditionstack.append(":")
                    i += 1
                else:
                    i += 1
            elif conditionstack[-1] == ":":
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
                elif line[i] == ",":
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
                elif line[i] == ",":
                    conditionstack.pop()
                    continue
                i += 1
            elif conditionstack[-1] == '"' or conditionstack[-1] == "'":
                if line[i] == '"':
                    conditionstack.pop()
                    i += 1
                elif line[i] == "\\":
                    i += 2
                else:
                    i += 1
            elif conditionstack[-1] == "[":
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
    return args






if __name__ == "__main__":
    print(count("def f(a=\"(\"", (0, 0, None)))
    print(getargument(["def f(a: int, b)"]))
    print(getargument(["def f(a = \"hello\", b)"]))
    print(getargument(["def f(a = (1, 2, 3), b = [4, 5, 6])"]))
    print(getargument(["def f(a = \"()))\")"]))
    print(getargument(["def f(a=10, ", "    b: int)"]))
