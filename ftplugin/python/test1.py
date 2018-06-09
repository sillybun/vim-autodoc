from typing import Union

def f(a: Union[float, int], b: int):
    return a + b

f(1, 2)
f(1.0, 2)
