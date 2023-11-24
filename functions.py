import math

nan = float('nan')

def negative(a):
    return -a

def plus(a, b):
    return a + b

def minus(a, b):
    return a - b

def times(a, b):
    return a*b

def divide(a, b):
    return a/b if b else nan

def power(a, b):
    if a == 0 and b < 0:
        return nan
    if abs(b) > 20 or abs(a) > 1e3 or abs(a) < 1e-5:
        return nan
    try:
        result = a**b
        if isinstance(result, complex):
            return nan
        return result
    except:
        print(a, b)
        exit()

def sine(a):
    return math.sin(a)

def cosine(a):
    return math.cos(a)

def tangent(a):
    return math.tan(a)

def logarithm(b, a):
    if a > 0 and b > 0 and b != 1:
        return math.log(a, b)
    else:
        return nan
    
def sqrt(a):
    if a < 0:
        return nan
    return math.sqrt(a)

def modulo(a, b):
    if b == 0:
        return nan
    return a % b