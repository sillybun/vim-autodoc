from typing import List, Callable, 

def testFun() -> List[Callable[..., Any]]:
    """
    called number: 1
    total time: 3.814697265625e-06s
    """
    temp = [lambda x : i*x for i in range(4)]
    return temp

for everyLambda in testFun():
    print(everyLambda(2))
