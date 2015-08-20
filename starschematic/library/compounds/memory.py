from library import Latch, Switch, PersistentSwitch, NOT, Informer
from library.library import EnabledSwitch
from starschematic import Compound, Transmitter

__author__ = 'Lai Tash'


class PersistentCell(Compound):
    def __init__(self, bits, *args, **kwargs):
        super(PersistentCell, self).__init__(*args, **kwargs)
        self.bits_n = bits
        self.build()

    def build(self):
        self.bits = []
        for bit_i in range(self.bits_n):
            bit = PersistentSwitch(self, 'bit_%i' % bit_i)
            self.bits.append(bit)

class RecetablePersistentCell(PersistentCell):
    def build(self):
        super(RecetablePersistentCell, self).build()
        self.reset = Transmitter(self, 'RESET')
        self.inputs.append(self.reset)
        self.reset_switch = PersistentSwitch(self, 'RESETSWITCH')
        self.reset >> self.reset_switch.on
        self.complete_indicator = NOT(self, 'COMPLETE')
        for bit in self.bits:
            self.reset_switch >> bit.off
            bit >> self.complete_indicator
        self.complete_indicator >> self.reset_switch.off


class CellsAND(Compound):
    def __init__(self, cell1, cell2, *args, **kwargs):
        super(CellsAND, self).__init__(*args, **kwargs)
        assert len(cell1.bits) == len(cell2.bits)
        self.cell1, self.cell2 = cell1, cell2

        if not self._name:
            label1 = (self.cell1.name if self.cell1.parent == self.parent
                      else self.cell1.fullname)
            label2 = (self.cell2.name if self.cell2.parent == self.parent
                      else self.cell2.fullname)
            self._name = '%s & %s' % (label1, label2)

        self.build()

    def build(self):
        self.bits = []
        for i,(bit1, bit2) in enumerate(zip(self.cell1.bits, self.cell2.bits)):
            bit = bit1 & bit2
            bit._name = 'bit%i' % i
            self.bits.append(bit)

class CellsXOR(Compound):
    def __init__(self, cell1, cell2, *args, **kwargs):
        super(CellsXOR, self).__init__(*args, **kwargs)
        assert len(cell1.bits) == len(cell2.bits)
        self.cell1, self.cell2 = cell1, cell2
        if not self._name:
            label1 = (self.cell1.name if self.cell1.parent == self.parent
                      else self.cell1.fullname)
            label2 = (self.cell2.name if self.cell2.parent == self.parent
                      else self.cell2.fullname)
            self._name = '%s ^ %s' % (label1, label2)
        self.build()

    def build(self):
        self.bits = []
        for i,(bit1, bit2) in enumerate(zip(self.cell1.bits, self.cell2.bits)):
            bit = bit1 ^ bit2
            bit._name = 'bit%i' % i
            self.bits.append(bit)

class CellsEquality(Compound):
    def __init__(self, cell1, cell2, *args, **kwargs):
        super(CellsEquality, self).__init__(*args, **kwargs)
        assert len(cell1.bits) == len(cell2.bits)
        self.cell1, self.cell2 = cell1, cell2
        if not self._name:
            label1 = (self.cell1.name if self.cell1.parent == self.parent
                      else self.cell1.fullname)
            label2 = (self.cell2.name if self.cell2.parent == self.parent
                      else self.cell2.fullname)
            self._name = '%s == %s' % (label1, label2)
        self.build()

    def build(self):
        self.xor = CellsXOR(self.cell1, self.cell2, self)
        self.NOT = NOT(self, 'EQUALS')
        for bit in self.xor.bits:
            bit >> self.NOT
        self.outputs.append(self.NOT)


class CellsIndicator(Compound):
    def __init__(self, cell, *args, **kwargs):
        super(CellsIndicator, self).__init__(*args, **kwargs)
        self.cell = cell
        self.build()

    def build(self):
        self.bits = []
        for i, bit in enumerate(self.cell.bits):
            self.bits.append(bit >> Informer(self, 'bit%i' % i))


class BinaryCounter(Compound):
    def __init__(self, cell, *args, **kwargs):
        super(BinaryCounter, self).__init__(*args, **kwargs)
        self.cell = cell
        self.build()

    def build(self):
        switches = Compound(self, 'SWITCHES')
        self.logic = Compound(self, 'LOGIC')
        self.input = Transmitter(self, 'INPUT')
        self.inputs.append(input)
        prev_switch = None
        self.switches = []
        for i, bit in enumerate(self.cell.bits):
            switch = Switch(switches, 'S%i' % i)
            self.switches.append(switch)
            switch >> bit.on
            (-switch) >> bit.off
            if prev_switch:
                not_ = NOT(self.logic, 'L%i' % i)
                prev_switch >> not_
                not_ >> switch
            else:
                self.input >> switch
            prev_switch = switch


class RecetableBinaryCounter(BinaryCounter):
    def build(self):
        super(RecetableBinaryCounter, self).build()
        reset = PersistentSwitch(self, 'RESET')
        self.reset = reset.on
        complete_flag = NOT(self, 'RESET_COMPLETE')
        complete_flag >> reset.off
        self.inputs.append(reset.on)
        for i, bit in enumerate(self.cell.bits):
            switch = self.switches[i]
            and_ = reset & bit
            and_._name = 'R%i' % i
            and_ >> switch
            and_ >> bit.off
            bit >> complete_flag



