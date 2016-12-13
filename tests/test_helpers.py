
#This module contains useful helper functions for the unit test suite


#Emulates a multiprocessing Queue
class Q:
    def __init__(self):
        pass

    def put(self, result):
        self.what_was_put = result


#shell object for testing dot property access
class O:
    pass

