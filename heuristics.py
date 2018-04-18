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

def inverted_domain_values(csp, assignment, variable):
    """ Método: Invertido (ORD)"""
    return sorted(csp.domains[variable], reverse=True)

def random_domain_values(csp, assignment, variable):
    """ Método: Embaralhado (RND) """
    shuffle(csp.domains[variable])

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
    """ Aplica a inferencia de Checar Adiante """
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
