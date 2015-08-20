from library import Latch, XOR
from stargate import Compound


class JKFlipFlop(Compound):
    def __init__(self, *args, **kwargs):
        super(JKFlipFlop, self).__init__(*args, **kwargs)
        self.build()

    def build(self):
        latch = Latch(self, 'JK')
        xor = XOR(self, 'x')
        self.J = xor.first
        self.K = xor.second
        self.data = latch.data
        self.inputs += [self.J, self.K, latch.data]
        self.outputs.append(latch)
        xor >> latch.enable

