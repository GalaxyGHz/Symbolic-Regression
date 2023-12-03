from expressions import functions, function_weights, evaluate_constants, write_expression
from random import choices, randint
import pandas as pd
import numpy as np

def sum_score(scores, Ys):
    try:
        scores = np.array(scores)
        if pd.isnull(scores).any():
            return float('inf')
        # if np.isinf(scores).any():
        #     return float('inf')
        if float('inf') in scores:
            return float('inf')
        return np.sum(np.abs(Ys - scores)/(np.abs(Ys)+1))
    except Exception as e:
        print("a")
        print(e)
        print(scores)
        print(scores.dtype)
        exit()     

def node_count(x):
    if "expressions" not in x:
        return 1
    return 1 + sum([node_count(c) for c in x["expressions"]])

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

    
# DFS to shorten constants
def dfs(expression): 
    children = 0 if "argument_count" not in expression else expression["argument_count"]
    
    if children == 0:
        return expression
    
    else:
        l_child = dfs(expression["expressions"][0])
        r_child = {"value": None} if children != 2 else dfs(expression["expressions"][1])
            
        expression["expressions"] = [l_child]
        if children == 2:
            expression["expressions"].append(r_child)
            
        if "value" not in l_child or "value" not in r_child:
            return expression
         
        if children == 1 and type(l_child["value"]) == int: # Unary functions
            val = evaluate_constants(expression)
            if type(val) == int:
                expression = {"value": val}
                
        elif children == 2 and type(l_child["value"]) == int and type(r_child["value"]) == int: # Binary functions
            val = evaluate_constants(expression)
            if type(val) == int:
                expression = {"value": val}
                
        return expression 

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