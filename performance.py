# This file is to run tests to determine performance

from time import time_ns as timer
from logger import logger

from performance_tests.test_logarithms import test_logarithms

performance_functions = [test_logarithms]
performance_names = ['Logarithms']



def test_performance():
    
    tests = [test_logarithms]
    names = ['Logarithms']

    



# This class contains several functions to test against each other
class Tests:
    def __init__(self, fxns, names, trials = 10, printout = False) -> None:

        # Creates a test instance for each function supplied
        self.tests = [Test(fxns[i], names[i], trials=trials, printout=printout)
                      for i in range(len(fxns))]
    
    # Calling this class begins running all tests
    def __call__(self, *args, params_per_trial = False):

        # Runs tests
        if params_per_trial:
            for params in args:
                for test in self.tests:
                    test(*params)
        else:
            for test in self.tests:
                test(*args)

        # Returns the results of the tests
        return self.get_results()

    # Returns the results as a string
    def get_results(self):
        results = []

        # The important stuff goes at the top of the file
        for test in self.tests:
            results.append(f'\t-- {test.name} --\n')
            results.append(test.results())
            results.append('\n\n')

        # For delimination 
        results.append(f'\n-------------------------------\n\n')

        # Nitty-gritty goes at the bottom
        for test in self.tests:
            results += test.get_results()
            results.append('\n\n')
        
        return results


# This class contains the tools to test performance
class Test:

    runtimes    = []
    starts      = []
    ends        = []


    def __init__(self, fxn, name, trials = 10, printout = False) -> None:
        self.fxn        = fxn # The function that will be tested
        self.name       = name
        self.trials     = trials

        # Whether or not to print status during each trial
        self.printout   = printout

    # Calling this function begins a test
    def __call__(self, *args) -> None:

        # Clears timing lists, in case of multiple consecutive trials
        self.reset()

        # Notifies user that the trials have begun
        if self.printout:
            print(self.begin_printout())

        # Run all the trials
        for trial in range(self.trials):
            self.begin() # Checks time

            # Calls the function to be tested, unpacking arguments into it
            self.fxn(*args)

            self.end() # Checks time

            # Performs mid-trial printout
            if self.printout:
                print(self.trial_printout())

        # Notifies user of the results and that the test has ended
        if self.printout:
            print(self.end_prinout())


    # begin() and end() check the time
    def begin(self):
        self.starts.append(timer())

    def end(self):
        self.ends.append(timer())
        self.runtimes.append(self.ends[-1] - self.starts[-1])
    

    # Printouts
    def begin_printout(self):
        return f'Being {self.name}:'

    def trial_printout(self, i = -1):
        if i == -1:
            return f'\t[{len(self.runtimes)}/{self.trials}]\t-\t{self.runtimes[i] / (10 ** 9)} s'
        return f'\n\t[{i}/{self.trials}]\t-\t{self.runtimes[i] / (10 ** 9)} s'

    def end_prinout(self):
        return f'\nEnd {self.name}.\n{self.results()}\n'
    
    def results(self):
        return f'''{self.name} average time:\t\t\t\t{sum(self.runtimes) / len(self.runtimes) / (10 ** 9)} s\n{self.name} real time to run {len(self.runtimes)} trials:\t{(self.ends[-1] - self.starts[0]) / (10 ** 9)} s'''
    
    # Returs the results as a list
    def get_results(self):
        results = []

        results.append(self.begin_printout())

        for trial in range(self.trials):
            results.append(self.trial_printout(trial))
        
        results.append(self.end_prinout())

        return results


    # Clears trials times
    def reset(self):
        self.runtimes   = []
        self.starts     = []
        self.ends       = []