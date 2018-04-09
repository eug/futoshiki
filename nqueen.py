import operator
import sys
from backtracking import Backtracking
from constraint import Binary, Unary
from heuristics import *
from time import time

def _parse_as_board(dimension, output):
    board = [0] * dimension
    for i in range(dimension):
        board[i] = [0] * dimension

    for k, v in assignment.items():
        i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1
        board[i][j] = v
    
    return board

def boardify_output(dimension, output):
    if not output:
        return " "

    s = ""
    for row in _parse_as_board(dimension, output):
        for cell in row:
            s += str(cell) + " "
        s += "\n"

    return s


def total_assignment(csp, assignment):
    return NQUEENS == len(assignment.keys())


def unique_assignment(csp, assignment):
    uniques = []

    for i in range(1, len(csp.variables)):
        rvalues = [v for v in csp.variables if v >= (i * 10) and v < ((i + 1) * 10) ]
        cvalues = [v for v in csp.variables if v % 10 == i]

        rsum = sum(v for v in rvalues)
        csum = sum(1 for v in cvalues)

        uniques.append(rsum > 0 and rsum == csum)

    return sum(uniques) == 1

def nqueens_selection(csp, assignment):
    candidates = []
    for var in csp.variables:
        if var not in assignment:
            for val in csp.domains[var]:
                if csp.is_consistent(assignment, var, val):
                    candidates.append(var)
    if candidates:
        return candidates[0]



# initialization
NQUEENS = 4
variables = []
domains = {}
constraints = []
assignment = {}

# encode board
for i in range(NQUEENS):
    for j in range(NQUEENS):
        variable = int(str(i+1) + str(j+1))
        variables.append(variable)
        domains[variable] = [1]

# create column constraints
for c in range(NQUEENS):
    min_var = 10 + (c + 1)
    max_var = 10 * (NQUEENS + 1)
    for variable_1 in range(min_var, max_var, 10):
        for variable_2 in range(variable_1, max_var, 10):
            if variable_1 != variable_2:
                constraints.append(Binary(operator.ne, variable_1, variable_2))

# create row constraints
for r in range(NQUEENS):
    min_var = (r + 1) * 10 + 1
    max_var = min_var + NQUEENS
    for variable_1 in range(min_var, max_var):
        for variable_2 in range(variable_1, max_var):
            if variable_1 != variable_2:
                constraints.append(Binary(operator.ne, variable_1, variable_2))

# create se-diagonal constraints
constraints.append(Binary(operator.ne, 31, 42))
constraints.append(Binary(operator.ne, 21, 32))
constraints.append(Binary(operator.ne, 21, 43))
constraints.append(Binary(operator.ne, 32, 43))
constraints.append(Binary(operator.ne, 11, 22))
constraints.append(Binary(operator.ne, 11, 33))
constraints.append(Binary(operator.ne, 11, 44))
constraints.append(Binary(operator.ne, 22, 33))
constraints.append(Binary(operator.ne, 22, 44))
constraints.append(Binary(operator.ne, 33, 44))
constraints.append(Binary(operator.ne, 12, 23))
constraints.append(Binary(operator.ne, 12, 34))
constraints.append(Binary(operator.ne, 23, 34))
constraints.append(Binary(operator.ne, 13, 24))



# create sw-diagonal constraints
constraints.append(Binary(operator.ne, 34, 43))
constraints.append(Binary(operator.ne, 24, 33))
constraints.append(Binary(operator.ne, 24, 42))
constraints.append(Binary(operator.ne, 33, 42))
constraints.append(Binary(operator.ne, 14, 23))
constraints.append(Binary(operator.ne, 14, 32))
constraints.append(Binary(operator.ne, 14, 41))
constraints.append(Binary(operator.ne, 23, 32))
constraints.append(Binary(operator.ne, 23, 41))
constraints.append(Binary(operator.ne, 32, 41))
constraints.append(Binary(operator.ne, 13, 22))
constraints.append(Binary(operator.ne, 13, 31))
constraints.append(Binary(operator.ne, 22, 31))
constraints.append(Binary(operator.ne, 12, 21))


# solve
bt = Backtracking(variables, domains, constraints)
bt.set_is_complete(total_assignment)
bt.set_variable_selection(nqueens_selection)
bt.set_value_selection(ordered_domain_values)
bt.set_look_ahead(no_inference)
start = time()
output = bt.solve(assignment)
t = time() - start
result = boardify_output(NQUEENS, output)
nassigns = bt.csp.nassigns

print(bt.solve(assignment))