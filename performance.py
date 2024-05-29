# This file is to run tests to determine performance

from time import process_time as timer

# This class contains the tools to test performance
class Test:

    runtimes    = []
    starts      = []
    ends        = []


    def __init__(self, fxn, name, trials = 10, print_individual = False):
        self.fxn                = fxn
        self.name               = name
        self.trials             = trials

        # Whether or not to print status during each trial
        self.print_individual   = print_individual

    # Calling this function begins a test
    def __call__(self, *args):

        # Clears timing lists, in case of multiple consecutive trials
        self.reset()

        # Notifies user that the trials have begun
        self.begin_printout()

        # Run all the trials
        for trial in range(self.trials):
            self.begin() # Checks time

            # Calls the function to be tested, unpacking arguments into it
            self.fxn(*args)

            self.end() # Checks time

            # Performs mid-trial printout, if necessary
            if self.print_individual:
                self.trial_printout()

        # Notifies user of the results and that the test has ended
        self.end_prinout()


    # begin() and end() check the time
    def begin(self):
        self.starts.append(timer())

    def end(self):
        self.ends.append(timer())
        self.runtimes.append(self.ends[-1] - self.starts[-1])
    

    # Printouts
    def begin_printout(self):
        print(f'Being trial of {self.name}!')

    def trial_printout(self):
        print(f'\t[{len(self.runtimes)}/{self.trials}]\t-\t{self.runtimes[-1]} s')

    def end_prinout(self):
        print(f'End trial of {self.name}!')
        self.results()
        print()

    def results(self):
        print(f'{self.name} average time:\t{sum(self.runtimes) / len(self.runtimes)} s')
        print(f'{self.name} real time to run {len(self.runtimes)} trials:\t{self.ends[-1] - self.starts[0]} s')


    # Clears trials times
    def reset(self):
        self.runtimes   = []
        self.starts     = []
        self.ends       = []