import mock
from library import NOT
from starschematic import Compound, value, Transmitter


def work(node):
    node.switch(node.current_state, None)
    node.current_state.apply()


def test_SwitchNOT():
    root = Compound(None)
    first = NOT(root)
    second = -first
    first.switch(first.current_state, None)
    first.current_state.apply()
    second.switch(second.current_state, None)
    second.current_state.apply()
    assert value(first) == 1
    assert value(second) == 0


def test_SwitchAND():
    root = Compound(None)
    power = NOT(root)
    not_ = -power
    work(power)
    work(not_)
    and_ = power & power
    work(and_)
    assert value(and_) == 1
    and_1 = power & not_
    work(and_1)
    assert value(and_1) == 0
    and_2 = not_ & not_
    work(and_2)
    assert value(and_2) == 0


def test_SwitchOR():
    root = Compound(None)
    power = NOT(root)
    not_ = -power
    work(power)
    work(not_)
    and_ = power | power
    work(and_)
    assert value(and_) == 1
    and_1 = power | not_
    work(and_1)
    assert value(and_1) == 1
    and_2 = not_ | not_
    work(and_2)
    assert value(and_2) == 0


def test_SwitchXOR():
    root = Compound(None)
    power = NOT(root)
    not_ = -power
    work(power)
    work(not_)
    and_ = power ^ power
    work(and_)
    assert value(and_) == 0
    and_1 = power ^ not_
    work(and_1)
    assert value(and_1) == 1
    and_2 = not_ | not_
    work(and_2)
    assert value(and_2) == 0


def test_Transmitter():
    root = Compound(None)
    power = NOT(root)
    not_ = -power
    work(power)
    work(not_)
    transmitter = Transmitter(root)
    power >> transmitter
    work(transmitter)
    assert value(transmitter) == 1
    transmitter = Transmitter(root)
    not_ >> transmitter
    work(transmitter)
    assert value(transmitter) == 0

