from copy import deepcopy

import sys
from random import shuffle

def order_domain_values(assignment, variable,  domain, constraints):
    return domain

def is_consistent(assignment, constraints, variable, value):
    assignment[variable] = value
    for constraint in constraints:
        if not constraint.eval(assignment):
            return False
    return True

def select_unassigned_vars(assignment):
    variables = []
    for k, v in assignment.items():
        if v == 0:
            variables.append(k)
    # shuffle(variables)
    return variables

def is_complete(assignment):
    return all(v != 0 for k, v in assignment.items())

def bt(assignment, domain, constraints):
    if is_complete(assignment):
        return assignment
    
    for variable in select_unassigned_vars(assignment):
        _assignment = deepcopy(assignment)

        for value in order_domain_values(assignment, variable,  domain, constraints):
            if is_consistent(_assignment, constraints, variable, value):
                assignment[variable] = value
                result = bt(assignment, domain, constraints)
                if result:
                    # decode_result(result, len(domain))
                    # print('')
                    return result
                assignment[variable] = 0 # null_value
                # decode_result(assignment, len(domain))
                # print('')

    return False


def decode_result(result, d):
    board = [[]] * d
    for k, v in result.items():
        i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1

        if len(board[i]) == 0:
            board[i] = [0] * d

        board[i][j] = v

    for row in board:
        for cell in row:
            sys.stdout.write(str(cell) + ' ')
        sys.stdout.write('\n')