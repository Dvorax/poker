# -*- coding: utf-8 -*-

import random
from poker.utility import Collection


def _find_multiples(cards, length=0, limit=0):
    # organize into ranks
    rank_cards = {}
    for card in cards:
        if card.rank in rank_cards:
            rank_cards[card.rank] = rank_cards[card.rank].add(card)
        else:
            rank_cards[card.rank] = Cards(card)
    
    # filter for length
    multiples = []
    for rank in rank_cards:
        if (length == 0 and len(rank_cards[rank]) >= 2 or
                0 < length == len(rank_cards[rank])):
            multiples.append(rank_cards[rank])
    
    # return desired amount
    if 1 < limit <= len(multiples):
        return multiples[-limit:]
    elif limit == 1 and len(multiples) >= 1:
        return multiples[-1]
    else:
        return multiples


def _find_flush(cards):
    """Returns the Cards that create the longest Flush"""

    suit_cards = {}
    for card in cards:
        if card.suit in suit_cards:
            suit_cards[card.suit] = suit_cards[card.suit].add(card)
        else:
            suit_cards[card.suit] = Cards(card)

    return max(suit_cards.values(), key=len)


def _find_straight(cards):
    """Returns the Cards that create the longest Straight"""

    straights = {}
    for card in cards:
        for high_rank in straights_by_high_rank(card.rank):
            if high_rank in straights:
                straights[high_rank] = straights[high_rank].add(card)
            else:
                straights[high_rank] = Cards(card)

    return max(straights.values(), key=len)


def straights_by_high_rank(card_rank):
    """
    Straights table organized by card ranks:
    5   6   7   8   9  10   J   Q   K   A
    4   5   6   7   8   9  10   J   Q   K
    3   4   5   6   7   8   9  10   J   Q
    2   3   4   5   6   7   8   9  10   J
    A   2   3   4   5   6   7   8   9  10

    Returns the high card ranks for the straights the rank is in
    """
    if card_rank < 5:
        return list(range(5, card_rank + 5))
    elif 5 <= card_rank <= 10:
        return list(range(card_rank, card_rank + 5))
    elif card_rank < 14:
        return list(range(card_rank, 14 + 1))
    else:
        return [5, 14]


class Card(object):

    ranks = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
             10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}

    # suits = {0: '♣', 1: '♦', 2: '♥', 3: '♠'}
    # suits = {0: '§', 1: '¨', 2: '©', 3: 'ª'}
    # suits = {0: ']', 1: '[', 2: '{', 3: '}'}
    suits = {0: 'C', 1: 'D', 2: 'H', 3: 'S'}

    rank_names = {2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six',
                  7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Jack',
                  12: 'Queen', 13: 'King', 14: 'Ace'}

    suit_names = {0: 'Club', 1: 'Diamond', 2: 'Heart', 3: 'Spade'}

    straight_high_ranks = range(5, 14 + 1)

    def __init__(self, rank, suit):
        if rank not in Card.ranks or suit not in Card.suits:
            raise CardError('Invalid card values')

        self.rank = rank
        self.suit = suit

    def rank_from_zero(self):
        return self.rank - 2

    def rank_name(self):
        return Card.rank_names[self.rank]

    def suit_name(self):
        return Card.suit_names[self.suit]

    def straights_by_high_rank(self):
        return straights_by_high_rank(self.rank)

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return type(other) is Card and self.rank == other.rank and \
            self.suit == other.suit

    def __le__(self, other):
        return self.rank <= other.rank

    def __ge__(self, other):
        return self.rank >= other.rank

    def __ne__(self, other):
        return type(other) is not Card or self.rank != other.rank or \
            self.suit != other.suit

    def __repr__(self):
        return Card.ranks[self.rank] + Card.suits[self.suit]

    def __hash__(self):
        return 13 * self.suit + self.rank_from_zero()


class Cards(Collection):

    def __init__(self, *cards):
        super(Cards, self).__init__(*cards)

    def ranks_represented(self):
        ranks = [card.rank for card in self.items]
        return set(ranks)

    def suits_represented(self):
        suits = [card.suit for card in self.items]
        return set(suits)

    def multiples(self, length, limit=0):
        return _find_multiples(self, length, limit)

    def singlets(self, limit=0):
        return _find_multiples(self, 1, limit)

    def pairs(self, limit=0):
        return _find_multiples(self, 2, limit)

    def triplets(self, limit=0):
        return _find_multiples(self, 3, limit)

    def quadruplets(self, limit=0):
        return _find_multiples(self, 4, limit)

    def flush(self):
        return _find_flush(self)

    def straight(self):
        return _find_straight(self)

    def kicker_value(self):
        """Returns a number between 0 and 1
        This number indicates the value of the cards as a kicker"""

        number_of_ranks = 13
        total_possible = pow(number_of_ranks, len(self.items))

        total = 0
        for i, card in enumerate(sorted(self.items)):
            total += number_of_ranks ** i * card.rank_from_zero()

        return 1.0 * total / total_possible


class Deck(Cards):

    def __init__(self, *cards):
        if len(cards) == 0:
            cards = [Card(rank, suit) for suit in Card.suits
                     for rank in Card.ranks]
        super(Deck, self).__init__(*cards)
        self.discard = []

    def shuffle(self):
        result = self._copy()
        random.shuffle(result.items)
        return result

    def draw_random(self):
        if len(self.items) > 0:
            card = random.choice(self.items)
            self.draw_card(card)
            return card
        else:
            raise CardError('Cannot draw cards from an empty deck')

    def draw_card(self, card):
        if card in self.items:
            self.discard.append(card)
            self.items.remove(card)
        else:
            raise CardError('Card not in deck')

    def _copy(self):
        copy = super(Deck, self)._copy()
        copy.discard = list(self.discard)
        return copy


class CardError(Exception):
    pass