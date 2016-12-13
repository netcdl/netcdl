__author__ = 'codyhanson'

from Test import Test

from multiprocessing import Process, Queue

class ActiveTest(Test):

    q = Queue()

    def __init__(self, statement):
        self.active = True
        super(ActiveTest, self).__init__(statement)

    def start(self):
        p = Process(target=self.run, args=(ActiveTest.q,))
        p.start()
        return p

    @staticmethod
    def get_from_queue():
        return ActiveTest.q.get()

