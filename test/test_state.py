from unittest import TestCase
from _schematic import State


class VirtualOutput(object):
    def __init__(self, value):
        self.value = value


class VirtualNode(object):
    outputs = [VirtualOutput(1), VirtualOutput(2), VirtualOutput(3)]


class TestState(TestCase):
    def setUp(self):
        self.node = VirtualNode()
        self.state = State(self.node)

    def test_copy(self):
        new_state = self.state.copy()
        assert new_state.output_states == self.state.output_states
        assert new_state.values == self.state.values
        assert new_state.node is self.state.node
        assert new_state.output_states is not self.state.output_states
        assert new_state.values is not self.state.values

    def test_apply(self):
        new_state = self.state.copy()
        new_state.output_states[0] = 3
        new_state.apply()
        assert self.node.current_state is new_state
        assert self.node.outputs[0].value == 3

    def test_value(self):
        assert self.state.value == 1
        self.state.output_states[0] = 0
        assert self.state.value == 0
        self.state.output_states[1] = 0
        self.state.output_states[2] = 0
        assert self.state.value == 0

    def test_default_output(self):
        self.state.output_states = [1]
        assert self.state.default_output == 1
