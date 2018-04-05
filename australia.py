import operator
import sys
from backtracking import bt
from constraint import Binary, Unary

class AssignmentDecoder:
    def __init__(self, d):
        self.d = d
        self.visited = []

    def decode(self, assignment):
        for variable, value in assignment.items():
            print(variable, value)

        sys.stdout.write('\n')

def is_complete(assignment):
    return all(v != 0 for k, v in assignment.items())

def select_unassigned_vars(assignment, domain, constraints):
    variables = []
    for k, v in assignment.items():
        if v == 0:
            variables.append(k)
    return variables

def order_domain_values(assignment, domain, constraints, variable):
    return domain

RED = 1
BLUE = 2
GREEN = 3

domain = [RED, BLUE, GREEN]
assignment = {'SA':0, 'NSW':0, 'NT':0, 'Q':0, 'WA':0, 'V':0, 'T':0}
constraints = [
    Binary(operator.ne, 'SA', 'WA'),
    Binary(operator.ne, 'SA', 'NT'),
    Binary(operator.ne, 'SA', 'Q'),
    Binary(operator.ne, 'SA', 'NSW'),
    Binary(operator.ne, 'SA', 'V'),
    Binary(operator.ne, 'WA', 'NT'),
    Binary(operator.ne, 'NT', 'Q'),
    Binary(operator.ne, 'Q', 'NSW'),
    Binary(operator.ne, 'NSW', 'V'),
    Unary(operator.eq, 'SA', RED)
]

print(bt(assignment, domain, constraints, is_complete, 
         select_unassigned_vars, order_domain_values,
         AssignmentDecoder(3).decode))
