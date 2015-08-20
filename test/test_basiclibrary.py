from library import AND, PersistentSwitch, Switch
from library import NOT
from machine import Machine
from stargate import Compound
from stargate import value


def setup_function(function):
    global root
    global power
    global not_
    global machine
    machine = Machine(Compound(None))

    root = Compound(None)
    power = NOT(root)
    not_ = -power
    work(power)
    work(not_)


def work(node):
    node.switch(node.current_state, machine)
    node.current_state.apply()


def test_AND():
    and_ = AND(root)
    and_.first.force(1)
    and_.second.force(1)
    work(and_)
    assert value(and_) == 1
    and_.second.force(0)
    work(and_)
    assert value(and_) == 0
    and_.first.force(0)
    work(and_)
    assert value(and_) == 0


def test_PersistentSwitch():
    switch = PersistentSwitch(root)
    switch.prepare()
    work(switch)
    assert value(switch) == 0
    power >> switch.on
    work(switch)
    assert value(switch) == 1
    work(switch)
    assert value(switch) == 1
    power >> switch.off
    work(switch)
    assert value(switch) == 0


def test_Switch():
    machine.tick = 2
    switch = Switch(root)
    switch.prepare()
    switch.default_input.force(0)
    work(switch)
    assert value(switch) == 0
    switch.default_input.force(1)
    work(switch)
    assert value(switch) == 1
    work(switch)
    assert value(switch) == 1
    switch.default_input.force(0)
    work(switch)
    assert value(switch) == 1
    switch.default_input.force(1)
    work(switch)
    assert value(switch) == 0