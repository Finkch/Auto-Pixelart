# This file is an alternative entry point for the program.
# Whereas main runs user-friendly menus, auto is a single
# command line set of arguments.

from sys import argv


def auto(*args):
    r = read_arguments(*args)
    print(r)


# Reads argv as a list, grabbing arguments
# and key-word arguments.
def read_arguments(*args) -> tuple[list, dict]:
    
    largs = []
    kwargs = {}

    # Read every item
    while len(args) > 0:

        # Looks for key-word
        if '--' in args[0]:
            kwargs[args[0][2:]] = args[ 1]
            args = args[2:]
        
        # Regular argument
        else:
            largs.append(args[0])
            args = args[1:]
    
    return largs, kwargs


# Runs main
if __name__ == '__main__':

    # We remove the file name - don't need it
    auto(*argv[1:])