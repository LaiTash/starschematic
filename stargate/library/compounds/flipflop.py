from library import NOT, Latch, AND, Switch
from stargate import Compound, Transmitter

__author__ = 'Lai Tash'


class FlipFlop(Compound):
    def __init__(self, *args, **kwargs):
        super(FlipFlop, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        and_ = AND(self, '&')
        switch = Switch(self, 'F')
        and_ >> switch
        self.enable = and_.first
        self.data = and_.second
        self.switch = switch
        self.inputs.extend([self.enable, self.data, self.switch])
        self.outputs.append(switch.default_output)



class DFlip(Compound):
    def __init__(self, *args, **kwargs):
        super(DFlip, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        not_ = NOT(self, '!')
        latch1 = Latch(self, 'L1')
        latch2 = Latch(self, 'L2')
        clock = Transmitter(self, 'CLK')
        data = Transmitter(self, 'DTA')
        clock >> not_
        clock >> latch1.enable
        data >> latch1.data
        not_ >> latch2.enable
        latch1 >> latch2.data
        self.output = latch2.default_output
        self.clock = clock.default_input
        self.data = data.default_input
        self.inputs.extend([self.clock, self.data])
        self.outputs.append(self.output)


