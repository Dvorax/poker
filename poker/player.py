from poker.utility import Collection
from poker.card import Cards
from poker.chips import ChipError
from copy import deepcopy


class Player(object):

    def __init__(self, name, pocket=Cards(), chips=0):
        self.name = name
        self.pocket = pocket
        self.chips = chips
        self.last_action = None
    
    def _clone(self):
        return deepcopy(self)
    
    def bet(self, amount):
        if self.chips < amount:
            raise ChipError('Player does not have enough chips.')
        
        player = self._clone()
        player.chips -= amount
        return player
            
    def won(self, amount):
        player = self._clone()
        player.chips += amount
        return player
    
    def give_card(self, card):
        player = self._clone()
        player.pocket = player.pocket.add(card)
        return player
    
    def empty_pocket(self):
        player = self._clone()
        player.pocket = Cards()
        return player

    def __repr__(self):
        return str(self.name)


class Players(Collection):

    def __init__(self, *players):
        super(Players, self).__init__(*players)

    def rotate(self):
        players = self._copy()
        players.items = players[1:] + players[:1]
        return players

    def big_blind(self):
        return self[0]

    def little_blind(self):
        return self[1]

    def has_human(self):
        pass