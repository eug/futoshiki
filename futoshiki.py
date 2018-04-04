# -*- coding: utf-8 -*-
from copy import deepcopy
import sys
from constraint import Unary, Binary
from backtracking import bt, is_consistent
import operator
from random import shuffle
from itertools import product

class AssignmentDecoder:
    def __init__(self, d):
        self.d = d
        self.visited = []

    def decode(self, assignment):
        board = [0] * self.d
        for i in range(self.d):
            board[i] = [0] * self.d

        for k, v in assignment.items():
            i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1
            board[i][j] = v

        state = ''
        for row in board:
            for cell in row:
                state += str(cell) + ' '
                sys.stdout.write(str(cell) + ' ')
        
        if state in self.visited:
            print("REVISITING")
            sys.exit(1)
        else:
            self.visited.append(state)

        sys.stdout.write('\n')

def is_complete(assignment):
    return all(v != 0 for k, v in assignment.items())

class AssignmentManager:
    def __init__(self, assignment, domain, constraints):
        self.unassigned = {}
        for variable in assignment.keys():
            self.unassigned[variable] = domain

    def select(self, assignment, domain, constraints):
        for variable in self.unassigned.keys():
            if self.unassigned[variable]:
                return self.unassigned[variable].pop()

def select_unassigned_vars(assignment, domain, constraints):
    variables = []
    for k, v in assignment.items():
        if v == 0:
            variables.append(k)
    return variables

def look_ahead(assignment, domain, constraints):
    options = {}

    for variable, value in product(_assignment.keys(), domain):
        if variable not in options:
            options[variable] = []
        if is_consistent(assignment, domain, constraints, variable, value):
            options[variable].append(value)

    for variable, values in options.items():
        if not values:
            return []

    variables = []
    for k, v in assignment.items():
        if v == 0:
            variables.append(k)
    # shuffle(variables)
    return variables


def order_domain_values(assignment, domain, constraints, variable):
    return domain

if __name__ == '__main__':

    N = int(input())
    for n in range(N):

        D, R = map(int, input().split())

        domain = [d for d in range(1, D + 1)]

        constraints = []

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
            ai, aj, bi, bj = map(int, input().split())
            variable_1 = ai * 10 + aj
            variable_2 = bi * 10 + bj
            constraints.append(Binary(operator.lt, variable_1, variable_2))

        # atribuições iniciais
        assignment = {}
        for i in range(D):
            row = list(map(int, input().split()))
            for j in range(D):
                variable = (i + 1) * 10 + (j + 1)
                assignment[variable] = row[j]

                if row[j] > 0:
                    constraints.append(Unary(operator.eq, variable, row[j]))

        input() # EOF

        # print(domain)
        # print(assignment)
        # for c in constraints:
        #     print(c)

        result = bt(assignment, domain, constraints, is_complete, 
                    AssignmentManager(assignment, domain, constraints).select,
                    order_domain_values,
                    AssignmentDecoder(D).decode)

        print(n + 1)
        if result:
            decode_result(result, D)
        else:
            print('ERROR')
        break


