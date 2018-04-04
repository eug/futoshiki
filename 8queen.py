import operator
import sys
from backtracking import bt
from constraint import Binary, Unary

NQUEENS = 4

def decode_result(result):
    board = [] * NQUEENS
    for k, v in result.items():
        i, j = int(k/10), k - (int(k/10) * 10)

        if len(board[i]) == 0:
            board[i] = [] * NQUEENS

        board[i][j] = v

    for row in board:
        for cell in row:
            sys.stdout.write(cell + ' ')
        sys.stdout.write('\n')


# initialization
domain = [q + 1 for q in range(1, NQUEENS)]
assignment = {}
constraints = []

# encode board
for i in range(NQUEENS):
    for j in range(NQUEENS):
        assignment[int(str(i+1) + str(j+1))] = 0

# print(assignment)



# create column constraints
for c in range(NQUEENS):
    min_var = 10 + (c + 1)
    max_var = 10 * (NQUEENS + 1)
    for variable_1 in range(min_var, max_var, 10):
        for variable_2 in range(variable_1, max_var, 10):
            if variable_1 != variable_2:
                print(variable_1, variable_2)
    print('')
        # constraints.append(Binary(operator.ne, , 'WA'))


#     Binary(operator.ne, 'SA', 'WA'),
#     Binary(operator.ne, 'SA', 'NT'),
#     Binary(operator.ne, 'SA', 'Q'),
#     Binary(operator.ne, 'SA', 'NSW'),
#     Binary(operator.ne, 'SA', 'V'),
#     Binary(operator.ne, 'WA', 'NT'),
#     Binary(operator.ne, 'NT', 'Q'),
#     Binary(operator.ne, 'Q', 'NSW'),
#     Binary(operator.ne, 'NSW', 'V')
# ]

# print(bt(assignment, domain, constraints))