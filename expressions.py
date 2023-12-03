from functions import *
from random import randint, choices

values = [*range(1, 10), "x"]
value_weights = [*([1]*9), 4]

functions = [
    {"function": negative, "argument_count": 1, "string": "-{}"},
    {"function": plus, "argument_count": 2, "string": "({} + {})"},
    {"function": minus, "argument_count": 2, "string": "({} - {})"},
    {"function": times, "argument_count": 2, "string": "{} * {}"},
    {"function": divide, "argument_count": 2, "string": "({}) / ({})"},
    {"function": power, "argument_count": 2, "string": "{}^{}"},
    {"function": sine, "argument_count": 1, "string": "sin({})"},
    {"function": cosine, "argument_count": 1, "string": "cos({})"},
    {"function": tangent, "argument_count": 1, "string": "tan({})"},
    {"function": logarithm, "argument_count": 2, "string": "log_{}({})"},
    {"function": sqrt, "argument_count": 1, "string": "sqrt({})"},
    {"function": modulo, "argument_count": 2, "string": "({}) % ({})"}
]
function_weights = [50, 50, 50, 30, 30, 25, 1, 1, 1, 1, 1, 1]

def write_expression(node):
    if "expressions" not in node:
        return node["value"]
    return node["string"].format(*[write_expression(c) for c in node["expressions"]])

def evaluate_expression(node, x):
    if "expressions" not in node:
        return x if node["value"] == "x" else node["value"]
    return node["function"](*[evaluate_expression(c, x) for c in node["expressions"]])

def evaluate_constants(node):
    if "expressions" not in node:
        return node["value"]
    return node["function"](*[evaluate_constants(c) for c in node["expressions"]])

def create_expression(depth):
    # Ramped half and half
    if randint(0, 1):
        return grow(depth)
    else:
        return full(depth)

def grow(depth):
    if depth == 1 or randint(0, 2) == 0:
        return {"value": choices(values, value_weights)[0]}
    else:
        func = choices(functions, function_weights)[0]
        return {
            "function": func["function"],
            "argument_count": func["argument_count"],
            "expressions": [grow(depth - 1) for _ in range(func["argument_count"])],
            "string": func["string"],
        }

def full(depth):
    if depth == 1:
        return {"value": choices(values, value_weights)[0]}
    else:
        func = choices(functions, function_weights)[0]
        return {
            "function": func["function"],
            "argument_count": func["argument_count"],
            "expressions": [full(depth - 1) for _ in range(func["argument_count"])],
            "string": func["string"],
        }
