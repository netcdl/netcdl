__author__ = 'codyhanson'

import logging
from TestResult import TestResult


class Test(object):
    def __init__(self, statement):
        self.logger = logging.getLogger(__name__)
        self.statement = statement
        self.success = False
        if not hasattr(self, 'display_str'):
            self.display_str = 'display'
        if not hasattr(self, 'result_detail'):
            self.result_detail = 'default detail'

    def create_result(self):
        return TestResult(self.success, self.display_str, self.result_detail)

    def __str__(self):
        return "{0} success:{1} detail:{2}".format(self.display_str, self.success, self.result_detail)
