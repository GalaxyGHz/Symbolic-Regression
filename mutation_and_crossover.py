from expressions import create_expression, values, value_weights, functions
from random import randint, random, choices
from utils import sort_by_score, sample_valid_function, select_random_node
from copy import deepcopy

TOURNAMENT_SCALE = 0.4

# not used now
def tournament_selection(expressions):
    # randomly select population members for the tournament
    tournament_expressions = [
        expressions[randint(0, len(expressions) - 1)] for _ in range(int(len(expressions)*TOURNAMENT_SCALE))]
    # select tournament member with best fitness
    return sort_by_score(tournament_expressions)[0]

def crossover(expression1, expression2, crossover_rate):
    crossover_node1 = select_random_node(expression1)
    crossover_node2 = select_random_node(expression2)
    tmp = []
    for key in crossover_node1:
        tmp.append((key, crossover_node1[key]))
    crossover_node1.clear()
    for key in crossover_node2:
        crossover_node1[key] = crossover_node2[key]
    crossover_node2.clear()
    for item in tmp:
        crossover_node2[item[0]] = item[1]
    return [expression1, expression2]

def crossover_combo(expression1, expression2, crossover_rate):
    crossover_node1 = select_random_node(expression1) # Select two random nodes 
    crossover_node2 = select_random_node(expression2) # Select two random nodes
    # cn1_n_tmp = crossover_node1.copy()
    # cn2_n_tmp = crossover_node2.copy()
    cn1_tmp = deepcopy(crossover_node1)
    cn2_tmp = deepcopy(crossover_node2)
    connector_node = {
        "function": functions[1]["function"], # Plus function
        "argument_count": 2,
        "expressions": [cn1_tmp, cn2_tmp],
        "string": functions[1]["string"], # Plus function's string
    }
    crossover_node1.clear()
    crossover_node2.clear()
    
    crossover_node1.update(deepcopy(connector_node))
    crossover_node2.update(deepcopy(connector_node))
    
    return [expression1, expression2]

def mutate_change_subtree(expression):
    new_expression = create_expression(randint(1, 3))
    if "argument_count" in new_expression:
        expression.clear()
        expression["function"] = new_expression["function"]
        expression["argument_count"] = new_expression["argument_count"]
        expression["string"] = new_expression["string"]
        expression["expressions"] = new_expression["expressions"]
    else:
        expression.clear()
        expression["value"] = new_expression["value"]

def mutate_change_operator_or_value(expression):
    if "argument_count" not in expression:
        expression["value"] = choices(values, value_weights)[0]
    else:
        func = sample_valid_function(expression["argument_count"])
        expression["function"] = func["function"]
        expression["string"] = func["string"]

def mutate_prune_subtree(expression):
    if "argument_count" not in expression:
        expression["value"] = choices(values, value_weights)[0]
        return
    expression.clear()
    expression["value"] = choices(values, value_weights)[0]

mutation_types = ["flip", "subtree", "prune"]
def mutate(expression, mutation_rate, mutation_weights):
    if random() <= mutation_rate:
        mutation_type = choices(mutation_types, mutation_weights)[0]
        if mutation_type == "subtree":
            mutate_change_subtree(expression)
        elif mutation_type == "prune":
            mutate_prune_subtree(expression)
        elif mutation_type == "flip":
            mutate_change_operator_or_value(expression)
    if "argument_count" in expression:
        for child in expression["expressions"]:
            mutate(child, mutation_rate, mutation_weights)
    return expression