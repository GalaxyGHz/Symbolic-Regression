from expressions import functions, function_weights
from random import choices, randint
import numpy as np

def sum_score(scores, Ys):
    return np.sum(np.abs(Ys - np.array(scores)))

def node_count(x):
    if "expressions" not in x:
        return 1
    return sum([node_count(c) for c in x["expressions"]])

def sort_by_score(expressions):
    return sorted(expressions, key=lambda x: x["score"], reverse=False)

def sample_valid_function(argument_count):
    func = choices(functions, function_weights)[0]
    while func["argument_count"] != argument_count:
        func = choices(functions, function_weights)[0]
    return func

# one version
def select_random_node(expression):
    #It favors nodes closer to root
    children = 0 if "argument_count" not in expression else expression["argument_count"]
    selected = randint(0, children)
    if selected == 0:
        return expression
    else:
        return select_random_node(expression["expressions"][selected - 1])

# # second version
# def select_random_node(expression):
#     expressions = []
#     checking = [expression]

#     while checking:
#         expression = checking.pop()
#         expressions.append(expression)
#         if "expressions" in expression:
#             for exp in expression["expressions"]:
#                 checking.append(exp)
            
#     node = choice(expressions)
#     # left_or_right = random.choice(["left", "right"])
#     return node