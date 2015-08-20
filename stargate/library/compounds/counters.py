from library import Switch, AND
from library.compounds.control import PulseShortener
from library.compounds.flipflop import FlipFlop
from stargate import Compound, Transmitter


class SyncCounter(Compound):
    def __init__(self, bits_n, *args, **kwargs):
        super(SyncCounter, self).__init__(*args, **kwargs)
        self.bits_n = bits_n
        self.build()

    def build(self):
        logic_compound = Compound(self, 'LOGIC')
        enable = Transmitter(self, 'ENABLE')
        clk = PulseShortener(1, self, 'CLK')
        self.bits = []
        bit = FlipFlop(self, 'B0')
        enable >> bit.enable
        self.bits.append(bit)
        prev = bit
        for i in range(1, self.bits_n):
            bit = FlipFlop(self, 'B%i' % i)
            self.bits.append(bit)
            prev >> bit.enable
            if i != self.bits_n - 1:
                and_ = AND(logic_compound, 'L%i' % i)
                prev >> and_.first
                bit >> and_.second
                prev = and_
        for bit in self.bits:
            clk >> bit.data
        self.enable = enable.default_input
        self.data = clk.default_input






