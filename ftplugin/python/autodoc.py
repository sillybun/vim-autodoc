import json
from typing import Dict, Optional, Set

import vimbufferutil


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
                for index, param in enumerate(fc.functionargs):
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


def addpep484hint(buffer) -> None:
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



def main() -> None:
    fa = FunctionAna()
    fa.readfromfile("testlog.log")
    print(fa.FUNCTION)


if __name__ == "__main__":
    main()
