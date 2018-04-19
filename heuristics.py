from random import shuffle

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
        return sum(csp.is_consistent(assignment, variable, value) \
                   for value in csp.domains[variable])

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
        return sum(csp.is_consistent(assignment, variable, value) \
                   for value in csp.domains[variable])

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

def random_domain_values(csp, assignment, variable):
    """ Método: Embaralhado (RND) """
    shuffle(csp.domains[variable])
    return csp.domains[variable]

def lcv(csp, assignment, variable):
    """ Método: Least-constraining-values (LCV) """
    def count_conflicts(value):
        csp.assign(assignment, variable, value)
        conflicts = sum(1 for c in csp.variable_constraints[variable] \
                        if not c.eval(assignment))
        csp.unassign(assignment, variable)
        return conflicts

    return sorted(csp.domains[variable], key=count_conflicts)


# Inferencia

def dont_look_ahead(csp, assignment, variable, value, pruned):
    """ Nenhuma inferencia é aplicada """
    return True

def forward_checking(csp, assignment, variable, value, pruned):
    """ Aplica a inferencia de Checagem Adiante """
    for N in csp.variable_neighbors[variable]:
        if N not in assignment:
            for n in csp.domains[N]:
                if not csp.is_consistent(assignment, N, n):
                    csp.domains[N].remove(n)
                    if pruned is not None:
                        pruned.append((N, n))
            if not csp.domains[N]:
                return False
    return True

def ac3(csp, assignment, variable, value, pruned):
    """ Aplica a inferencia de Consistencia de Arcos """
    queue = [(neighbor, variable) for neighbor in csp.variable_neighbors[variable]]
    
    while queue:
        neighbor, variable = queue.pop()
        if _revise(csp, assignment, neighbor, variable, pruned):
            if not csp.domains[neighbor]:
                return False
            for n in csp.variable_neighbors[neighbor]:
                if n != variable:
                    queue.append((n, neighbor))
    return True

def _revise(csp, assignment, neighbor, variable, pruned):
    """Return true if we remove a value."""
    revised = False
    
    for x in csp.domains[neighbor]:
        csp.assign(assignment, neighbor, x)
        for y in csp.domains[variable]:
            csp.assign(assignment, variable, y)
            if not csp.is_consistent(assignment):
                for p in csp.prune(neighbor, x):
                    pruned.append(p)
                revised = True
            csp.unassign(assignment, variable, y)
        csp.unassign(assignment, neighbor, x)

    return revised
