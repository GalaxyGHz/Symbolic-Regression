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
    if abs(b) > 100 or abs(a) > 1e3 or abs(a) < 1e-4:
        return nan
    try:
        result = a**b
        if isinstance(result, complex):
            return nan
        return result
    except:
        return nan
        print(a, b)
        exit()

def sine(a):
    try:
        result = math.sin(a)
        return result
    except:
        # print("Sin", a)
        return nan

def cosine(a):
    try:
        result = math.cos(a)
        return result
    except:
        # print("Cos", a)
        return nan

def tangent(a):
    try:
        result = math.tan(a)
        return result
    except:
        # print("Tan", a)
        return nan

def logarithm(b, a):
    if a > 0 and b > 0 and b != 1:
        try:
            result = math.log(a,b)
            return result
        except:
            # print("Log", a, b)
            return nan
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