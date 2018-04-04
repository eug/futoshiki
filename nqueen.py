import operator
import sys
from backtracking import bt
from constraint import Binary, Unary

NQUEENS = 4

def decode_result(result):
    board = [] * NQUEENS
    for k, v in result.items():
        i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1
        print(i, j)
        if len(board[i]) == 0:
            board[i] = [] * NQUEENS

        board[i][j] = v

    for row in board:
        for cell in row:
            sys.stdout.write(cell + ' ')
        sys.stdout.write('\n')


def is_complete(assignment):
    pass




# initialization
domain = [q + 1 for q in range(1, NQUEENS)]
assignment = {}
constraints = []

# encode board
for i in range(NQUEENS):
    for j in range(NQUEENS):
        assignment[int(str(i+1) + str(j+1))] = 0

# create column constraints
for c in range(NQUEENS):
    min_var = 10 + (c + 1)
    max_var = 10 * (NQUEENS + 1)
    for variable_1 in range(min_var, max_var, 10):
        for variable_2 in range(variable_1, max_var, 10):
            if variable_1 != variable_2:
                constraints.append(Binary(operator.ne, variable_1, variable_2))

# create row constraints
for r in range(NQUEENS):
    min_var = (r + 1) * 10 + 1
    max_var = min_var + NQUEENS
    for variable_1 in range(min_var, max_var):
        for variable_2 in range(variable_1, max_var):
            if variable_1 != variable_2:
                constraints.append(Binary(operator.ne, variable_1, variable_2))

# create se-diagonal constraints
constraints.append(Binary(operator.ne, 31, 42))
constraints.append(Binary(operator.ne, 21, 32))
constraints.append(Binary(operator.ne, 21, 43))
constraints.append(Binary(operator.ne, 32, 43))
constraints.append(Binary(operator.ne, 11, 22))
constraints.append(Binary(operator.ne, 11, 33))
constraints.append(Binary(operator.ne, 11, 44))
constraints.append(Binary(operator.ne, 22, 33))
constraints.append(Binary(operator.ne, 22, 44))
constraints.append(Binary(operator.ne, 33, 44))
constraints.append(Binary(operator.ne, 12, 23))
constraints.append(Binary(operator.ne, 12, 34))
constraints.append(Binary(operator.ne, 23, 34))
constraints.append(Binary(operator.ne, 13, 24))



# create sw-diagonal constraints
constraints.append(Binary(operator.ne, 34, 43))
constraints.append(Binary(operator.ne, 24, 33))
constraints.append(Binary(operator.ne, 24, 42))
constraints.append(Binary(operator.ne, 33, 42))
constraints.append(Binary(operator.ne, 14, 23))
constraints.append(Binary(operator.ne, 14, 32))
constraints.append(Binary(operator.ne, 14, 41))
constraints.append(Binary(operator.ne, 23, 32))
constraints.append(Binary(operator.ne, 23, 41))
constraints.append(Binary(operator.ne, 32, 41))
constraints.append(Binary(operator.ne, 13, 22))
constraints.append(Binary(operator.ne, 13, 31))
constraints.append(Binary(operator.ne, 22, 31))
constraints.append(Binary(operator.ne, 12, 21))



print(bt(assignment, domain, constraints))