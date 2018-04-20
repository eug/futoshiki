import sys

from constraint import Binary, Unary


class CSP:
    def __init__(self, variables, domains, constraints, max_assigns=-1):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.max_assigns = max_assigns
        self.nassigns = 0

        # optimisation
        removals = []
        for v in self.variables:
            for c in self.constraints:
                a, b = c.arg1, c.arg2
                if isinstance(c, Unary) and v == a:
                    for d in self.domains[v]:
                        if d != b:
                            removals.append((v, d))

        for variable, value in removals:
            self.domains[variable].remove(value)
        
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

    def assign(self, assignment, variable, value, do_count=False):
        """ Adiciona uma variável e valor nas atribuições """
        assignment[variable] = value
        if do_count:
            self.nassigns += 1

    def unassign(self, assignment, variable):
        """ Remove a variável das atribuições """
        if variable in assignment:
            del assignment[variable]

    def is_consistent(self, assignment, variable, value):
        """ Verifica se a atribuição do valor na variavel é
            valida com todas restrições """
        self.assign(assignment, variable, value)

        for constraint in self.variable_constraints[variable]:
            if not constraint.eval(assignment):
                self.unassign(assignment, variable)
                return False

        self.unassign(assignment, variable)
        return True

    def prune(self, variable, value):
        """ Remove todos possiveis valores do dominio
            da variavel, exceto o valor atual """
        removals = [(variable, d) for d in self.domains[variable] if d != value]
        self.domains[variable] = [value]
        return removals

    def unprune(self, pruned):
        """ Adiciona os items podados no dominio da variável """
        for variable, value in pruned:
            self.domains[variable].append(value)


class Backtracking:
    def __init__(self, variables, domains, constraints, max_assigns=-1):
        self.csp = CSP(variables, domains, constraints, max_assigns)
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

    def _can_assign(self):
        return self.csp.max_assigns > -1 and \
               self.csp.nassigns < self.csp.max_assigns

    def _bt(self, assignment):
        if self.is_complete(self.csp, assignment):
            return assignment

        variable = self.select_unassigned_var(self.csp, assignment)

        if not variable:
            return False

        for value in self.order_domain_values(self.csp, assignment, variable):

            # Verifica se a atribuição é consistente
            if self.csp.is_consistent(assignment, variable, value):

                # Verifica se não excedeu o limite de atribuições
                if not self._can_assign():
                    return False

                self.csp.assign(assignment, variable, value, do_count=True)

                # Remove os demais valores possiveis da variavel atual
                pruned = self.csp.prune(variable, value)

                # Executa o algoritmo de look ahead (se houver)
                if self.look_ahead(self.csp, assignment, variable, value, pruned):
                    result = self._bt(assignment)
                    if result:
                        return result

                # Adiciona novamente os valores possiveis
                self.csp.unprune(pruned)

        self.csp.unassign(assignment, variable)

        return False
