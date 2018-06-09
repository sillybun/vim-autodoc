def f(a: Union[float, int], b: Union[float, int]=10) -> Union[float, int]:
    return a + b


class A:
    def f(self, a: int, b: int) -> int:
        return a + b

    def g(self, a: int, b: int) -> int:
        def f(a: int, b: int) -> int:
            return a + b
        return f(a, b)

def g(a: int, b: int) -> int:
    def f(a: int, b: int) -> int:
        return a + b
    return f(a, b)

addunit = A()
addunit.f(1, 2)
addunit.g(1, 2)

g(1, 2)
f(1, 2)
f(1.0, 2.0)
