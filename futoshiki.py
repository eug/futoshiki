import sys
from constraint import Unary, Binary
from backtracking import bt
import operator

def decode_result(result, d):
    board = [[]] * d
    for k, v in result.items():
        i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1

        if len(board[i]) == 0:
            board[i] = [0] * d

        board[i][j] = v

    for row in board:
        for cell in row:
            sys.stdout.write(str(cell) + ' ')
        sys.stdout.write('\n')


if __name__ == '__main__':

    N = int(input())
    for n in range(N):

        D, R = map(int, input().split())

        domain = [d for d in range(1, D + 1)]

        constraints = []

        # restrições de coluna do problema
        for c in range(D):
            min_var = 10 + (c + 1)
            max_var = 10 * (D + 1)
            for variable_1 in range(min_var, max_var, 10):
                for variable_2 in range(variable_1, max_var, 10):
                    if variable_1 != variable_2:
                        constraints.append(Binary(operator.ne, variable_1, variable_2))
        
        # restrições de linha do problema
        for r in range(D):
            min_var = (r + 1) * 10 + 1
            max_var = min_var + D
            for variable_1 in range(min_var, max_var):
                for variable_2 in range(variable_1, max_var):
                    if variable_1 != variable_2:
                        constraints.append(Binary(operator.ne, variable_1, variable_2))

        # restrições da instancia
        for i in range(R):
            ai, aj, bi, bj = map(int, input().split())
            variable_1 = ai * 10 + aj
            variable_2 = bi * 10 + bj
            constraints.append(Binary(operator.lt, variable_1, variable_2))

        # atribuições iniciais
        assignment = {}
        for i in range(D):
            row = list(map(int, input().split()))
            for j in range(D):
                variable = (i + 1) * 10 + (j + 1)
                assignment[variable] = row[j]

                if row[j] > 0:
                    constraints.append(Unary(operator.eq, variable, row[j]))

        input() # EOF
        # print(domain)
        # print(assignment)
        # for c in constraints:
        #     print(c)
        result = bt(assignment, domain, constraints)
        print(n + 1)
        if result:
            decode_result(result, D)
        else:
            print('ERROR')
        break


