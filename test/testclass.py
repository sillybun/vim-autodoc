from typing import Type
import numpy as np

class A:
    def copy(self) -> "A":
        return self

    def f(self, a: int, b: int) -> int:
        """
        called number: 1
        total time: 1.1920928955078125e-06s
        """
        return a + b


a = A()
a.f(1, 2)
