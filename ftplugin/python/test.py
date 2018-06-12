from parameters import recordparametertype, logfunctionparameters, FUNCTION

@recordparametertype
def f(a: int):
    for i in range(a):
        yield i**3

for i in f(3):
    print(i)

print(FUNCTION)
