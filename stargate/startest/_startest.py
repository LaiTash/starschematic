import os
from unittest import TestCase
from _pytest.tmpdir import tmpdir
import pytest
from exports.graphviz import GraphBuilder
from machine import Machine
from stargate import Compound

__author__ = 'Lai Tash'

def startest(cls):
    @pytest.fixture
    def startest(request):
        tmp = tmpdir(request)
        t = cls(tmp)
        return t
    return startest

def at(*ticks):
    def _at(method):
        def _wr(self):
            method(self)
        _wr.ticks = ticks
        return _wr
    return _at


class StarTest(object):
    def __init__(self, tmpdir):
        self.tmpdir = str(tmpdir)
        self.root = Compound(None, 'root')
        self.events = {}
        for meth_name in dir(self):
            meth = getattr(self, meth_name)
            ticks = getattr(meth, 'ticks', None)
            if ticks is not None:
                for tick in ticks:
                    events = self.events.get(tick, [])
                    events.append(meth)
                    self.events[tick] = events

    def each_tick(self, tick):
        pass

    def get_total_ticks(self):
        return max(self.events.keys() or [0]) + 1

    def run_machine(self, ticks=None):
        self.machine = Machine(self.root, on_tick=self.each_tick)
        self.machine.run(ticks or self.get_total_ticks(), self.events)

    def view(self, prefix):
        builder = GraphBuilder()
        graph = builder.visit(self.root)
        graph.render(os.path.join(self.tmpdir,
                                  'prefix_%i' % self.machine.tick))