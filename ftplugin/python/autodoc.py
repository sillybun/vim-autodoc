import json
from typing import Dict, Optional, Set

import vimbufferutil
import typestyle
import time
import re

debug = False

class FunctionAna:

    def __init__(self, path: Optional[str] = None) -> None:
        if path is None:
            return
        else:
            self.readfromfile(path)

    def readfromfile(self, path: str) -> None:
        with open(path) as file:
            self.FUNCTION: Dict[str, Dict] = json.loads(file.read())

    def getparamtype(self, func: str, parnum: int) -> list:
        return self.FUNCTION[func]["parameters"][parnum]

    def getparamnumber(self, func: str) -> int:
        return len(self.FUNCTION[func]["parameters"])

    def getreturntype(self, func: str) -> list:
        return self.FUNCTION[func]["return"]

    def getcallnumber(self, func: str) -> int:
        return self.FUNCTION[func]["analysis"]["callnumber"]

    def getcollapsetime(self, func: str) -> float:
        return self.FUNCTION[func]["analysis"]["collapse"]


def adddocstring_paramtype(
    buffer, returnflag=False, doctype: str = "Epydoc"
) -> None:
    functionlog = FunctionAna(".autodocparameters.log")

    functioncode = vimbufferutil.AllFunctions()
    functioncode.regist(buffer)

    abc = vimbufferutil.AddBufferContent()
    for func in functionlog.FUNCTION:
        funcdict = functionlog.FUNCTION[func]
        for _fc in functioncode.functions:
            fc: vimbufferutil.FunctionCode = _fc
            if fc.functionname == func:
                tfc: vimbufferutil.FunctionCode = fc
                commentspace = " " * (4 * (fc.indentlevel + 1))
                abc.addandwait(commentspace + '"""', fc.endline + 1)
                for index in fc.functionargsdict:
                    param = fc.functionargsdict[index]["arg"]
                    if str(index) in funcdict["parameters"]:
                        abc.addandwait(
                            commentspace + "@type " + param + ": " +
                            ", ".join(funcdict["parameters"][str(index)]),
                            fc.endline + 1
                        )
                if returnflag:
                    abc.addandwait(
                        commentspace + "@rtype: " +
                        ", ".join(funcdict["return"]), fc.endline + 1
                    )
                if tfc.containdocstring:
                    for i in range(tfc.docstartline, tfc.docendline + 1):
                        abc.removeandwait(i + 1)
                    for docline in tfc.docstring:
                        if "@type" not in docline and "@rtype" not in docline:
                            abc.addandwait(
                                commentspace + docline, fc.endline + 1
                            )
                abc.addandwait(commentspace + '"""', fc.endline + 1)
    abc.conduct(buffer)


def adddocstring_runtime_info(buffer) -> None:
    functionlog = FunctionAna(".autodocparameters.log")

    functioncode = vimbufferutil.AllFunctions()
    functioncode.regist(buffer)

    abc = vimbufferutil.AddBufferContent()
    for func in functionlog.FUNCTION:
        funcdict = functionlog.FUNCTION[func]
        for _fc in functioncode.functions:
            fc: vimbufferutil.FunctionCode = _fc
            if fc.functionname == func:
                tfc: vimbufferutil.FunctionCode = fc
                commentspace = " " * (4 * (fc.indentlevel + 1))
                abc.addandwait(commentspace + '"""', tfc.endline + 1)
                if tfc.containdocstring:
                    for i in range(tfc.docstartline, tfc.docendline + 1):
                        abc.removeandwait(i + 1)
                    for docline in tfc.docstring:
                        if "called number: " not in docline and "total time: " not in docline:
                            abc.addandwait(
                                commentspace + docline, fc.endline + 1
                            )
                abc.addandwait(
                    commentspace + "called number: " +
                    str(funcdict["analysis"]["callnumber"]),
                    tfc.endline + 1
                )
                abc.addandwait(
                    commentspace + "total time: " +
                    str(funcdict["analysis"]["collapsetime"]) + "s",
                    tfc.endline + 1
                )
                abc.addandwait(commentspace + '"""', tfc.endline + 1)
    abc.conduct(buffer)


