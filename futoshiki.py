# -*- coding: utf-8 -*-
from copy import deepcopy
import sys
from constraint import Unary, Binary
# from backtracking import backtracking, CSP
import operator
from random import shuffle
from itertools import product
from time import time
from backtracking import Backtracking


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


# Ordem das variaveis

def first_unassigned_var(csp, assignment):
    for variable in csp.variables:
        if variable not in assignment:
            return variable

def mrv_r(csp, assignment):
    """ Heuristica: Minimum-remaining-values
        Desempate: Aleatoriamente """

    def count_valid_values(variable):
        """ Conta o numero de valores validos da variavel """
        return sum(csp.is_consistent(assignment, variable, value) for value in csp.domains[variable])

    def random_unassigned_variables():
        """ Retorna variaveis remanescentes aleatoriamente """
        variables = [v for v in csp.variables if v not in assignment]
        shuffle(variables)
        return variables

    return min(random_unassigned_variables(), key=count_valid_values)


def mrv_d(csp, assignment):
    """ Heuristica: Minimum-remaining-values
        Desempate: Maior Grau de Restrição  """

    def count_valid_values(variable):
        """ Conta o numero de valores validos da variavel """
        return sum(csp.is_consistent(assignment, variable, value) for value in csp.domains[variable])

    def degree_unassigned_variables():
        """ Retorna variaveis com maior grau de restrição """
        vars_degree = {}
        max_degree = 0

        for var in csp.variables:
            if var not in assignment:
                degree = len(csp.variable_constraints[var])
                vars_degree[var] = degree
                if degree > max_degree:
                    max_degree = degree

        return [k for k, v in vars_degree.items() if v == max_degree]

    return min(degree_unassigned_variables(), key=count_valid_values)


# Ordem dos valores

def ordered_domain_values(csp, assignment, variable):
    """ Método: Ordenado (ORD)"""
    return csp.domains[variable]

def unordered_domain_values(csp, assignment, variable):
    """ Método: Embaralhado (RND) """
    shuffle(csp.domains[variable])

def lcv(csp, assignment, variable):
    """ Método: Least-constraining-values (LCV) """
    def count_conflicts(value):
        csp.assign(assignment, variable, value)
        conflicts = sum(1 for c in csp.variable_constraints[variable] if not c.eval(assignment))
        csp.unassign(assignment, variable)
        return conflicts

    return sorted(csp.domains[variable], key=count_conflicts)



# Inferencia

def no_inference(csp, assignment, variable, value, censured):
    return True


def forward_checking(csp, assignment, variable, value, censured):
    for N in csp.variable_neighbors[variable]:
        if N not in assignment:
            for n in csp.domains[N]:
                if not csp.is_consistent(assignment, N, n):
                    csp.domains[N].remove(n)
                    if censured is not None:
                        censured.append((N, n))
            if not csp.domains[N]:
                return False
    return True



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
            bt = Backtracking(variables, domains, constraints)
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

        print ("{},{},{},{},{:.2f},{}".format(n, D, r, nassigns, t, result))
