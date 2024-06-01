# Testing the performance of two formulae involving logarithms
#   diviving two logarithms
#   using a weird base with logarithms

from performance import Tests

from random import randint
from math import log, e


def test_logarithms(trials):
    
    # Creates the arguments for the tests
    args = [
        [randint(1, 10000), # The number of which to take the log
         randint(1, 10000), # The log base or logged divisor
         randint(1, 5)]     # The power to raise the whole equation
            for i in range(trials) # Creates a set of arguments per trial
    ]

    # Don't print since we're logging anyways
    printout = False

    # Sets up the test
    logarithms_tests = Tests(
        [logarithm_divi, logarithm_base],   # The functions to test
        ['Divi', 'Base'],                   # The names to log them under
        trials = trials,                    # The number of trails
        printout = printout                 # Whether to print to console
    )

    # Runs the tests
    results = logarithms_tests(*args, params_per_trial = True)

    return results



# These are two variations of the mapping function used in visualise to show a palette
# They evaluate to the same value

def logarithm_divi(x, base, p):
    return (log(x, e) / (2 * log(base, e)) + 0.5) ** p

def logarithm_base(x, base, p):
    return (log(x, base) / 2 + 0.5) ** p