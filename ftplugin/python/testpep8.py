from typing import Iterable, List, Iterator

def f(a: Iterable[int]) -> None:
    for i in a:
        print(i)

f(range(3))
