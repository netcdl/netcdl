
from TestResult import TestResult
from Report import Report



def test_record_result():
    tr1 = TestResult(False, 'failed', 'failed detail')
    tr2 = TestResult(True, 'testing', 'testing detail')
    tr3 = None
    r = Report()
    r.record_result(tr1)
    r.record_result(tr2)
    r.record_result(tr3)
    assert len(r.results) == 2
    assert r.results[0] is tr1
    assert r.results[1] is tr2
    r.log()

