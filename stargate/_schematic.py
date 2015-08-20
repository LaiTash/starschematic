from abc import ABCMeta, abstractproperty, abstractmethod
from collections import OrderedDict
import uuid

__author__ = 'lai'


class NoDefaultOutputError(Exception):
    pass


class NoDefaultInputError(Exception):
    pass


def value(obj):
    try:
        return int(obj)
    except TypeError:
        return obj.value


class State(object):
    values = {}
    output_states = []
    node = None

    def __init__(self, node):
        super(State, self).__setattr__('node', node)
        states = [output.value for output in node.outputs]
        super(State, self).__setattr__('output_states', states)
        super(State, self).__setattr__('values', {})

    def copy(self):
        result = State(self.node)
        result.output_states = self.output_states[:]
        result.values = self.values.copy()
        return result

    def __eq__(self, other):
        return (
            self.node == other.node and
            self.output_states == other.output_states and
            self.values == other.values
        )

    def __setattr__(self, key, value):
        if key in ('node', 'output_states', 'values', 'default_output'):
            super(State, self).__setattr__(key, value)
        else:
            self.values[key] = value

    def __getattr__(self, item):
        try:
            return getattr(super(State, self), item)
        except AttributeError:
            return self.values[item]

    def apply(self):
        for output, state in zip(self.node.outputs, self.output_states):
            output.value = state
        self.node.current_state = self

    @property
    def value(self):
        return int(all(self.output_states))

    @property
    def default_output(self):
        if len(self.output_states) == 1:
            return self.output_states[0]
        raise NoDefaultOutputError()

    @default_output.setter
    def default_output(self, val):
        if len(self.output_states) == 1:
            self.output_states[0] = value(val)
        else:
            raise NoDefaultOutputError()


class Output(object):
    def __init__(self, node, name=None):
        self._name = name
        self.node = node
        self.value = 0
        self.uuid = str(uuid.uuid4())

    def connect(self, input):
        input.connect(self)
        return self

    @property
    def name(self):
        return '%s[%s]' % (self.node.name, self._name if self._name!='output' else '')

    def __rshift__(self, other):
        if isinstance(other, Node):
            other.default_input.connect(self)
            result = other
        elif isinstance(other, Input):
            other.connect(self)
            result = other.node
        else:
            ValueError('Input or Node expected')
        return other

    def __neg__(self):
        return SwitchNOT(self, self.node.parent)

    def __and__(self, other):
        return SwitchAND(self, other, self.node.parent)

    def __or__(self, other):
        return SwitchOR(self, other, self.node.parent)

    def __xor__(self, other):
        return SwitchOR(self, other, self.node.parent)


class Input(object):
    def __init__(self, node, name):
        self._name = name
        self.node = node
        self.inputs = []
        self.uuid = str(uuid.uuid4())
        self._forced = None

    def force(self, value=None):
        """
        Set or remove a forced value. If value is None, remove forced value.

        :param value: forced input value or None
        """
        self._forced = None if value is None else int(bool(value))

    @property
    def value(self):
        if self._forced is not None:
            return self._forced
        return int(any(map(value, self.inputs)))

    def connect(self, signal:Output):
        self.inputs.append(signal)
        return self

    @property
    def name(self):
        return '%s{%s}' % (self.node.name, self._name)


class Node(metaclass=ABCMeta):
    """ Represents a circuit node, everything that has inputs/outputs """

    def __init__(self, parent, name:str=None, ):
        self._name = name
        self._parent = parent
        self.current_state = State(self)
        self.uuid = str(uuid.uuid4())
        self._changed_last_tick = False
        if parent:
            parent.add(self)

    def tick(self):
        pass

    def activate(self):
        raise Exception('Cannot activate')

    def prepare(self):
        for output in self.outputs:
            output.value = 0

    @abstractmethod
    def switch(self, state, machine):
        pass

    @property
    def value(self):
        return value(self.current_state)

    def __neg__(self):
        return SwitchNOT(self, self.parent)

    def __and__(self, other):
        return SwitchAND(self, other, self.parent)

    def __or__(self, other):
        return SwitchOR(self, other, self.parent)


    def __xor__(self, other):
        return SwitchXOR(self, other, self.parent)


    def __getitem__(self, item):
        return self.inputs[item]

    @property
    def parent(self):
        return self._parent

    @property
    def name(self):
        return self._name or repr(self)

    @property
    def container_name(self):
        if self._parent:
            return '%s' % self._parent.fullname
        else:
            return ''

    @property
    def fullname(self):
        if self._parent:
            return '%s.%s' % (self._parent.fullname, self.name)
        else:
            return self.name

    @property
    def default_input(self):
        if len(self.inputs) == 1:
            return self.inputs[0]
        raise NoDefaultInputError()

    @property
    def default_output(self):
        if len(self.outputs) == 1:
            return self.outputs[0]
        raise NoDefaultOutputError()

    @abstractproperty
    def inputs(self):
        return None

    @abstractproperty
    def outputs(self):
        return None

    def __rshift__(self, child):
        output = self.default_output
        if isinstance(child, Node):
            inp = child.default_input
            result = child
        elif isinstance(child, Input):
            inp = child
            result = child.node
        output >> inp
        return result


