from abc import ABCMeta, abstractmethod, abstractproperty
from collections import OrderedDict

__author__ = 'lai'


class NoDefaultOutputError(Exception):
    pass


class NoDefaultInputError(Exception):
    pass


class Output(object):
    def __init__(self, node, name=None):
        self._name = name
        self.node = node

    def connect(self, input):
        input.connect(self)
        return self

    @property
    def name(self):
        return '%s[%s]' % (self.node.name, self)

    def __rshift__(self, other):
        if isinstance(other, Node):
            other.default_input.connect(self)
        elif isinstance(other, Input):
            other.connect(self)
        else:
            ValueError('Input or Node expected')
        return other


class Input(object):
    def __init__(self, node, name):
        self._name = name
        self.node = node
        self.inputs = []

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
        raise NoDefaultInputError()

    @property
    def default_output(self):
        raise NoDefaultOutputError()

    def __rshift__(self, child):
        output = self.default_output
        inp = child.default_input
        inp.connect(output)
        return self


class Signaler(Node):
    """ Atom with no inputs and single output """
    def __init__(self, *args, **kwargs):
        super(Signaler, self).__init__(*args, **kwargs)
        self._output = Output(self, 'output')

    @property
    def default_output(self):
        return self._output


class Receiver(Node):
    """ Atom with no outputs and single input """
    def __init__(self, *args, **kwargs):
        super(Receiver, self).__init__(*args, **kwargs)
        self._input = Input(self, 'input')

    @property
    def default_input(self):
        return self._input



class SimpleAtom(Signaler, Receiver):
    """ Represents an atomic node with one input and one output """
    pass


class MultipleAtom(Signaler):
    """ Represents an atomic node with one output and multiple inputs """
    input_names = []

    def __init__(self, *args, **kwargs):
        super(MultipleAtom, self).__init__(*args, **kwargs)
        for name in self.input_names:
            setattr(self, name, Input(self, name))


class FirstSecondAtom(Signaler):
    input_names = ['first', 'second']


class Compound(Node):
    def __init__(self, *args, **kwargs):
        super(Compound, self).__init__(*args, **kwargs)
        self.children = OrderedDict()

    def add(self, child):
        if child in self.children.items():
            raise Exception('Child already in a compound')
        childlist = self.children.get(child.name)
        if childlist is None:
            childlist = []
        childlist.append(child)
        return self

    def __getitem__(self, child_name):
        return


class NOT(SimpleAtom):
    """ NOT switch """
    def __init__(self, input, *args, **kwargs):
        super(NOT, self).__init__(*args, **kwargs)
        self._input_parent = input
        input >> self

    @property
    def name(self):
        super_name = self._name
        if super_name:
            return super_name
        return '!%s' % self._input_parent.name