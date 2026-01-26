import os  # unused

def add(a, b):
    return a + b

def main():
    x = 1
    y = 2
    print(add(x, y))
    print(unknown_var)  # noqa: F821

if __name__ == "__main__":
    main()
