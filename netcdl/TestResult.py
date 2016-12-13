__author__ = 'codyhanson'

from fabulous.color import highlight_red, highlight_green


class TestResult:
    def __init__(self, passed, display_str, result_detail):
        self.passed = passed
        self.display_str = display_str
        self.result_detail = result_detail

    def log(self):
        if self.passed:
            print highlight_green(self.display_str)
        else:
            print highlight_red(self.display_str)
