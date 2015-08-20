from library import Button, PersistentSwitch
from library.compounds.linearcounter import LinearTimer
from library.compounds.memory import PersistentCell, CellsIndicator, \
    RecetablePersistentCell
from starschematic import Compound

__author__ = 'Lai Tash'


class BitKeys(Compound):
    def __init__(self, cell, *args, **kwargs):
        super(BitKeys, self).__init__(*args, **kwargs)
        self.cell = cell
        self.build()

    def build(self):
        self.buttons = []
        for i, bit in enumerate(self.cell.bits):
            button = Button(self, 'k%i' % i)
            button >> bit.on
            self.buttons.append(button)


class BitKeyboard(Compound):
    def __init__(self, bits_n, *args, **kwargs):
        super(BitKeyboard, self).__init__(*args, **kwargs)
        self.bits_n = bits_n
        self.build()

    def build(self):
        self.cell = RecetablePersistentCell(self.bits_n, self, 'MEMORY')
        self.keys = BitKeys(self.cell, self, 'KEYBOARD')
        self.buttons = self.keys.buttons
        self.screen = CellsIndicator(self.cell, self, 'SCREEN')
        self.reset = self.cell.reset
        self.reset_button = Button(self, 'RESET')
        self.reset_button >> self.reset
        self.bits = self.cell.bits


class AutoBitKeyboard(BitKeyboard):
    def __init__(self, seconds, *args, **kwargs):
        self.seconds = seconds
        super(AutoBitKeyboard, self).__init__(*args, **kwargs)

    def build(self):
        super(AutoBitKeyboard, self).build()
        self.reset_timer = LinearTimer(self.seconds, self, 'TIMER')
        self.reset_enable_switch = PersistentSwitch(self, 'TIMER_TRIGGER')
        self.reset_enable_switch >> self.reset_timer
        self.reset_timer.face[-1] >> self.reset
        for button in self.buttons:
            button >> self.reset_enable_switch.on
