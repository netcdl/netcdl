from ActiveTest import ActiveTest
from multiprocessing import Queue
import time

def mock_run(self, q):
    self.success = True
    self.result_detail = 'mock detail'
    return q.put(self.create_result())

class TestActiveTest:
    def test_ctor(self):
        at = ActiveTest('statement')
        assert at.statement == 'statement'
        assert type(at.q) == type(Queue())
        assert at.success == False

    def test_start_and_get_from_q(self):
        at = ActiveTest('statement')
        return

        #mock a 'run' function
        at.run = mock_run

        process = at.start()

        time.sleep(1)

        result = ActiveTest.get_from_queue()
        assert result.success == True
        assert result.result_detail == 'mock detail'
