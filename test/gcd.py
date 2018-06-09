def main() -> None:
    """
    called number: 1
    total time: 8.606910705566406e-05s
    """
    print(gcd(15, 10))
    print(gcd(45, 12))

def gcd(a: int, b: int) -> int:
    """
    called number: 2
    total time: 1.6689300537109375e-06s
    """
    while b:
        a, b = b, a%b
    return a

if __name__ == "__main__":
    main()
