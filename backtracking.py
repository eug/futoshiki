from copy import deepcopy

import sys


def is_consistent(assignment, domain, constraints, variable, value):
    original_value = assignment[variable]
    assignment[variable] = value
    for constraint in constraints:
        if not constraint.eval(assignment):
            assignment[variable] = original_value
            return False
    assignment[variable] = original_value
    return True

def bt(assignment, domain, constraints, is_complete,
       select_unassigned_var, order_domain_values,
       debug_step=None, null_value=0):

    if is_complete(assignment):
        return assignment

    if debug_step:
        debug_step(assignment)

    for variable in  select_unassigned_var(assignment, domain, constraints):

        for value in order_domain_values(assignment, domain, constraints, variable):
            
            if is_consistent(assignment, domain, constraints, variable, value):
                assignment[variable] = value
                result = bt(assignment, domain, constraints, is_complete, select_unassigned_var, order_domain_values, debug_step)
                if result:
                    return result
                assignment[variable] = null_value

    return False
