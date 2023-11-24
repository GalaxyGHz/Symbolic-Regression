import pandas as pd
from symbolic_regression import symbolic_regression
from expressions import write_expression


dataset = pd.read_csv('dataset.csv', sep=',')

for x in dataset.iterrows():
    print()

    Xs = [float(g) for g in x[1]["Xs"].strip('][').split(', ')]
    Ys = [float(g) for g in x[1]["Ys"].strip('][').split(', ')]

    # MUTATION WEIGHTS are the list passed to symbolic regression, the first item represents the probability of the mutation being a value or function cahnge,
    # the second values is the probability of a subtree change, and the third value is the probability of a subtree prune (delete subtree)
    best = symbolic_regression(100, 600, 5, Xs, Ys, [100, 200, 200, 100], 0.01, [1, 1, 1], 0.2)
    print("Target expression:", x[1]["Equation"], "| Our Expression:", write_expression(best), "with score:", str(best["score"]), "(lower is better)")
    # vrednost 9223372036854775807 pomeni da je prislo do napake v racunanju, kot npr deljenje z 0, ali potenciranje prevelikega stevila in overflow

   