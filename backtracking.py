from copy import deepcopy

import sys


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
    
    def assign(self, assignment, variable, value):
        assignment[variable] = value

    def unassign(self, assignment, variable):
        if variable in assignment:
            del assignment[variable]

    def is_consistent(self, assignment, variable, value):
        original_value = None

        if variable in assignment:
            original_value = assignment[variable]
        
        assignment[variable] = value

        for constraint in constraints:
            if not constraint.eval(assignment):
                assignment[variable] = original_value
                return False

        if original_value:
            self.assign(assignment, variable, original_value)
        else:
            self.unassign(assignment, variable, value)

        return True

def backtracking(csp, assignment,
                 is_complete,
                 select_unassigned_var,
                 order_domain_values,
                 inference,
                 debug_step=None,
                 null_value=0):

    def bt(assignment):
        if is_complete(assignment):
            return assignment

        if debug_step:
            debug_step(assignment)

        variable = select_unassigned_var(csp, assignment)

        for value in order_domain_values(csp, assignment, variable):
            if cps.is_consistent(csp, assignment, variable, value):

                if inferece(csp, assignment, variable, value):
                    assignment[variable] = value
                    result = bt(assignment)
                    if result:
                        return result
                
        assignment[variable] = null_value
        return False

    return bt(assignment)