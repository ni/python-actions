"""Required docstring."""


def foo(x: int, y: int) -> int:
    """Required docstring."""
    print("Hello, world!")
    return x + y


# Definitive Pyright errors:
def broken_function(x: str) -> int:
    """This function has type errors."""
    return x  # Error: returning str when int expected


# Type mismatch
numbers: list[int] = [1, 2, "three"]  # Error: str in int list

# Wrong argument types
result = foo("not", "numbers")  # Error: str args to int params
