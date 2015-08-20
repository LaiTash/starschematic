from library import Timer
from library.compounds.counters import SyncCounter
from startest._startest import StarTest, startest

__author__ = 'Lai Tash'


class SyncCounterTest(StarTest):
    def each_tick(self, tick):
        self.view('syncc')

cls = startest(SyncCounterTest)
def test_SyncCounter(cls):
    timer = Timer(cls.root, 'timer')
    counter = SyncCounter(4, cls.root, 'counter')
    counter.enable.force(1)
    timer >> counter.data
    cls.run_machine(400)