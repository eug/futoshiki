# -*- coding: utf-8 -*-
from copy import deepcopy
import sys
from constraint import Unary, Binary
from backtracking import backtracking, CSP
import operator
from random import shuffle
from itertools import product

class LinearAssignmentDecoder:
    def __init__(self, d):
        self.d = d

    def decode(self, assignment):
        board = [0] * self.d
        for i in range(self.d):
            board[i] = [0] * self.d

        for k, v in assignment.items():
            i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1
            board[i][j] = v

        for row in board:
            for cell in row:
                sys.stdout.write(str(cell) + ' ')
        sys.stdout.write('\n')


class BoardAssignmentDecoder:
    def __init__(self, d):
        self.d = d

    def decode(self, assignment):
        board = [0] * self.d
        for i in range(self.d):
            board[i] = [0] * self.d

        for k, v in assignment.items():
            i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1
            board[i][j] = v

        for row in board:
            for cell in row:
                sys.stdout.write(str(cell) + ' ')
            sys.stdout.write('\n')
        sys.stdout.write('\n')


class AssignmentManager:
    def __init__(self, assignment, domain, constraints):
        self.unassigned = {}
        for variable in assignment.keys():
            self.unassigned[variable] = domain

    def select(self, assignment, domain, constraints):
        for variable in self.unassigned.keys():
            if self.unassigned[variable]:
                return self.unassigned[variable].pop()


def look_ahead(assignment, domain, constraints):
    options = {}

    for variable, value in product(assignment.keys(), domain):
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







def is_complete(csp, assignment):
    return len(csp.variables) and len(assignment.keys())

def first_unassigned_var(csp, assignment):
    for k, v in assignment.items():
        if v == 0:
            return k

def ordered_domain_values(csp, assignment, variable):
    return cps.domains[variable]

def unordered_domain_values(csp, assignment, variable):
    shuffle(cps.domains[variable])

def no_inference(self):
    return True




if __name__ == '__main__':

    
    variables = []
    domains = {}
    constraints = []
    assignment = {}

    with open('test_0.txt', 'r') as f:
    # with open(sys.argv[-1], 'r') as f:
        N = int(f.readline())
        for n in range(N):
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
            
            decoder = LinearAssignmentDecoder(D)
            
            csp = CSP(variables, domains, constraints)
            result = backtracking(csp, assignment,
                                  is_complete,
                                  first_unassigned_var,
                                  ordered_domain_values,
                                  no_inference,
                                  decoder.decode)

            if result:
                decoder.decode(result)
            else:
                print('ERROR')

# '"    N = int(input())
# for n in range(N):

#     D, R = map(int, input().split())

#     domain = [d for d in range(1, D + 1)]

#     constraints = []

#     # restrições de coluna do problema
#     for c in range(D):
#         min_var = 10 + (c + 1)
#         max_var = 10 * (D + 1)
#         for variable_1 in range(min_var, max_var, 10):
#             for variable_2 in range(variable_1, max_var, 10):
#                 if variable_1 != variable_2:
#                     constraints.append(Binary(operator.ne, variable_1, variable_2))
    
#     # restrições de linha do problema
#     for r in range(D):
#         min_var = (r + 1) * 10 + 1
#         max_var = min_var + D
#         for variable_1 in range(min_var, max_var):
#             for variable_2 in range(variable_1, max_var):
#                 if variable_1 != variable_2:
#                     constraints.append(Binary(operator.ne, variable_1, variable_2))

#     # restrições da instancia
#     for i in range(R):
#         ai, aj, bi, bj = map(int, input().split())
#         variable_1 = ai * 10 + aj
#         variable_2 = bi * 10 + bj
#         constraints.append(Binary(operator.lt, variable_1, variable_2))

#     # atribuições iniciais
#     assignment = {}
#     for i in range(D):
#         row = list(map(int, input().split()))
#         for j in range(D):
#             variable = (i + 1) * 10 + (j + 1)
#             if row[j] > 0:
#                 assignment[variable] = row[j]
#                 constraints.append(Unary(operator.eq, variable, row[j]))

#     input() # EOF

#     result = bt(assignment, domain, constraints, is_complete, 
#                 first_unassigned_var,
#                 order_domain_values,
#                 AssignmentDecoder(D).decode)

#     print(n + 1)
#     if result:
#         AssignmentDecoder(D).decode(result)
#     else:
#         print('ERROR')
#     break"'