class AbstractSignaler(Node):
    """ Atom with no inputs and single output """
    def __init__(self, *args, **kwargs):
        self._output = Output(self, 'output')
        super(AbstractSignaler, self).__init__(*args, **kwargs)

    @property
    def outputs(self):
        return [self._output]


class AbstractReceiver(Node):
    """ Atom with no outputs and single input """
    def __init__(self, *args, **kwargs):
        super(AbstractReceiver, self).__init__(*args, **kwargs)
        self._input = Input(self, 'input')

    @property
    def default_input(self):
        return self._input

    @property
    def inputs(self):
        return [self._input]


class Signaler(AbstractSignaler):
    @property
    def inputs(self):
        return []


class Receiver(AbstractReceiver):
    @property
    def outputs(self):
        return []


class SimpleAtom(AbstractSignaler, AbstractReceiver):
    """ Represents an atomic node with one input and one output """
    pass


class MultipleAtom(AbstractSignaler):
    """ Represents an atomic node with one output and multiple inputs """
    input_names = []

    def __init__(self, *args, **kwargs):
        super(MultipleAtom, self).__init__(*args, **kwargs)
        for name in self.input_names:
            setattr(self, name, Input(self, name))

    @property
    def inputs(self):
        return [getattr(self, name) for name in self.input_names]


class FirstSecondAtom(MultipleAtom):
    input_names = ['first', 'second']


class Compound(Node):
    def __init__(self, *args, **kwargs):
        self.children = OrderedDict()
        self._inputs = []
        self._outputs = []

        super(Compound, self).__init__(*args, **kwargs)

    def circuit(self):
        result = []
        for child in self.children.values():
            if isinstance(child, Compound):
                result += child.circuit()
            else:
                result.append(child)
        return result

    def prepare(self):
        for node in self.children.values():
            node.prepare()

    def switch(self, state, machine):
        pass

    def add(self, child):
        if child in self.children.values():
            raise Exception('Child already in a compound')
        if child.name in self.children:
            raise Exception('Child with this name already in a compound')
        self.children[child.name] = child
        return self

    def __getitem__(self, child_name):
        return self.children[child_name]

    @property
    def default_input(self):
        if len(self.inputs) == 1:
            return self.inputs[0]
        raise NoDefaultInputError()

    @property
    def default_output(self):
        if len(self.outputs) == 1:
            return self.outputs[0]
        raise NoDefaultOutputError()

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs


class SwitchNOT(SimpleAtom):
    """ NOT switch """
    def __init__(self, input_, *args, **kwargs):
        self._input_parent = input_
        super(SwitchNOT, self).__init__(*args, **kwargs)
        input_ >> self

    def switch(self, state, machine):
        state.default_output = not value(self.default_input)

    @property
    def name(self):
        super_name = self._name
        if super_name:
            return super_name
        return '!%s' % self._input_parent.name


class SwitchAND(FirstSecondAtom):
    def __init__(self, first, second, *args, **kwargs):
        self._input_parents = [first, second]
        super(SwitchAND, self).__init__(*args, **kwargs)
        first >> self.first
        second >> self.second

    def switch(self, state, machine):
        state.default_output = all(map(value, self.inputs))

    @property
    def name(self):
        super_name = self._name
        if super_name:
            return super_name
        return '(%s & %s)' % (
            self._input_parents[0].name, self._input_parents[1].name
        )


class SwitchOR(FirstSecondAtom):
    def __init__(self, first, second, *args, **kwargs):
        self._input_parents = [first, second]
        super(SwitchOR, self).__init__(*args, **kwargs)
        first >> self.first
        second >> self.second

    def switch(self, state, machine):
        state.default_output = any(map(value, self.inputs))

    @property
    def name(self):
        super_name = self._name
        if super_name:
            return super_name
        return '(%s | %s)' % (self._input_parents[0].name,
                            self._input_parents[1].name)


class SwitchXOR(FirstSecondAtom):
    def __init__(self, first, second, *args, **kwargs):
        self._input_parents = [first, second]
        super(SwitchXOR, self).__init__(*args, **kwargs)
        first >> self.first
        second >> self.second

    def switch(self, state, machine):
        state.default_output = value(self.first) ^ value(self.second)

    @property
    def name(self):
        super_name = self._name
        if super_name:
            return super_name
        return '(%s ^ %s)' % (
            self._input_parents[0].name, self._input_parents[1].name
        )


class Transmitter(SimpleAtom):
    def switch(self, state, machine):
        state.default_output = self.default_input
