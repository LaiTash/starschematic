from shutil import rmtree
from .machine import Machine
from starschematic.exports.graphviz import GraphBuilder
import os


class App(object):
    def __init__(self, root, target_dir='img'):
        self.root = root
        self.target_dir = target_dir
        try:
            rmtree(target_dir)
        except FileNotFoundError:
            pass
        os.mkdir(target_dir)

    def render(self, tick):
        builder = GraphBuilder()
        graph = builder.visit(self.root)
        graph.render(os.path.join(self.target_dir, str(tick)))

    def run(self, ticks, events=None):
        events = events or {}
        machine = Machine(self.root, self.render)
        machine.run(ticks, events)

