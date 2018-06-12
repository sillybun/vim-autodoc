def main() -> None:
    print(gcd(15, 10))
    print(gcd(45, 12))

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a%b
    return a

if __name__ == "__main__":
    main()
