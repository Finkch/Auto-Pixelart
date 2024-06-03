# Testing the performance of two formulae involving logarithms
#   diviving two logarithms
#   using a weird base with logarithms

from random import randint
from math import log, e


# Returns the arguments and functions for this test case
def test_logarithms(trials):
    
    # Creates the arguments for the tests
    args = [
        [randint(2, 10000), # The number of which to take the log
         randint(2, 10000), # The log base or logged divisor
         randint(1, 5)]     # The power to raise the whole equation
            for i in range(trials) # Creates a set of arguments per trial
    ]

    return args, [logarithm_divi, logarithm_base], ['Divi', 'Base']



# These are two variations of the mapping function used in visualise to show a palette
# They evaluate to the same value

def logarithm_divi(x, base, p):
    return (log(x, e) / (2 * log(base, e)) + 0.5) ** p

def logarithm_base(x, base, p):
    return (log(x, base) / 2 + 0.5) ** p