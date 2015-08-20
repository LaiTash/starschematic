from library import NOT, Latch
from starschematic import Compound, Transmitter

__author__ = 'Lai Tash'


class NegativeFlipFlop(Compound):
    def __init__(self, *args, **kwargs):
        super(NegativeFlipFlop, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        self.clock = Transmitter(self, 'CLOCK')
        self.data = Transmitter(self, 'DATA')
        self.not_ = NOT(self, '!')
        self.latch1 = Latch(self, '1')
        self.latch2 = Latch(self, 'OUTPUT')
        self.outputs.append(self.latch2)
        self.clock >> self.not_
        self.clock >> self.latch1.enable
        self.data >> self.latch1.data
        self.not_ >> self.latch2.enable
        self.latch1 >> self.latch2.data



