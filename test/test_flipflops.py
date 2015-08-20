from library.compounds.flipflop import DFlip
from startest._startest import StarTest, at, startest

__author__ = 'Lai Tash'


class DFlipTest(StarTest):
    def each_tick(self, tick):
        self.view('dflip_each')

    @at(5)
    def at_3(self):
        self.dflip.data.force(0)

    @at(10)
    def at_5(self):
        self.dflip.data.force(1)


cls=startest(DFlipTest)
def test_dflip(cls):
    dflip = DFlip(cls.root, 'D-Flip')
    dflip.data.force(1)
    dflip.clock.force(1)
    cls.dflip = dflip
    cls.run_machine(15)
