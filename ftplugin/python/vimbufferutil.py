from typing import List, Set

import countparentheses


class AddBufferContent:

    def __init__(self):
        self.adddict = dict()
        self.removeset: Set[int] = set()

    def addandwait(self, content: str, linenumber: int):
        if linenumber in self.adddict:
            self.adddict[linenumber].append(content)
        else:
            self.adddict[linenumber] = [content]

    def removeandwait(self, linenumber: int):
        self.removeset.add(linenumber)

    def remove(self, buffer, linenumber: int):
        del buffer[linenumber - 1]

    def add(self, buffer, content: str, linenumber: int):
        buffer.append(content, linenumber)

    def conduct(self, buffer):
        alreadyadd = 0
        alreadyremove = 0
        for i in sorted(set(self.adddict.keys()).union(self.removeset)):
            if i in self.removeset:
                self.remove(buffer, i + alreadyadd - alreadyremove)
                alreadyremove += 1
            if i in self.adddict:
                for content in self.adddict[i]:
                    self.add(buffer, content, i + alreadyadd - alreadyremove)
                    alreadyadd += 1
        self.removeset = set()
        self.adddict = dict()


class FunctionCode:

    def __init__(self) -> None:
        return

    def regist(self, buffer, startline: int) -> None:
        self.startline = startline
        self.endline = self.startline
        self.functiondefstatement: List[str] = list()
        self.containdocstring = False
        tline: str = buffer[startline]
        textra = tline.lstrip()
        self.functionname = textra[4: textra.find('(')]
        self.indentlevel = (len(tline) - len(textra)) // 4
        if self.indentlevel != 0:
            indentlevel = self.indentlevel
            for i in range(self.startline - 1, -1, -1):
                cline: str = buffer[i]
                if len(cline.strip()) == 0:
                    continue
                cextra: str = cline.lstrip()
                cindentlevel = (len(cline) - len(cextra)) // 4
                if cindentlevel == indentlevel - 1:
                    if cextra.startswith("def "):
                        addname = cextra[4: cextra.find('(')]
                        self.functionname = addname + ".<locals>." + self.functionname
                    elif cextra.startswith("class "):
                        addname = cextra[6: cextra.find("(")]
                        self.functionname = addname + "." + self.functionname
                    indentlevel -= 1
                if indentlevel == 0:
                    break
        prev = (0, 0, None)
        while True:
            prev = countparentheses.count(buffer[self.endline], prev)
            self.functiondefstatement.append(buffer[self.endline])
            if prev[0] != prev[1]:
                self.endline += 1
            else:
                break
        self.functionargs = countparentheses.getargument(self.functiondefstatement).split(",")
        if self.endline < len(buffer) - 1 and\
                buffer[self.endline + 1].strip().startswith('"""'):
            self.containdocstring = True
            self.docstartline = self.endline + 1
            if '"""' in buffer[self.docstartline].lstrip()[3:]:
                self.docendline = self.docstartline
            else:
                self.docendline = self.docstartline + 1
                while self.docendline < len(buffer) - 1 and '"""' not in buffer[
                    self.docendline
                ]:
                    self.docendline += 1
            self.docstring: List[str] = list()
            if len(buffer[self.docstartline].strip()) > 3:
                tline = buffer[self.docstartline].strip()
                if self.docendline == self.docstartline:
                    if len(tline) > 6:
                        self.docstring.append(
                            tline[(tline.find('"""') + 3):tline.rfind('"""')]
                        )
                else:
                    self.docstring.append(tline[(tline.find('"""') + 3):])
            if self.docendline > self.docstartline:
                for row in range(self.docstartline + 1, self.docendline):
                    self.docstring.append(
                        buffer[row][4 * (self.indentlevel + 1):]
                    )
                if buffer[self.docendline].strip() != '"""':
                    self.docstring.append(
                        buffer[self.docendline][4 * (
                            self.indentlevel + 1
                        ):buffer[self.docendline].rfind('"""')]
                    )


class AllFunctions:
    def __init__(self):
        self.functions = list()

    def regist(self, buffer):
        for row, line in enumerate(buffer):
            extra = line.lstrip()
            if extra.startswith("def ") and row < len(buffer) - 1:
                fc = FunctionCode()
                fc.regist(buffer, row)
                self.functions.append(fc)
