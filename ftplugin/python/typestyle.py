from ipdb import set_trace
from typing import List, Optional, Type, Dict



class ZYTType:

    def __init__(self) -> None:
        self.type: Optional[Type] = None
        self.any = False
        self.subtype: Optional[List[ZYTType]] = None
        self.basicflag = False
        self.repeatflag = False
        self.classname: Optional[str] = None

    BasicType = {
        "NoneType": type(None),
        "int": type(1),
        "float": type(1.0),
        "str": type("1"),
        "bool": type(True),
        "bytes": type(b"1"),
        "function": type(lambda x: x),
        "type": type(type(1))
    }
    CompondType = {
        "list": type(list()),
        "set": type(set()),
        "dict": type(dict()),
        "tuple": type(tuple())
    }
    BasicTypePEP484 = {
        "None": type(None),
        "int": type(1),
        "float": type(1.0),
        "str": type("1"),
        "bool": type(True),
        "bytes": type(b"1"),
        "Type": type(type(1)),
        "Callable": type(lambda x: x),
    }
    CompondTypePEP484 = {
        "List": type(list()),
        "Set": type(set()),
        "Dict": type(dict()),
        "Tuple": type(tuple()),
    }
    BasicPEP484: Dict[Type, str] = {
        type(None): "None",
        type(1): "int",
        type(1.0): "float",
        type("1"): "str",
        type(True): "bool",
        type(b"1"): "bytes",
        type(lambda x: x): "Callable[..., Any]",
        type(type(1)): "Type"
    }
    CompondPEP484: Dict[Type, str] = {
        type(list()): "List",
        type(set()): "Set",
        type(dict()): "Dict",
        type(tuple()): "Tuple"
    }

    def gettypename(self, sth):
        _type = type(sth)
        if isinstance(sth, list) and len(sth) > 0:
            return "list[" + self.gettypename(sth[0]) + "]"
        elif isinstance(sth, tuple) and len(sth) > 0:
            if len(sth) <= 5:
                return "tuple[" + ",".join(
                    [self.gettypename(sth[i]) for i in range(len(sth))]
                ) + "]"
            else:
                flag = True
                for i in range(1, len(sth)):
                    if self.gettypename(sth[i]) != self.gettypename(sth[0]):
                        flag = False
                        break
                if flag:
                    return "tuple[" + self.gettypename(sth[0]) + ",...]"
                else:
                    return "tuple[" + ",".join(
                        [self.gettypename(sth[i]) for i in range(5)]
                    ) + ",...]"
        elif isinstance(sth, set) and len(sth) > 0:
            return "set[" + self.gettypename(list(sth)[0]) + "]"
        elif isinstance(sth, dict) and len(sth) > 0:
            key = list(sth.keys())[0]
            return "dict[" + self.gettypename(key) +\
                    "," + self.gettypename(sth[key]) + "]"
        else:
            typestr = str(_type)
            return typestr[(typestr.find("'") + 1):typestr.rfind("'")]

    def fromvar(self, sth):
        self.fromAutoDoc(self.gettypename(sth))
        return self

    def fromdoc(self, typestr: str):
        self.fromAutoDoc(typestr)
        return self

    def fromAutoDoc(self, typestr: str) -> str:
        self.type = None
        self.subtype = None
        self.basicflag = False
        self.repeatflag = False
        self.classname = None
        self.any = False
        if typestr == "":
            return ""
        for bt in self.BasicType:
            if typestr.startswith(bt):
                self.type = self.BasicType[bt]
                self.basicflag = True
                return typestr[len(bt):]
        for ct in self.CompondType:
            if typestr.startswith(ct):
                self.type = self.CompondType[ct]
                typestr = typestr[len(ct):]
                if typestr.startswith("["):
                    temptype = ZYTType()
                    typestr = temptype.fromAutoDoc(typestr[1:])
                    self.subtype = [temptype]
                    while(typestr.startswith(",")):
                        if typestr.startswith(",..."):
                            self.repeatflag = True
                            typestr = typestr[4:]
                            break
                        temptype = ZYTType()
                        typestr = temptype.fromAutoDoc(typestr[1:])
                        self.subtype.append(temptype)
                    return typestr[1:]
                else:
                    return typestr
        if typestr.startswith("__main__."):
            typestr = typestr[9:]
        self.classname = ""
        for t in typestr:
            if t == "]" or t == ",":
                break
            self.classname += t
        return typestr[len(self.classname):]

    def fromPEP484(self, typestr: str) -> str:
        self.type = None
        self.subtype = None
        self.basicflag = False
        self.repeatflag = False
        self.classname = None
        self.any = False
        if " " in typestr:
            typestr = "".join([t for t in typestr if t != 0])
        if typestr == "":
            return ""
        if typestr.startswith("Any"):
            self.any = True
            return typestr[3:]
        for bt in self.BasicTypePEP484:
            if typestr.startswith(bt):
                self.type = self.BasicTypePEP484[bt]
                self.basicflag = True
                typestr = typestr[len(bt)]
                if bt == "Callable":
                    left = 1
                    for i in range(1, len(typestr)):
                        if typestr == "[":
                            left += 1
                        elif typestr == "]":
                            left -= 1
                        if left == 0:
                            typestr = typestr[i + 1]
                            return typestr
                return typestr
        for ct in self.CompondTypePEP484:
            if typestr.startswith(ct):
                self.type = self.CompondTypePEP484[ct]
                typestr = typestr[len(ct):]
                if typestr.startswith("["):
                    if typestr.startswith("[()]"):
                        return typestr[4:]
                    temptype = ZYTType()
                    typestr = temptype.fromPEP484(typestr[1:])
                    self.subtype = [temptype]
                    while(typestr.startswith(",")):
                        if typestr.startswith(",..."):
                            self.repeatflag = True
                            typestr = typestr[4:]
                            break
                        temptype = ZYTType()
                        typestr = temptype.fromPEP484(typestr[1:])
                        self.subtype.append(temptype)
                    return typestr[1:]
                else:
                    return typestr
        self.classname = ""
        for t in typestr:
            if t == "]" or t == ",":
                break
            self.classname += t
        return typestr[len(self.classname):]


    def subset(self, othertype) -> bool:
        if othertype.any:
            return True
        if self.type == othertype.type:
            if self.type is None:
                return self.classname == othertype.classname
            else:
                if self.basicflag:
                    return True
                else:
                    if self.type != type(tuple):
                        if othertype.subtype == None:
                            return True
                        elif self.subtype == None:
                            return False
                        elif len(self.subtype) != len(othertype.subtype):
                            return False
                        if self.repeatflag != othertype.repeatflag:
                            return False
                        for i in range(len(self.subtype)):
                            if not self.subtype[i].subset(othertype.subtype[i]):
                                return False
                        return True
                    else:
                        if othertype.subtype == None or self.subset == None:
                            return self.subset == None and self.subset == None
                        elif len(self.subtype) != len(othertype.subtype):
                            return False
                        if self.repeatflag != othertype.repeatflag:
                            return False
                        for i in range(len(self.subtype)):
                            if not self.subtype[i].subset(othertype.subtype[i]):
                                return False
                        return True
        return False

    def generatepep484(self) -> str:
        if self.basicflag:
            if self.type is not None:
                return self.BasicPEP484[self.type]
            else:
                return ""
        elif self.type is not None:
            rstr: str = self.CompondPEP484[self.type]
            if self.subtype is None:
                if self.type == type(tuple()):
                    return rstr + "[()]"
                else:
                    return rstr
            else:
                rstr += "["
                rstr += ", ".join(t.generatepep484() for t in self.subtype)
                if self.repeatflag:
                    rstr += ", ..."
                rstr += "]"
            return rstr
        elif self.classname is not None:
            return '"' + self.classname.split(".")[-1] + '"'
        else:
            return "Any"

    def autodoctopep484(self, doc: str) -> str:
        self.fromAutoDoc(doc)
        return self.generatepep484()

def unionpep484(types: List[ZYTType]) -> str:
    # print(list(t.generatepep484() for t in types))
    shorttypes = list()
    for i in range(len(types)):
        flag = True
        for j in range(len(types)):
            if j != i and types[j].subset(types[i]):
                if j > i or not types[i].subset(types[j]):
                    flag = False
                break
        if flag:
            shorttypes.append(types[i])
    if len(shorttypes) == 1:
        return shorttypes[0].generatepep484()
    else:
        return "Union[" + ", ".join(t.generatepep484() for t in shorttypes) + "]"


def main():
    type1 = ZYTType().fromvar(1)
    print(type1.generatepep484())
    type2 = ZYTType().fromvar(1.0)
    print(type2.generatepep484())
    print(unionpep484([type1, type2]))

if __name__ == "__main__":
    main()
