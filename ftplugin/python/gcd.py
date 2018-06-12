def main() -> None:
    """
    called number: 1
    total time: 0.00019097328186035156s
    """
    print(gcd(15, 10))
    print(gcd(45, 12))

def gcd(a: int, b: int) -> int:
    """
    called number: 2
    total time: 4.0531158447265625e-06s
    """
    while b:
        a, b = b, a%b
    return a

if __name__ == "__main__":
    main()
