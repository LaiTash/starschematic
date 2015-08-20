from library.compounds.memory import PersistentCell, BinaryCounter, \
    RecetableBinaryCounter
from library.compounds.switches import NegativeFlipFlop
from starschematic import Compound
from starschematic.library import Switch, Button, NOT, AND, Timer
from starschematic.library.compounds.linearcounter import LinearTimer
from starschematic.app import App
from starschematic.library.compounds.keyboards import BitKeyboard, \
    AutoBitKeyboard

root = Compound(None, 'Root')

def keyboard_test():
    keyboard = AutoBitKeyboard(3, 6, root, 'keyboard')

    App(root).run(500, {
        5: [keyboard.buttons[2].activate],
        12: [keyboard.buttons[5].activate],
        #16: [keyboard.reset_button.activate],
        40: [keyboard.buttons[2].activate],
    })


def flipflop_test():
    flipflop = NegativeFlipFlop(root, 'FF')
    button = Button(root, 'clock')
    switch = Switch(root, 'data')
    button >> flipflop.clock
    switch >> flipflop.data

    App(root).run(100, {
        1: [switch.activate],
        10: [button.activate],
        30: [switch.activate],
        40: [button.activate],
    })


def binarycounter_test():
    cell = PersistentCell(4, root, 'MEMORY')
    counter = BinaryCounter(cell, root, 'COUNTER')
    button = Timer(root, 'PUSH')
    button >> counter
    App(root).run(500, {
    })

def recetable_binarycounter_test():
    cell = PersistentCell(4, root, 'MEMORY')
    counter = RecetableBinaryCounter(cell, root, 'COUNTER')
    timer = Timer(root, 'TIME')
    button = Button(root, '(RESET)')
    timer >> counter.input
    button >> counter.reset
    App(root).run(500, {
        100: [button.activate]
    })


def basic_test():
    power = NOT(root, 'POWER')
    and_ = AND(root, 'AND')
    power >> and_.first
    power >> and_.second
    and_2 = AND(root, 'AND2')
    power >> and_2.first
    App(root).run(10)

recetable_binarycounter_test()
#basic_test()
