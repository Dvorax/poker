import unittest
from poker.card import Card, Cards
from poker.hand import HighCard, OnePair, TwoPair, ThreeOfAKind, Straight, \
    Flush, FullHouse, FourOfAKind, StraightFlush, HandError


class HandModuleTest(unittest.TestCase):

    def setUp(self):
        pass


class HandClassTest(unittest.TestCase):

    def setUp(self):
        self.straight_flush = Cards(
            Card(6, 0), Card(7, 0), Card(8, 0), Card(9, 0), Card(10, 0),
            Card(8, 1), Card(13, 2))
        self.four_of_a_kind = Cards(
            Card(9, 1), Card(9, 2), Card(9, 0), Card(9, 3), Card(7, 1),
            Card(4, 3), Card(2, 0))
        self.full_house = Cards(
            Card(10, 1), Card(10, 0), Card(10, 2), Card(7, 0), Card(7, 1),
            Card(4, 3), Card(4, 2))
        self.flush = Cards(
            Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1),
            Card(7, 3), Card(4, 2))
        self.straight = Cards(
            Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(6, 2),
            Card(3, 2), Card(2, 0))
        self.three_of_a_kind = Cards(
            Card(9, 1), Card(9, 0), Card(9, 3), Card(7, 3), Card(14, 1),
            Card(5, 1), Card(3, 2))
        self.two_pair = Cards(
            Card(10, 0), Card(10, 1), Card(2, 1), Card(2, 3), Card(8, 3),
            Card(9, 1), Card(4, 2))
        self.one_pair = Cards(
            Card(5, 3), Card(5, 0), Card(9, 1), Card(6, 3), Card(8, 2),
            Card(4, 2), Card(2, 0))
        self.high_card = Cards(
            Card(10, 0), Card(8, 1), Card(6, 1), Card(4, 1), Card(2, 3),
            Card(3, 2), Card(7, 3))

    def test_find(self):
        pass


class HighCardTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(10, 0), Card(8, 1), Card(6, 1), Card(4, 1),
                      Card(2, 3))
        self.hand = HighCard(cards)
    
    def test_creation(self):
        expected = 'Ten-high with kicker <Cards: [2S, 4D, 6D, 8D]>'
        self.assertEqual(str(self.hand), expected)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 0)
        self.assertEqual(self.hand.score(), 8.48611743286299497)


class OnePairTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(5, 3), Card(5, 0), Card(9, 1), Card(6, 3),
                      Card(8, 2))
        self.bad = Cards(Card(10, 0), Card(8, 1), Card(6, 1), Card(4, 1),
                         Card(2, 3))
        self.hand = OnePair(cards)
    
    def test_creation(self):
        expected = 'Pair of Fives with kicker <Cards: [6S, 8H, 9D]>'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, OnePair, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 13)
        self.assertEqual(self.hand.score(), 16.57578516158398)


class TwoPairTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(10, 0), Card(10, 1), Card(2, 1), Card(2, 3),
                      Card(8, 3))
        self.bad = Cards(Card(5, 3), Card(5, 0), Card(9, 1), Card(6, 3),
                         Card(8, 2))
        self.hand = TwoPair(cards)
    
    def test_creation(self):
        expected = 'Two pairs of Tens and Twos with a kicker Eight'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, TwoPair, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 2 * 13)
        self.assertEqual(self.hand.score(), 34.46153846153846)


class ThreeOfAKindTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(9, 1), Card(9, 0), Card(9, 3), Card(7, 3), Card(14, 1))
        self.bad = Cards(Card(10, 0), Card(10, 1), Card(2, 1), Card(2, 3), Card(8, 3))
        self.hand = ThreeOfAKind(cards)
    
    def test_creation(self):
        expected = 'Three of a kind Nine with kicker <Cards: [7S, AD]>'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, ThreeOfAKind, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 3 * 13)
        self.assertEqual(self.hand.score(), 46.95266272189349)


class StraightTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(6, 2))
        low_ace = Cards(Card(14, 0), Card(2, 1), Card(3, 2), Card(4, 3), Card(5, 0))
        self.bad = Cards(Card(9, 1), Card(9, 0), Card(9, 3), Card(7, 3), Card(14, 1))
        self.hand = Straight(cards)
        self.low_ace_hand = Straight(low_ace)
    
    def test_creation(self):
        expected = 'Six-high straight'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, Straight, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 4 * 13)
        self.assertEqual(self.hand.score(), 56.0)
        self.assertEqual(self.low_ace_hand.score(), 55.0)


class FlushTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1))
        self.bad = Cards(Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(6, 2))
        self.hand = Flush(cards)
    
    def test_creation(self):
        expected = 'Diamond Flush with <Cards: [2D, 4D, 6D, 9D, 10D]>'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, Flush, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 5 * 13)
        self.assertEqual(self.hand.score(), 73.56304050978608)


class FullHouseTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(10, 1), Card(10, 0), Card(10, 2), Card(7, 0), Card(7, 1))
        self.bad = Cards(Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1))
        self.hand = FullHouse(cards)
    
    def test_creation(self):
        expected = 'Full house with Ten triplet and Seven pair'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, FullHouse, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 6 * 13)
        self.assertEqual(self.hand.score(), 86.38461538461539)


class FourOfAKindTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(9, 1), Card(9, 2), Card(9, 0), Card(9, 3), Card(7, 1))
        self.bad = Cards(Card(10, 1), Card(10, 0), Card(10, 2), Card(7, 0), Card(7, 1))
        self.hand = FourOfAKind(cards)
    
    def test_creation(self):
        expected = 'Four of a kind Nines with a kicker Seven'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, FourOfAKind, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 7 * 13)
        self.assertEqual(self.hand.score(), 98.38461538461539)


class StraightFlushTest(unittest.TestCase):

    def setUp(self):
        cards = Cards(Card(6, 0), Card(7, 0), Card(8, 0), Card(9, 0), Card(10, 0))
        low_ace = Cards(Card(14, 0), Card(2, 0), Card(3, 0), Card(4, 0), Card(5, 0))
        self.bad = Cards(Card(9, 1), Card(9, 2), Card(9, 0), Card(9, 3), Card(7, 1))
        self.hand = StraightFlush(cards)
        self.low_ace_hand = StraightFlush(low_ace)
    
    def test_creation(self):
        expected = 'Ten-high Club straight flush'
        self.assertEqual(str(self.hand), expected)
        self.assertRaises(HandError, StraightFlush, self.bad)
    
    def test_score(self):
        self.assertEqual(self.hand.hand_score, 8 * 13)
        self.assertEqual(self.hand.score(), 112.0)
        self.assertEqual(self.low_ace_hand.score(), 107.0)


class HandComparisonsTest(unittest.TestCase):

    def setUp(self):
        self.straight = Straight(Cards(
            Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(6, 2)))
        self.straight2 = Straight(Cards(
            Card(2, 0), Card(3, 1), Card(4, 3), Card(5, 0), Card(6, 3)))
        self.flush = Flush(Cards(
            Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1)))
        self.flush2 = Flush(Cards(
            Card(5, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1)))
    
    def test_less_than_and_greater_than(self):
        self.assertTrue(self.straight < self.flush)
        self.assertTrue(self.flush > self.straight)
        self.assertTrue(self.flush < self.flush2)
    
    def test_equal_and_not_equal(self):
        self.assertTrue(self.straight == self.straight2)
        self.assertTrue(self.straight != self.flush)
        self.assertTrue(self.flush != self.flush2)
    
    def test_less_greater_equal(self):
        pass


if __name__ == '__main__':
    unittest.main()
