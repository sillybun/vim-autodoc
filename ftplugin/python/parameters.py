import json
import time
from functools import wraps
import types
import itertools
from typing import Dict


FUNCTION: Dict[str, Dict] = dict()

def gettypename(sth):
    _type = type(sth)
    if isinstance(sth, list) and len(sth) > 0:
        return "list[" + gettypename(sth[0]) + "]"
    elif isinstance(sth, tuple) and len(sth) > 0:
        if len(sth) <= 5:
            return "tuple[" + ",".join(
                [gettypename(sth[i]) for i in range(len(sth))]
            ) + "]"
        else:
            flag = True
            for i in range(1, len(sth)):
                if gettypename(sth[i]) != gettypename(sth[0]):
                    flag = False
                    break
            if flag:
                return "tuple[" + gettypename(sth[0]) + ",...]"
            else:
                return "tuple[" + ",".join(
                    [gettypename(sth[i]) for i in range(5)]
                ) + ",...]"
    elif isinstance(sth, set) and len(sth) > 0:
        return "set[" + gettypename(list(sth)[0]) + "]"
    elif isinstance(sth, dict) and len(sth) > 0:
        try:
            key = list(sth.keys())[0]
            return "dict[" + gettypename(key) +\
                    "," + gettypename(sth[key]) + "]"
        except IndexError:
            return "dict"
    elif isinstance(sth, types.GeneratorType):
        return "generator"
    elif isinstance(sth, range):
        return "range"
    else:
        typestr = str(_type)
        return typestr[(typestr.find("'") + 1):typestr.rfind("'")]

def recordparametertype(func):


    global FUNCTION

    @wraps(func)
    def wrapper(*args, **kwargs):
        if func.__qualname__ not in FUNCTION:
            FUNCTION[func.__qualname__] = dict()
            FUNCTION[func.__qualname__]["parameters"] = dict()
            FUNCTION[func.__qualname__]["analysis"] = dict()
            for i, arg in enumerate(args):
                FUNCTION[func.__qualname__]["parameters"][i] = set(
                    [gettypename(arg)]
                )
            FUNCTION[func.__qualname__]["return"] = set()
            FUNCTION[func.__qualname__]["analysis"]["callnumber"] = 1
            FUNCTION[func.__qualname__]["analysis"]["collapsetime"] = 0
        else:
            for i, arg in enumerate(args):
                FUNCTION[func.__qualname__]["parameters"][i].add(
                    gettypename(arg)
                )
            FUNCTION[func.__qualname__]["analysis"]["callnumber"] += 1
        starttime = time.time()
        result = func(*args, **kwargs)
        endtime = time.time()
        FUNCTION[func.__qualname__]["analysis"]["collapsetime"
                                                ] += endtime - starttime
        FUNCTION[func.__qualname__]["return"].add(gettypename(result))
        return result

    return wrapper


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return sorted(list(obj))
        return json.JSONEncoder.default(self, obj)


def logfunctionparameters():
    logfile = open(".autodocparameters.log", "w")
    logfile.write(json.dumps(FUNCTION, cls=SetEncoder))


if __name__ == "__main__":

    class A:

        @recordparametertype
        def f(self, a, b):
            return a + b

    a = A()
    a.f(1, 2)
    a.f(1, 2.0)

    @recordparametertype
    def g(b):
        return

    g(range(10))
    g([1, 2, 3])
    print(FUNCTION)
