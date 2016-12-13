__author__ = 'codyhanson'


class Report:
    def __init__(self):
        self.results = []

    def record_result(self, result):
        if result is None:
            return
        self.results.append(result)

    def log(self):
        print "Logging results list:"
        success = 0
        failed = 0
        for result in self.results:
            result.log()
            if result.passed:
                success += 1
            else:
                failed += 1

        print "Passed: {0}/{1}".format(success, success + failed)
