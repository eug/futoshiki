# -*- coding: utf-8 -*-
import getopt
import operator
import sys
from random import shuffle
from time import time

from backtracking import Backtracking
from constraint import Binary, Unary
from heuristics import *


class Config:
    input_file = None
    variable_selection = None
    value_selection = None
    look_ahead = None
    output_as_csv = False
    show_help = False
    instance_id = -1


def parse_args(argv):
    shortopts = 'i:f:r:l:a:ch'

    longopts = [
        'instance='
        'input-file=',
        'var-selection=',
        'val-selection=',
        'look-ahead=',
        'as-csv',
        'help'
    ]

    arg_fn_map = {
        'fuv': first_unassigned_var,
        'mrvr': mrv_r,
        'mrvd': mrv_d,
        'odv': ordered_domain_values,
        'idv': inverted_domain_values,
        'rdv': random_domain_values,
        'lcv': lcv,
        'dla': dont_look_ahead,
        'fwc': forward_checking
    }

    config = Config()
    options, _ = getopt.getopt(sys.argv[1:], shortopts, longopts)

    for opt, arg in options:
        if opt in ('-i', '--instance'):
            config.instance_id = int(arg)
        elif opt in ('-f', '--input-file'):
            config.input_file = arg
        elif opt in ('-c', '--as-csv'):
            config.output_as_csv = True
        elif opt in ('-h', '--help'):
            config.show_help = True
        elif opt in ('-r', '--var-selection'):
            if arg in ('fuv', 'mrvr', 'mrvd'):
                config.variable_selection = arg_fn_map[arg]
        elif opt in ('-l', '--val-selection'):
            if arg in ('odv', 'idv', 'rdv', 'lcv'):
                config.value_selection = arg_fn_map[arg]
        elif opt in ('-a', '--look-ahead'):
            if arg in ('dla', 'fwc'):
                config.look_ahead = arg_fn_map[arg]

    return config

def read_file(filename):
    instances = []

    with open(filename, 'r') as f:

        N = int(f.readline())

        for n in range(N):

            variables = []
            domains = {}
            constraints = []
            assignment = {}
            D, R = map(int, f.readline().split())

            for i in range(D):
                for j in range(D):
                    variable = int(str(i + 1) + str(j + 1))
                    variables.append(variable)
                    domains[variable] = [d for d in range(1, D + 1)]

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
                ai, aj, bi, bj = map(int, f.readline().split())
                variable_1 = ai * 10 + aj
                variable_2 = bi * 10 + bj
                constraints.append(Binary(operator.lt, variable_1, variable_2))

            # atribuições iniciais
            for i in range(D):
                row = list(map(int, f.readline().split()))
                for j in range(D):
                    variable = (i + 1) * 10 + (j + 1)
                    if row[j] > 0:
                        assignment[variable] = row[j]
                        constraints.append(Unary(operator.eq, variable, row[j]))

            f.readline() # EOF
    
            instances.append((variables, domains, constraints, assignment, D, r, n))

        return instances

def print_help():
    print("""Futoshiki Solver
Usage:
    python futoshiki.py -f futoshiki_all.txt -r fuv -l odv -a dla
    python futoshiki.py -f futoshiki_all.txt -r mrvr -l lcv -a fwc -c

Options:
    -i --instance=ID                    Instance ID
    -f --input-file=FILE                Instances file
    -r --var-selection=[fuv|mrvr|mrvd]  Variable selection algorithm
    -l --val-selection=[odv|rdv|lcv]    Value selection algorithms
    -a --look-ahead=[dla|fwc]           Look ahead algorithm
    -c --as-csv                         Print the results line-by-line (csv-style)
    -h --help                           Print this message

Variable Selection Heuristics:
    fuv     First Unassignment Variable
    mrvr    Minimum-Remaining-Values (Random tie breaker)
    mrvd    Minimum-Remaining-Values (Maximum-Restriction-Degree tie breaker)

Value Selection Heuristics:
    odv     Ordered-Domain-Values
    idv     Inverted-Domain-Value
    rdv     Random-Domain-Values
    lcv     Least-Constraining-Values

Look Ahead Heuristics:
    dla     Don't Look Ahead
    fwc     Forward Checking
    """)

def _parse_as_board(dimension, output):
    board = [0] * dimension
    for i in range(dimension):
        board[i] = [0] * dimension

    for k, v in output.items():
        i, j = int(k/10) - 1, k - (int(k/10) * 10) - 1
        board[i][j] = v
    
    return board

def boardify_output(dimension, output):
    if not output:
        return " "

    s = ""
    for row in _parse_as_board(dimension, output):
        for cell in row:
            s += str(cell) + " "
        s += "\n"

    return s

def stringfy_output(dimension, output):
    if not output:
        return " "

    s = ""
    for row in _parse_as_board(dimension, output):
        for cell in row:
            s += str(cell) + " "

    return s


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        print('Faltando argumentos')
        sys.exit(1)

    config = parse_args(sys.argv[1:])

    if config.show_help:
        print_help()
        sys.exit(0)

    if not config.input_file:
        print('Arquivo de entrada não especificado')
        sys.exit(1)

    if not config.variable_selection:
        print('Algoritmo de seleção de variavel não especificado')
        sys.exit(1)
    
    if not config.value_selection:
        print('Algoritmo de seleção de valor não especificado')
        sys.exit(1)

    if not config.look_ahead:
        print('Algoritmo de inferencia não especificado')
        sys.exit(1)
    
    instances = read_file(config.input_file)

    if config.instance_id > 0:
        instances = [instances[config.instance_id-1]]

    for variables, domains, constraints, assignment, D, r, n in instances:
        try:
            bt = Backtracking(variables, domains, constraints, 1000000)
            bt.set_is_complete(total_assignment)
            bt.set_variable_selection(config.variable_selection)
            bt.set_value_selection(config.value_selection)
            bt.set_look_ahead(config.look_ahead)

            start = time()
            output = bt.solve(assignment)
            t = time() - start

            nassigns = bt.csp.nassigns
        except KeyboardInterrupt:
            t = 0
            nassigns = 0
            output = None

        if nassigns == 1000000:
            print(n + 1)
            print('Numero de atribuições excede limite maximo')

        if config.output_as_csv:
            if output:
                result = stringfy_output(D, output)
                print ("{},{},{},{},{:.2f},{}".format(n + 1, D, r, nassigns, t, result))
            else:
                print ("{},{},{},{},{:.2f},".format(n + 1, D, r, nassigns, t))
        else:
            print(n + 1)
            print(boardify_output(D, output))
