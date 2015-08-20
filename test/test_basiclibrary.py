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
    power >> and_.first
    power >> and_.second
    work(and_)
    assert value(and_) == 1
    and_1 = AND(root)
    power >> and_1.first
    not_ >> and_1.second
    work(and_1)
    assert value(and_1) == 0
    and_2 = not_ & not_
    not_ >> and_2.first
    not_ >> and_2.second
    work(and_2)
    assert value(and_2) == 0


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
    power_switch = Switch(root)
    power_switch.prepare()
    power_switch.activate()
    switch = Switch(root)
    switch.prepare()
    work(switch)
    assert value(switch) == 0
    power_switch >> switch
    work(power_switch)
    work(switch)
    assert value(switch) == 1
    work(switch)
    assert value(switch) == 1
    power_switch.activate()
    work(power_switch)
    work(switch)
    assert value(switch) == 1
    power_switch.activate()
    work(power_switch)
    work(switch)
    assert value(switch) == 0