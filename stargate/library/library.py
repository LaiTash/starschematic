from stargate import Signaler, Receiver, MultipleAtom, SimpleAtom
from stargate import FirstSecondAtom
from stargate import value


class AND(FirstSecondAtom):
    def switch(self, state, machine):
        state.default_output = all(map(value, self.inputs))


class NOT(SimpleAtom):
    def switch(self, state, machine):
        state.default_output = not value(self.default_input)


class OR(FirstSecondAtom):
    def switch(self, state, machine):
        state.default_output = any(map(value, self.inputs))


class XOR(FirstSecondAtom):
    def switch(self, state, machine):
        state.default_output = value(self.first) ^ value(self.second)


class Button(Signaler):
    ticks = 10

    def prepare(self):
        super(Button, self).prepare()
        self.ticks_left = 0

    def activate(self):
        self.ticks_left = self.ticks

    def tick(self):
        self.ticks_left -= 1

    def switch(self, state, machine):
        state.default_output = self.ticks_left > 0


class PersistentSwitch(MultipleAtom):
    input_names = ['off', 'on']

    def prepare(self):
        super(PersistentSwitch, self).prepare()
        self.current_state.previous_states = 0

    def switch(self, state, machine):
        prev = state.previous_states
        current_state = value(self.on) | value(self.off)<<1
        if current_state in (3, 2) and prev in (0, 1):
            current_state = 2
        elif current_state in (3, 1) and prev in (0, 2):
            current_state = 1
        else:
            current_state = state.default_output
        state.previous_states = value(self.on) | value(self.off)<<1
        state.default_output = current_state & 1


class Informer(Receiver):
    @property
    def value(self):
        return self.default_input.value

    def switch(self, state, machine):
        pass

class Switch(SimpleAtom):
    def prepare(self):
        super(Switch, self).prepare()
        self.current_state._state = 0
        self.current_state.previous_input = 0

    def activate(self, state=None):
        state = state or self.current_state
        state._state = int(not state._state)
        state.default_output = state._state

    def switch(self, state, machine):
        nomatch = state.previous_input == 0 and value(self.default_input) == 1
        is_first_tick = machine.tick == 1
        if nomatch and not is_first_tick:
            self.activate(state)
        state.previous_input = value(self.default_input)


class EnabledSwitch(Switch):
    def prepare(self):
        super(EnabledSwitch, self).prepare()
        self.activate()


class Timer(SimpleAtom):
    ticks = 10

    def prepare(self):
        super(Timer, self).prepare()
        self.current_ticks = 0

    def tick(self):
        if not self.default_input.value:
            self.current_ticks -= 1
        if self.current_ticks == -self.ticks:
            self.current_ticks = self.ticks

    def switch(self, state, machine):
        state.default_output = self.current_ticks > 0


class Latch(MultipleAtom):
    input_names = ['enable', 'data']
    def switch(self, state, machine):
        if value(self.enable):
            state.default_output = self.data