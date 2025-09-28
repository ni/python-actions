import os, sys  # Multiple imports on one line (E401)

def foo( x: int , y: int ) -> int:  # Spaces around parameters (E211, E251)
    print( "Hello, world!" )  # Unnecessary spaces inside parentheses (E201, E202)
    return x+y  # Missing whitespace around operator (E225)

foo(1,2)