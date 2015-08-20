__author__ = 'Lai Tash'


from stargate import Compound, Transmitter
from ..library import AND, NOT, PersistentSwitch, Timer


class LinearCounter(Compound):
    def __init__(self, length, *args, **kwargs):
        super(LinearCounter, self).__init__(*args, **kwargs)
        self.length = length
        self.build()

    def build(self):
        self.enable = Transmitter(self, 'enable')
        self.data = Transmitter(self, 'data')
        self.initializer = self.enable & self.data
        self.not_data = -self.data
        self.face = []
        prev = self.initializer
        ticker = [self.data, self.not_data]
        ticker_i = 0
        for i in range(self.length*2):
            switch = prev >> PersistentSwitch(self, 'switch_%i' % i).on
            self.face.append(switch)
            prev = switch & ticker[ticker_i]
            prev._name = 'and_%i' % i
            ticker_i = int(not(ticker_i))
        for node in self.face:
             self.face[-1] >> node.off
        self._inputs = [self.enable, self.data]

class LinearTimer(Compound):
    def __init__(self, seconds, *args, **kwargs):
        super(LinearTimer, self).__init__(*args, **kwargs)
        self.seconds = seconds
        self.build()

    def build(self):
        self.timer = Timer(self)
        self.counter = LinearCounter(self.seconds, self.parent, 'Face')
        self.face = self.counter.face
        self.timer >> self.counter.data
        self.enable = self.counter.enable
        self._inputs = [self.enable]
