from library import Timer
from library.compounds.counters import SyncCounter, CounterResetter
from startest._startest import StarTest, startest, at

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
    cls.run_machine(4)


class CounterResetterTest(StarTest):
    #@at(40)
    #def at_40(self):
    #    self.resetter.counter.enable.force(0)

    @at(50)
    def at_50(self):
        self.resetter.counter.enable.force(0)
        self.resetter.default_input.force(1)

    def each_tick(self, tick):
        self.view('syncc')

counter_resetter_test = startest(CounterResetterTest)
def test_CounterResetterTest(counter_resetter_test):
    timer = Timer(counter_resetter_test.root, 'timer')
    counter = SyncCounter(4, counter_resetter_test.root, 'counter')
    counter.enable.force(1)
    timer >> counter.data
    counter_resetter_test.resetter = CounterResetter(
        counter, counter_resetter_test.root, 'RESETTER'
    )
    counter_resetter_test.run_machine(400)

