import operator

from backtracking import bt
from constraint import Binary, Unary

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
    Binary(operator.ne, 'NSW', 'V')
]

print(bt(assignment, domain, constraints))
