import unittest
from poker.target import StraightFlushTarget, FourOfAKindTarget, \
    FullHouseTarget, FlushTarget, StraightTarget, ThreeOfAKindTarget, \
    TwoPairTarget, PairTarget
from poker.probability import hand_probability


class ProbabilityEmptyHandTest(unittest.TestCase):

    def setUp(self):
        self.total = 133784560.0
        self.straight_flush = StraightFlushTarget()
        self.four_kind = FourOfAKindTarget()
        self.full_house = FullHouseTarget()
        self.flush = FlushTarget()
        self.straight = StraightTarget()
        self.three_kind = ThreeOfAKindTarget()
        self.two_pair = TwoPairTarget()
        self.pair = PairTarget()
    
    # testing the probability of empty hands
    
    def test_straight_flush(self):
        self.assertEqual(hand_probability(self.straight_flush), 37260 / self.total)

    def test_four_of_a_kind(self):
        # Passes!
        self.assertEqual(hand_probability(self.four_kind), 224848 / self.total)

    def test_full_house(self):
        self.assertTrue(False)
        # self.assertGreaterEqual(hand_probability(self.full_house), 3473184 / self.total)

    def test_flush(self):
        self.assertEqual(hand_probability(self.flush), 4047644 / self.total)

    def test_straight(self):
        self.assertEqual(hand_probability(self.straight), 6180020 / self.total)

    def test_three_of_a_kind(self):
        self.assertEqual(hand_probability(self.three_kind), (6461620 + 3698032) / self.total)

    def test_two_pair(self):
        self.assertEqual(hand_probability(self.two_pair), 31433400 / self.total)

    def test_pair(self):
        self.assertEqual(hand_probability(self.pair), 58627800 / self.total)

    def test_no_pair(self):
        self.assertTrue(False)


class ProbabilitySatisfiedTest(unittest.TestCase):

    def setUp(self):
        self.straight_flush = StraightFlushTarget()
        self.four_kind = FourOfAKindTarget()
        self.full_house = FullHouseTarget()
        self.flush = FlushTarget()
        self.straight = StraightTarget()
        self.three_kind = ThreeOfAKindTarget()
        self.two_pair = TwoPairTarget()
        self.pair = PairTarget()
        
    # testing probability of satisfied hands
        
    def test_straight_flush(self):
        target = self.straight_flush.hit_area((5, 0), (5, 0), (5, 0), (5, 0), (5, 0))
        self.assertEqual(hand_probability(target), 1.0)
    
    def test_four_of_a_kind(self):
        target = self.four_kind.hit_area(2, 2, 2, 2)
        self.assertEqual(hand_probability(target), 1.0)
        
    def test_flush(self):
        target = self.flush.hit_area(0, 0, 0, 0, 0)
        self.assertEqual(hand_probability(target), 1.0)
        
    def test_straight(self):
        target = self.straight.hit_area(5, 5, 5, 5, 5)
        self.assertEqual(hand_probability(target), 1.0)
    
    def test_three_of_a_kind(self):
        target = self.three_kind.hit_area(2, 2, 2)
        self.assertEqual(hand_probability(target), 1.0)
    
    def test_pair(self):
        target = self.pair.hit_area(2, 2)
        self.assertEqual(hand_probability(target), 1.0)
    
    def test_two_pair(self):
        target = self.two_pair.hit_area(2, 2, 3, 3)
        self.assertEqual(hand_probability(target), 1.0)
        
        
class ProbabilityOneDrawTest(unittest.TestCase):

    # testing the probability of hands with one draw left
    
    def setUp(self):
        self.total = 46.0
        self.straight_flush = StraightFlushTarget()
        self.four_kind = FourOfAKindTarget()
        self.full_house = FullHouseTarget()
        self.flush = FlushTarget()
        self.straight = StraightTarget()
        self.three_kind = ThreeOfAKindTarget()
        self.two_pair = TwoPairTarget()
        self.pair = PairTarget()
    
    def test_two_pair(self):
        target = self.two_pair.hit_area(2, 2, 3, 4, 5, 6)
        self.assertEqual(hand_probability(target), 12 / self.total)
    
    def test_pair(self):
        target = self.pair.hit_area(2, 3, 4, 5, 6, 7)
        self.assertEqual(hand_probability(target), 18 / self.total)

    def test_three_of_a_kind(self):
        target = self.three_kind.hit_area(2, 2, 3, 3, 4, 4)
        self.assertEqual(hand_probability(target), 6 / self.total)
    
    def test_straight(self):
        target = self.straight.hit_area(5, 5, 5, 5, 13, 13)
        self.assertEqual(hand_probability(target), 4 / self.total)
        
    def test_flush(self):
        target = self.flush.hit_area(0, 0, 0, 0, 1, 1)
        self.assertEqual(hand_probability(target), 9 / self.total)
        
    def test_straight_flush(self):
        target = self.straight_flush.hit_area((5, 0), (5, 0), (5, 0), (5, 0), (6, 0), (6, 0))
        self.assertEqual(hand_probability(target), 1 / self.total)
    
    def test_four_of_a_kind(self):
        target = self.four_kind.hit_area(2, 2, 2, 3, 3, 3)
        self.assertEqual(hand_probability(target), 2 / self.total)
        

class ProbabilityTwoDrawTest(unittest.TestCase):

    # testing the probability of hands with one draw left

    # The values that are compared to the hand_probability result are
    # expected values calculated by myself. I don't have another way of
    # verifying that the result is correct and this method is only effective
    # to the point that things fall in line with expectations.
    
    def setUp(self):
        self.total = 1.0 * 47 * 46  # 2162.0
        self.straight_flush = StraightFlushTarget()
        self.four_kind = FourOfAKindTarget()
        self.full_house = FullHouseTarget()
        self.flush = FlushTarget()
        self.straight = StraightTarget()
        self.three_kind = ThreeOfAKindTarget()
        self.two_pair = TwoPairTarget()
        self.pair = PairTarget()
    
    def test_two_pair(self):
        # hit 3/4/5; miss, hit 3/4/5; hit 6-14, hit same rank
        target = self.two_pair.hit_area(2, 2, 3, 4, 5)
        self.assertEqual(hand_probability(target), 918 / self.total)
    
    def test_pair(self):
        # hit 2-6; miss, hit 2-6; hit 7-14, hit same rank
        target = self.pair.hit_area(2, 3, 4, 5, 6)
        self.assertEqual(hand_probability(target), 1446 / self.total)

    def test_three_of_a_kind(self):
        # hit 2/3; miss, hit 2/3; hit 4, hit 4
        target = self.three_kind.hit_area(2, 2, 3, 3, 4)
        self.assertEqual(hand_probability(target), 370 / self.total)
    
    def test_straight(self):
        # hit 5; miss, hit 5
        target = self.straight.hit_area(5, 5, 5, 5, 13)
        self.assertEqual(hand_probability(target), 356 / self.total)
        
    def test_flush(self):
        # hit 0; miss, hit 0
        target = self.flush.hit_area(0, 0, 0, 0, 1)
        self.assertEqual(hand_probability(target), 756 / self.total)
        
    def test_straight_flush(self):
        target = self.straight_flush.hit_area((5, 0), (5, 0), (5, 0), (5, 0), (6, 0))
        self.assertEqual(hand_probability(target), 92 / self.total)
    
    def test_four_of_a_kind(self):
        # hit 2; miss, hit 2; hit 3, hit 3
        target = self.four_kind.hit_area(2, 2, 2, 3, 3)
        self.assertEqual(hand_probability(target), 94 / self.total)