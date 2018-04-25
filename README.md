# Futoshiki
A naïve implementation of Futoshiki solver using Backtracking in Python 3.

## Usage
    python futoshiki.py -f input/futoshiki_all.txt -r fuv -l odv -a dla

## Options
    -i --instance=ID                    Instance ID
    -f --input-file=FILE                Instances file
    -r --var-selection=[fuv|mrvr|mrvd]  Variable selection algorithm
    -l --val-selection=[odv|rdv|lcv]    Value selection algorithms
    -a --look-ahead=[dla|fwc]           Look ahead algorithm
    -c --as-csv                         Print the results line-by-line (csv-style)
    -h --help                           Print this message

## Variable Selection Heuristics
    fuv     First Unassigned Variable
    mrvf    Minimum-Remaining-Values (tie breaker: First )
    mrvd    Minimum-Remaining-Values (tie breaker: Maximum-Restriction-Degree)

## Value Selection Heuristics
    odv     Ordered-Domain-Values
    idv     Inverted-Domain-Value
    rdv     Random-Domain-Values
    lcv     Least-Constraining-Values

## Look Ahead Heuristics
    dla     Don't Look Ahead
    fwc     Forward Checking
