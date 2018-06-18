from typing import List, Callable, Any

def testFun() -> List[Callable[..., Any]]:
    """
    called number: 1
    total time: 4.0531158447265625e-06s
    """
    temp = [lambda x : i*x for i in range(4)]
    return temp

for everyLambda in testFun():
    print(everyLambda(2))
