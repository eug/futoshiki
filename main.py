import sys

import operator

def backtracking_search(csp):
    # returns a solution or failure
    return recursive_backtracking({}, csp)

def recursive_backtracking(assignment, csp):
    # returns a solution or failure
    if is_assignment_complete():
        return assignment
    
    var = select_unassigned_variable(variables[csp], assignment, csp)

    for v in order_domain_values(var, assignment, csp):
        if _is_consistent_with_assignment_according_to_constraints(v):
            add(var, value) # to assignment
            result = recursive_backtracking(assignment, csp)
            if result != 'ERROR':
                return result
            remove(var, value) # from assignment
    return False

def solve(board, constraints):
    print(board)
    print(constraints)
    print('')





class Backtracking:
    def __init__(self):
        pass
    
    def solve(self, P):
        if self._reject(P, c):
            return

        if self._accept(P, c):
            return self._output(P, c)

        s = self._first(P, c)

        while s:
            self.solve(s)
            s = self._next(P, c)





def bt(assignments, variables, domain, constraints):
    pass


N = int(input())
for n in range(N):
    d, r = map(int,input().split())

    constraints = []
    for _ in range(r):
        ai, aj, bi, bj = map(int, input().split())
        constraints.append(((ai, aj), (bi, bj)))

    board = [0] * d
    for i in range(d):
        board[i] = list(map(int, input().split()))

    input() # EOF
    
    print(n + 1)
    solve(board, constraints)