def addpep484hint(buffer, returnflag) -> None:
    # starttime = time.time()
    logfile = FunctionAna(".autodocparameters.log")

    functioncode = vimbufferutil.AllFunctions()
    functioncode.regist(buffer)

    styledecoder = typestyle.ZYTType()

    abc = vimbufferutil.AddBufferContent()

    importset: Set[str] = set()

    if debug:
        print(logfile.FUNCTION)
        print([t.functionname for t in functioncode.functions])
    for loggedfunc in logfile.FUNCTION:
        loggedfuncinfo = logfile.FUNCTION[loggedfunc]
        for _fc in functioncode.functions:
            fc: vimbufferutil.FunctionCode = _fc
            if fc.functionname == loggedfunc:
                tfc: vimbufferutil.FunctionCode = fc
                # if -1 not in tfc.functionargsdict:
                #     print(tfc.functiondefstatement)
                methodflag = False
                if "." in loggedfunc and\
                        loggedfunc.split(".")[-2] != "<locals>":
                    methodflag = True
                if debug:
                    print(tfc.functionargsdict)
                    print(loggedfuncinfo)
                for index in sorted(tfc.functionargsdict):
                    if methodflag and index == 0:
                        continue
                    if index == -1:
                        continue
                    arginfo = tfc.functionargsdict[index]
                    argpos = arginfo["pos"]
                    if str(index) in loggedfuncinfo["parameters"]:
                        if "type" in tfc.functionargsdict[index]:
                            continue
                        print(loggedfuncinfo["parameters"][str(index)])
                        types = [typestyle.ZYTType().fromdoc(adtype)
                                 for adtype in loggedfuncinfo["parameters"][str(index)]]
                        for t in types:
                            importset = importset.union(t.getpep484import())
                        if len(types) == 1:
                            abc.insertandwait(": " + types[0].generatepep484(), tfc.startline +
                                              argpos[0] + 1, argpos[1] + len(arginfo["arg"]))
                        else:
                            tline = typestyle.unionpep484(types)
                            abc.insertandwait(": " + tline, tfc.startline +
                                              argpos[0] + 1, argpos[1] + len(arginfo["arg"]))
                            if "Optional" in tline:
                                importset.add("Optional")
                            importset.add("Union")
                if returnflag and "type" not in tfc.functionargsdict[-1]:
                    types = [typestyle.ZYTType().fromdoc(adtype)
                             for adtype in loggedfuncinfo["return"]]
                    for t in types:
                        importset = importset.union(t.getpep484import())
                    arginfo = tfc.functionargsdict[-1]
                    argpos = arginfo["pos"]
                    if len(types) == 1:
                        abc.insertandwait(" -> " + types[0].generatepep484(), tfc.startline +
                                          argpos[0] + 1, argpos[1] + 1)
                    else:
                        abc.insertandwait(" -> " + typestyle.unionpep484(types), tfc.startline +
                                          argpos[0] + 1, argpos[1] + 1)


    start = 0
    peek = 0

    while True:
        if buffer[peek].startswith("#"):
            peek += 1
        elif buffer[peek].startswith(" "):
            peek += 1
        elif buffer[peek].startswith("from"):
            start = peek + 1
            peek += 1
        elif buffer[peek].startswith("import"):
            start = peek + 1
            peek += 1
        else:
            break

    for i in range(0, start):
        if buffer[i].startswith("from typing import"):
            extra = buffer[i][19:]
            print(extra)
            extra = re.sub("\s", "", extra)
            already = set(extra.split(","))
            importset = importset - already
            print(already)
            print(importset)
            abc.insertandwait(", " + ", ".join(list(importset)), i+1, len(buffer[i]))
            importset = set()
            break
    if len(importset) != 0:
        abc.addandwait("from typing import " + ", ".join(list(importset)), start)
        abc.addandwait("", start)

    abc.conduct(buffer)
    # endtime = time.time()
    # print(endtime - starttime)

def main() -> None:
    fa = FunctionAna()
    fa.readfromfile("testlog.log")
    print(fa.FUNCTION)


if __name__ == "__main__":
    main()

