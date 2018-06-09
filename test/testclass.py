from typing import Type
import numpy as np

class A:
    def copy(self) -> "A":
        return self

a = A()
