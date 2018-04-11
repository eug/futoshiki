# -*- coding: utf-8 -*-
import operator
from random import shuffle
from time import time

from backtracking import Backtracking
from constraint import Binary, Unary
from heuristics import *

# Decodificação da Saida

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

def stringfy_output(dimension, output):
    if not output:
        return " "

    s = ""
    for row in _parse_as_board(dimension, output):
        for cell in row:
            s += str(cell) + " "

    return s


# Definição de completude

def total_assignment(csp, assignment):
    return len(csp.variables) == len(assignment.keys())


def read_file(filename):
    instances = []

    with open(filename, 'r') as f:

        N = int(f.readline())

        for n in range(N):

            variables = []
            domains = {}
            constraints = []
            assignment = {}
            D, R = map(int, f.readline().split())

            for i in range(D):
                for j in range(D):
                    variable = int(str(i + 1) + str(j + 1))
                    variables.append(variable)
                    domains[variable] = [d for d in range(1, D + 1)]

            # restrições de coluna do problema
            for c in range(D):
                min_var = 10 + (c + 1)
                max_var = 10 * (D + 1)
                for variable_1 in range(min_var, max_var, 10):
                    for variable_2 in range(variable_1, max_var, 10):
                        if variable_1 != variable_2:
                            constraints.append(Binary(operator.ne, variable_1, variable_2))
            
            # restrições de linha do problema
            for r in range(D):
                min_var = (r + 1) * 10 + 1
                max_var = min_var + D
                for variable_1 in range(min_var, max_var):
                    for variable_2 in range(variable_1, max_var):
                        if variable_1 != variable_2:
                            constraints.append(Binary(operator.ne, variable_1, variable_2))

            # restrições da instancia
            for i in range(R):
                ai, aj, bi, bj = map(int, f.readline().split())
                variable_1 = ai * 10 + aj
                variable_2 = bi * 10 + bj
                constraints.append(Binary(operator.lt, variable_1, variable_2))

            # atribuições iniciais
            for i in range(D):
                row = list(map(int, f.readline().split()))
                for j in range(D):
                    variable = (i + 1) * 10 + (j + 1)
                    if row[j] > 0:
                        assignment[variable] = row[j]
                        constraints.append(Unary(operator.eq, variable, row[j]))

            f.readline() # EOF
    
            instances.append((variables, domains, constraints, assignment, D, r, n))

        return instances

if __name__ == '__main__':
    instances = read_file('futoshiki_all.txt')

    for variables, domains, constraints, assignment, D, r, n in instances:
        try:
            bt = Backtracking(variables, domains, constraints, 1000000)
            bt.set_is_complete(total_assignment)
            bt.set_variable_selection(mrv_d)
            bt.set_value_selection(lcv)
            bt.set_look_ahead(forward_checking)
            start = time()
            output = bt.solve(assignment)
            t = time() - start
            result = stringfy_output(D, output)
            nassigns = bt.csp.nassigns
        except KeyboardInterrupt:
            nassigns = ' '
            result = ' '

        print ("{},{},{},{},{:.2f},{}".format(n + 1, D, r, nassigns, t, result))
