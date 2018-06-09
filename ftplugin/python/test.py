from typing import Union

def f(a: Union[float, int], b: int) -> Union[float, int]:
    return a + b

def g(a: int, b: int) -> None:
    a += b

f(1, 2)
f(1.0, 2)
z = g(1, 2)
