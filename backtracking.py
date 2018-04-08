import sys
from copy import deepcopy

from constraint import Binary, Unary


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

        # stats
        self.nassigns = 0

        # optimisation
        self.variable_constraints = {}
        self.variable_neighbors = {}

        for v in self.variables:
            self.variable_constraints[v] = []
            self.variable_neighbors[v] = set([])

            for c in self.constraints:
                a, b = c.arg1, c.arg2
                if isinstance(c, Binary) and v in [a, b]:
                    n = b if v == a else a
                    self.variable_constraints[v].append(c)
                    self.variable_neighbors[v].add(n)
                elif isinstance(c, Unary) and v == a:
                    self.variable_constraints[v].append(c)


    def assign(self, assignment, variable, value, do_count=False):
        """ Adiciona uma variável-valor nas atribuições """
        assignment[variable] = value
        if do_count:
            self.nassigns += 1

    def unassign(self, assignment, variable):
        """ Remove a variável das atribuições """
        if variable in assignment:
            del assignment[variable]

    def is_consistent(self, assignment, variable, value):
        """ Verifica se a atribuição do valor na variavel é valida com todas restrições """
        self.assign(assignment, variable, value)

        for constraint in self.variable_constraints[variable]:
            if not constraint.eval(assignment):
                self.unassign(assignment, variable)
                return False

        self.unassign(assignment, variable)
        return True

    def censure(self, variable, value):
        """ Remove todos possiveis valores do dominio da variavel, exceto o valor atual """
        removals = [(variable, d) for d in self.domains[variable] if d != value]
        self.domains[variable] = [value]
        return removals

    def absolve(self, censured):
        """ Adiciona os items censurados no dominio da variável """
        for variable, value in censured:
            self.domains[variable].append(value)


class Backtracking:
    def __init__(self, variables, domains, constraints):
        self.csp = CSP(variables, domains, constraints)
        self.is_complete = None
        self.select_unassigned_var = None
        self.order_domain_values = None
        self.look_ahead = None
    
    def set_variable_selection(self, callback):
        self.select_unassigned_var = callback
    
    def set_value_selection(self, callback):
        self.order_domain_values = callback
    
    def set_look_ahead(self, callback):
        self.look_ahead = callback

    def set_is_complete(self, callback):
        self.is_complete = callback

    def solve(self, assignment):
        self._ensure_callbacks()
        return self._bt(assignment)
    
    def _ensure_callbacks(self):
        if not self.select_unassigned_var or\
           not self.order_domain_values or\
           not self.is_complete or\
           not self.look_ahead:
            raise Exception()

    def _bt(self, assignment):
        if self.is_complete(self.csp, assignment):
            return assignment

        # if debug_step:
        #     debug_step(assignment)

        variable = self.select_unassigned_var(self.csp, assignment)

        for value in self.order_domain_values(self.csp, assignment, variable):
            if self.csp.is_consistent(assignment, variable, value):
                self.csp.assign(assignment, variable, value, do_count=True)
                censured = self.csp.censure(variable, value)
                if self.look_ahead(self.csp, assignment, variable, value, censured):
                    result = self._bt(assignment)
                    if result:
                        return result
                self.csp.absolve(censured)
        self.csp.unassign(assignment, variable)
        return False






# def backtracking(csp, assignment,
#                  is_complete,
#                  select_unassigned_var,
#                  order_domain_values,
#                  inference,
#                  debug_step=None,
#                  null_value=0):

#     def bt(assignment):
#         if is_complete(csp, assignment):
#             return assignment

#         if debug_step:
#             debug_step(assignment)

#         variable = select_unassigned_var(csp, assignment)

#         for value in order_domain_values(csp, assignment, variable):
#             if csp.is_consistent(assignment, variable, value):
#                 csp.assign(assignment, variable, value)
#                 censured = csp.censure(variable, value)
#                 if inference(csp, assignment, variable, value, censured):
#                     result = bt(assignment)
#                     if result:
#                         return result
#                 csp.absolve(censured)
#         csp.unassign(assignment, variable)
#         return False

#     return bt(assignment)
