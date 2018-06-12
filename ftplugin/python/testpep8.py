from typing import Iterable, List, Iterator

def f(a: Iterable[int]) -> str:
    for i in a:
        print(i)
    return "str"

b: Iterable[int] = [1, 2, 3]
b[f(range(3))]
