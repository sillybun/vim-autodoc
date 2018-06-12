from typing import Union, List, Dict, Set

def f(a: Union[float, int]) -> Union[float, int]:
    return a + 1

def g(a: Union[Dict, List, Set]) -> int:
    return len(a)

f(1)
f(2.0)
g(list())
g(set())
g(dict())
