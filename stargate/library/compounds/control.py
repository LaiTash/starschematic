from library import XOR, AND, NOT
from stargate import Compound, Transmitter

__author__ = 'Lai Tash'


class PulseShortener(Compound):
    def __init__(self, ticks, *args, **kwargs):
        super(PulseShortener, self).__init__(*args, **kwargs)
        self.ticks = ticks
        self.build()

    def build(self):
        inp = Transmitter(self, 'SNL')
        not_ = NOT(self, '!')
        inp >> not_
        prev = not_
        for i in range(self.ticks-1):
            repeater = XOR(self, 'R%i' % i)
            prev >> repeater.first
            prev = repeater
        and_ = AND(self, 'PLS')
        prev >> and_.first
        inp >> and_.second
        self.inputs.append(inp.default_input)
        self.outputs.append(and_.default_output)



