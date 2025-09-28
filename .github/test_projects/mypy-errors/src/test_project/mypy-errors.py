"""Required docstring."""


def foo(x: int, y: int): # mypy error: Function is missing a return type annotation
    """Required docstring."""
    print("Hello, world!")
    return x + y


foo(1, 2)
