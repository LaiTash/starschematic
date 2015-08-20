from library.compounds.control import PulseShortener
from startest._startest import StarTest, startest


class ShortenerTestCls(StarTest):
    def each_clock(self, clock):
        self.view('shortener', clock)


cls = startest(ShortenerTestCls)
def test_shortener(cls):
    shortener = PulseShortener(5, cls.root, 'S')
    shortener.default_input.force(1)
    cls.run_machine(10)

