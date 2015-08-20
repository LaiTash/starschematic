from stargate import Transmitter

__author__ = 'Lai Tash'


class Machine(object):
    def __init__(self, root, on_tick=None, on_clock=None):
        self.on_tick = on_tick
        self.on_clock = on_clock

        self.root = root
        self.circuit = set()
        self.transmitters = set()

        self.changed_this_tick = set()
        self.tick = 0
        self.clock = 0

        self.reset()

    def reset(self):
        self.circuit = set(self.root.circuit())
        self.transmitters = set([
            node for node in self.circuit if isinstance(node, Transmitter)
        ])
        self.circuit.difference_update(self.transmitters)
        for node in self.circuit:
            node.prepare()

    def before_tick(self):
        for node in self.circuit:
            node.tick()

    def run_clock(self):
        if self.on_clock:
            self.on_clock(self.clock)
        self.clock += 1
        changes = 0
        for node in self.circuit:
            new_state = node.current_state.copy()
            node.switch(new_state, self)
            if new_state != node.current_state:
                if node in self.changed_this_tick:
                    changes = 0
                    break
                else:
                    self.changed_this_tick.add(node)
                    changes += 1
                new_state.apply()
        for transmitter in self.transmitters:
            transmitter.switch(transmitter.current_state, self)
            transmitter.current_state.apply()
        return changes

    def run_tick(self):
        self.changed_this_tick = set()
        self.tick += 1
        self.before_tick()
        while self.run_clock():
            pass
        if self.on_tick:
            self.on_tick(self.tick)

    def run(self, ticks, events=None):
        events = events or {}
        for i in range(ticks):
            for event in events.get(self.tick, []):
                event()
            self.run_tick()
