from poker.card import Card
from copy import deepcopy
from itertools import combinations, permutations


class Target(object):
    """
    Each child class is based on concept of dividing the cards of a deck 
    into different areas that can satisfy the conditions for each hand. 
    This is done so the probability algorithm can focus on satisfying each 
    area individually and then take the sum of possibilities. For example, 
    cards can be grouped by rank or suit.

    Cards by rank and suit for visualization of possible target areas:
    2C 3C 4C 5C 6C 7C 8C 9C 10C JC QC KC AC
    2D 3D 4D 5D 6D 7D 8D 9D 10D JD QD KD AD
    2H 3H 4H 5H 6H 7H 8H 9H 10H JH QH KH AH
    2S 3S 4S 5S 6S 7S 8S 9S 10S JS QS KS AS
    """
    
    @property
    def destroyed(self):
        for area in self.areas:
            if self.area_distance(area) <= 0:
                return True
        return False
    
    def __init__(self, area_keys, initial_size, needed, hit_decrement=1):
        self.areas = dict((key, initial_size) for key in area_keys)
        self.initial_size = initial_size
        self.needed = needed
        self.hit_decrement = hit_decrement
        self.shots = 0

    def copy(self):
        return deepcopy(self)

    def hit_area(self, *area_keys):
        target = self.copy()
        for area in area_keys:
            target.areas[area] -= self.hit_decrement
            target.shots += 1
        return target

    def hit_with_cards(self, *cards):
        target = self.copy()
        for card in cards:
            area_keys = self._keys_from_cards(card)
            target = target.hit_area(*area_keys)
        return target

    def area_distance(self, area_key):
        return self.area_satisfies(area_key) + self.needed - self.initial_size

    def area_hits(self, area_key):
        return self.initial_size - self.area_satisfies(area_key)

    def area_misses(self, area_key):
        return self.shots - self.area_hits(area_key)

    def area_satisfies(self, area_key):
        # Returns the number of cards that can be hit in the area that
        # contribute to satisfying the target.
        return self.areas[area_key]

    def _keys_from_cards(self, *cards):
        pass

    
class StraightFlushTarget(Target):
    
    def __init__(self):
        straight_flush_keys = \
            [(high_rank, suit)
             for high_rank in Card.straight_high_ranks
             for suit in Card.suits]
        super(StraightFlushTarget, self).__init__(
            area_keys=straight_flush_keys, initial_size=5, needed=5)

    def _keys_from_cards(self, *cards):
        return [(high_rank, card.suit) for card in cards
                for high_rank in card.straights_by_high_rank()]


class FourOfAKindTarget(Target):
    # Pair Targets are divided by card rank and need 2 hits out of the 4 cards 
    # in any of the 13 ranks to be satisfied.

    def __init__(self):
        super(FourOfAKindTarget, self).__init__(
            area_keys=Card.ranks, initial_size=4, needed=4)

    def _keys_from_cards(self, *cards):
        return [card.rank for card in cards]


class FullHouseTarget(Target):
    # not finished

    def __init__(self):
        full_house_keys = [(a, b) for a, b in permutations(Card.ranks, 2)]
        super(FullHouseTarget, self).__init__(
            area_keys=full_house_keys, initial_size=8, needed=5)

    def _keys_from_cards(self, *cards):
        return None


class FlushTarget(Target):

    def __init__(self):
        super(FlushTarget, self).__init__(
            area_keys=Card.suits, initial_size=13, needed=5)

    def _keys_from_cards(self, *cards):
        return [card.suit for card in cards]


class StraightTarget(Target):

    def __init__(self):
        super(StraightTarget, self).__init__(
            initial_size=20, needed=5, hit_decrement=4,
            area_keys=Card.straight_high_ranks)

    def _keys_from_cards(self, *cards):
        return [high_rank for card in cards
                for high_rank in card.straights_by_high_rank()]

    def hit_with_cards(self, *cards):
        new_cards = []
        ranks = []
        for card in cards:
            if card.rank not in ranks:
                new_cards.append(card)
                ranks.append(card.rank)

        return super(StraightTarget, self).hit_with_cards(*new_cards)

    def area_hits(self, area_key):
        return super(StraightTarget, self).area_hits(area_key) / 4

    def area_distance(self, area_key):
        return self.areas[area_key] / 4


class ThreeOfAKindTarget(Target):
    # Pair Targets are divided by card rank and need 2 hits out of the 4 cards 
    # in any of the 13 ranks to be satisfied.

    def __init__(self):
        super(ThreeOfAKindTarget, self).__init__(
            area_keys=Card.ranks, initial_size=4, needed=3)

    def _keys_from_cards(self, *cards):
        return [card.rank for card in cards]


class TwoPairTarget(Target):
    # not finished

    def __init__(self):
        two_pair_keys = [(a, b) for a, b in combinations(Card.ranks, 2)]
        super(TwoPairTarget, self).__init__(
            area_keys=two_pair_keys, initial_size=8, needed=4)

        # The .areas dictionary has no meaning in TwoPairTarget except as
        # a storage mechanism for the area keys. The keys are still useful
        # because they specify the areas that can be satisfied which would
        # satisfy the target as a whole. The dictionary value, which
        # represents the number of cards contained in an area that contribute
        # to satisfying a target, is impossible to maintain since the
        # combination key is missing knowledge of the actual rank that was hit.

        # The values in this dictionary are used instead of the .areas values.
        self.rank_areas = dict((rank, 4) for rank in Card.ranks)

    def hit_area(self, *ranks):
        # This function is not meant to take area_keys as parameters like in
        # its parent and many of its sibling implementations. It affects the
        # rank_areas dictionary instead of the areas dictionary.
        target = self.copy()
        for rank in ranks:
            target.rank_areas[rank] -= self.hit_decrement
            target.shots += 1
        return target

    def area_distance(self, area_key):
        cards_in_ranks = 0
        for rank in area_key:
            cards_in_ranks += self.rank_areas[rank]
        return cards_in_ranks + self.needed - self.initial_size

    def area_satisfies(self, area_key):
        # When we get a pair in any rank area, we can ignore the rest of the
        # cards in that rank area.
        result = 0
        for rank in area_key:
            size = self.rank_areas[rank]
            if size > 2:
                result += size
        return result

    def _keys_from_cards(self, *cards):
        return [card.rank for card in cards]


class PairTarget(Target):
    # Pair Targets are divided by card rank and need 2 hits out of the 4 cards 
    # in any of the 13 ranks to be satisfied.

    def __init__(self):
        super(PairTarget, self).__init__(
            area_keys=Card.ranks, initial_size=4, needed=2)

    def _keys_from_cards(self, *cards):
        return [card.rank for card in cards]


targets = [StraightFlushTarget, FourOfAKindTarget, 
           FlushTarget, StraightTarget, ThreeOfAKindTarget,
           TwoPairTarget, PairTarget]  # FullHouseTarget, ,


def _combination_area_keys(rank):
    area_keys = []
    for other_rank in Card.ranks:
        # do not append anything if ranks are equal
        if rank < other_rank:
            area_keys.append((rank, other_rank))
        elif rank > other_rank:
            area_keys.append((other_rank, rank))
    return area_keys
