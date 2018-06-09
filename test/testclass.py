from typing import Type
from numpy import ndarray

class A:
    def copy(self) -> "A":
        return self

    def get(self, a: "ndarray"):
        return a.shape

a = A()
a.get(np.zeros(10))
