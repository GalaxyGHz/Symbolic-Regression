import pandas as pd
from expressions import create_expression, evaluate_expression, function_weights
import numpy as np
import sys
from mutation_and_crossover import sort_by_score, mutate, crossover, crossover_combo
from random import randint, choices
from copy import deepcopy
from utils import node_count, sum_score, dfs
from expressions import write_expression
import math

crossovers = [
    {"function": crossover_combo},
    {"function": crossover}, 
]

def calculate_score(samples, Xs, Ys, score_function):
    for sample in samples:
        scores = []
        for x in Xs:
            scores.append(evaluate_expression(sample, x))
        if Ys[-1] > 1e+10: # Adaptive power chance
            function_weights[5] = 100
        else:
            function_weights[5] = 25
        penalty = 1 + math.exp(node_count(sample) - 15) # Exponential function where up to around 10 nodes have about the same penalty
        sample["score"] = score_function(scores, Ys)*penalty
        if np.isnan(sample["score"]):
            sample["score"] = float("inf")

# proportion is an array with the proportions of expression types of the new population
# Expression types are as follows, by index:
# Index 0: best propotion[0] expressions from the last population
# Index 1: proportion[1] expressions, created by mutating some expression from the best expression list
# Index 2: proportion[2] expressions, created by crossover-ing two expressions from  the best expression list
# proportion[2] should be even, since we add both expressions created by crossover 
# Index 3: proportion[3] number of newly created random expressions added to the population
#
# The proportion array should sum to the population_size variable
# population argument should be sorted
def create_new_population_by_proportion(population_size, population, proportions, mutation_rate, mutation_weights, crossover_rate):
    new_population = []
    proportions = np.round(population_size*(proportions/np.sum(proportions))).astype(np.int32)

    for i in range(proportions[0]):
        new_population.append(population[i])

    for i in range(proportions[1]):
        expression_to_mutate = randint(0, proportions[0])
        new_population.append(mutate(deepcopy(population[expression_to_mutate]), mutation_rate, mutation_weights))
    
    for i in range(proportions[2]//2):
        expressions_to_crossover1 = randint(0, proportions[0])
        expressions_to_crossover2 = randint(0, proportions[0])
        # crossover returns two newly created expressions
        crossover_weights = [50, 50]
        crossover_function = choices(crossovers, crossover_weights)[0]
        new_expressions = crossover_function["function"](deepcopy(population[expressions_to_crossover1]), deepcopy(population[expressions_to_crossover2]), crossover_rate)
        new_population.append(new_expressions[0]) 
        new_population.append(new_expressions[1])

    for i in range(proportions[3]):
        # could also experiment with changing these values for project report
        new_population.append(create_expression(randint(1, 4))) 

    return new_population

def symbolic_regression(number_of_generations, population_size, expression_depth, Xs, Ys, population_change_proportions, mutation_rate, mutation_weights, crossover_rate):

    expressions = [create_expression(expression_depth) for _ in range(population_size)]
    for generation in range(number_of_generations):
        expressions = [dfs(expression) for expression in expressions]
        
        # print("\r" + str(round(generation/number_of_generations*100, 2)) + "%", end="")
        calculate_score(expressions, Xs, Ys, sum_score)
        
        expressions = sort_by_score(expressions)
        
        if expressions[0]["score"] == 0 or generation == number_of_generations - 1:
            # print("\r    \r", end="")
            return expressions[0]
        
        expressions = create_new_population_by_proportion(population_size, expressions, population_change_proportions, mutation_rate, mutation_weights, crossover_rate)
    # never get here
        
