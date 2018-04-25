from random import shuffle

# Definição de completude

def total_assignment(csp, assignment):
    return len(csp.variables) == len(assignment.keys())

# Ordem das variaveis

def first_unassigned_var(csp, assignment):
    for variable in csp.variables:
        if variable not in assignment:
            return variable

def mrv_f(csp, assignment):
    """ Heuristica: Minimum-remaining-values
        Desempate: Primeiro """
    min_remaining = 10000
    variable = None

    for v in csp.variables:
        if v in assignment: continue
        remaining = sum(csp.is_consistent(assignment, v, d) for d in csp.domains[v])

        if remaining < min_remaining:
            min_remaining = remaining
            variable = v

    return variable

def mrv_d(csp, assignment):
    """ Heuristica: Minimum-remaining-values
        Desempate: Maior Grau de Restrição  """
    max_degree = -1
    min_remaining = 10000
    variable = None

    for v in csp.variables:
        if v in assignment: continue
        degree = len(csp.variable_constraints[v])
        remaining = sum(csp.is_consistent(assignment, v, d) for d in csp.domains[v])

        if (remaining < min_remaining) or (remaining == min_remaining and degree > max_degree):
            min_remaining = remaining
            max_degree = degree
            variable = v

    return variable

# Ordem dos valores

def ordered_domain_values(csp, assignment, variable):
    """ Método: Ordenado (ORD)"""
    return csp.domains[variable]

def inverted_domain_values(csp, assignment, variable):
    """ Método: Invertido (ORD)"""
    return sorted(csp.domains[variable], reverse=True)

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
    """ Aplica Checagem Adiante """
    for N in csp.variable_neighbors[variable]:
        if N in assignment: continue

        for n in csp.domains[N][:]:
            if not csp.is_consistent(assignment, N, n):
                pruned.append((N, n))
                csp.domains[N].remove(n)

        if not csp.domains[N]:
            return False

    return True
