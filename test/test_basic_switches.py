from library import NOT
from stargate import Compound, value, Transmitter


def setup_function(function):
    global root
    global power
    global not_

    root = Compound(None)
    power = NOT(root)
    not_ = -power
    work(power)
    work(not_)


def work(node):
    node.switch(node.current_state, None)
    node.current_state.apply()


def test_SwitchNOT():
    assert value(power) == 1
    assert value(not_) == 0

def test_SwitchAND():
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
    and_ = power ^ power
    work(and_)
    assert value(and_) == 0
    and_1 = power ^ not_
    work(and_1)
    assert value(and_1) == 1
    and_2 = not_ ^ not_
    work(and_2)
    assert value(and_2) == 0


def test_Transmitter():
    transmitter = Transmitter(root)
    power >> transmitter
    work(transmitter)
    assert value(transmitter) == 1
    transmitter = Transmitter(root)
    not_ >> transmitter
    work(transmitter)
    assert value(transmitter) == 0
