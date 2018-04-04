import operator

class Constraint:
    def __init__(self, op, arg1, arg2, null_value=0):
        self.op, self.arg1, self.arg2, self.null_value = op, arg1, arg2, null_value

    def eval(self, A):
        """ Retorna False se violar a restrição, True caso contrario"""
        raise NotImplementedError()

    def __str__(self):
        op = str(self.op).split()[-1].replace('>', '')
        return '{} {} {}'.format(self.arg1, op, self.arg2)

class Binary(Constraint):
    def __init__(self, op, variable_1, variable_2):
        super().__init__(op, variable_1, variable_2)

    def eval(self, A):
        if A[self.arg1] == self.null_value or A[self.arg2] == self.null_value:
            return True
        return self.op(A[self.arg1], A[self.arg2])

    def __str__(self):
        return 'b({})'.format(super().__str__())

class Unary(Constraint):
    def __init__(self, op, variable, domain_value):
        super().__init__(op, variable, domain_value)

    def eval(self, A):
        if A[self.arg1] == self.null_value:
            return True
        return self.op(A[self.arg1], self.arg2)

    def __str__(self):
        return 'u({})'.format(super().__str__())
