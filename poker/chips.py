from copy import deepcopy


class Table(object):

    def __init__(self, players):
        self.pots = [Pot()]
        self.players = players

    def copy(self):
        return deepcopy(self)

    def add_chips(self, amount):
        table = self.copy()
        table.pots[-1].add_chips(amount)
        return table

    def add_side(self, *excluded_players):
        table = self.copy()
        table.pots = table.pots.append(Pot(*excluded_players))
        return table
    
    
class Pot(object):

    def __init__(self, value=0, *excluded_players):
        self.value = value
        self.excluded_players = list(excluded_players)

    def copy(self):
        return deepcopy(self)

    def add_chips(self, amount):
        pot = self.copy()
        pot.value += amount
        return pot
    

class ChipError(Exception):
    pass