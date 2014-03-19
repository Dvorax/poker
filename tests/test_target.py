import unittest
# from poker.card import Card
from poker.target import StraightFlushTarget, FourOfAKindTarget, \
        FullHouseTarget, FlushTarget, StraightTarget, ThreeOfAKindTarget, \
        TwoPairTarget, PairTarget

class TargetsTest(unittest.TestCase):

    def setUp(self):
        self.straight_flush = StraightFlushTarget()
        self.four_kind = FourOfAKindTarget()
        self.full_house = FullHouseTarget()
        self.flush = FlushTarget()
        self.straight = StraightTarget()
        self.three_kind = ThreeOfAKindTarget()
        self.two_pair = TwoPairTarget()
        self.pair = PairTarget()
    
    def test_hit_area(self):
        pass
    
    def test_hit_with_cards(self):
        pass

    def test_area_distance(self):
        pass

    def test_area_hits(self):
        pass

    def test_area_misses(self):
        pass