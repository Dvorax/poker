import unittest
from poker.card import Card, Cards
from poker.pattern import MultiplesPattern, StraightOrFlushPattern


class MultiplesPatternsTest(unittest.TestCase):

    def setUp(self):
        self.no_cards = Cards()
        self.one_card = Cards(Card(2, 0))
        self.no_pair = Cards(Card(2, 0), Card(3, 1))
        self.one_pair = Cards(Card(2, 0), Card(2, 1), Card(3, 0))
        self.two_pair = Cards(Card(2, 0), Card(2, 1), Card(3, 0), Card(3, 2))
        self.triplet = Cards(Card(2, 0), Card(2, 1), Card(2, 2))
        self.full_house = Cards(
            Card(2, 0), Card(2, 1), Card(2, 2), Card(3, 0), Card(3, 1))
        self.quadruplet = Cards(Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3))
    
    def test_is_satisfied_by(self):
        pattern = MultiplesPattern(2, 2)
        self.assertEqual(pattern.matches_with(self.one_pair), False)
        self.assertEqual(pattern.matches_with(self.two_pair), True)
    
        pattern = MultiplesPattern(3)
        self.assertEqual(pattern.matches_with(self.one_pair), False)
        self.assertEqual(pattern.matches_with(self.triplet), True)
    
        pattern = MultiplesPattern(3, 2)
        self.assertEqual(pattern.matches_with(self.two_pair), False)
        self.assertEqual(pattern.matches_with(self.triplet), False)
        self.assertEqual(pattern.matches_with(self.full_house), True)

        pattern = MultiplesPattern(4)
        self.assertEqual(pattern.matches_with(self.triplet), False)
        self.assertEqual(pattern.matches_with(self.quadruplet), True)
    
    def test_distance_two_pair(self):
        pattern = MultiplesPattern(2, 2)
        self.assertEqual(pattern.distance(self.no_cards), 4)
        self.assertEqual(pattern.distance(self.one_card), 3)
        self.assertEqual(pattern.distance(self.no_pair), 2)
        self.assertEqual(pattern.distance(self.one_pair), 1)
        self.assertEqual(pattern.distance(self.two_pair), 0)
    
    def test_distance_triplet(self):
        pattern = MultiplesPattern(3)
        self.assertEqual(pattern.distance(self.no_cards), 3)
        self.assertEqual(pattern.distance(self.one_card), 2)
        self.assertEqual(pattern.distance(self.one_pair), 1)
        self.assertEqual(pattern.distance(self.triplet), 0)
    
    def test_distance_full_house(self):
        pattern = MultiplesPattern(3, 2)
        self.assertEqual(pattern.distance(self.no_cards), 5)
        self.assertEqual(pattern.distance(self.one_card), 4)
        self.assertEqual(pattern.distance(self.no_pair), 3)
        self.assertEqual(pattern.distance(self.one_pair), 2)
        self.assertEqual(pattern.distance(self.two_pair), 1)
        self.assertEqual(pattern.distance(self.triplet), 1)
        self.assertEqual(pattern.distance(self.full_house), 0)
    
    def test_distance_quadruplet(self):
        pattern = MultiplesPattern(4)
        self.assertEqual(pattern.distance(self.no_cards), 4)
        self.assertEqual(pattern.distance(self.one_card), 3)
        self.assertEqual(pattern.distance(self.one_pair), 2)
        self.assertEqual(pattern.distance(self.triplet), 1)
        self.assertEqual(pattern.distance(self.quadruplet), 0)


class StraightOrFlushPatternsTest(unittest.TestCase):

    def setUp(self):
        self.straight = Cards(
            Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(6, 2))
        self.flush = Cards(Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1))
        self.both = Cards(Card(6, 0), Card(7, 0), Card(8, 0), Card(9, 0), Card(10, 0))
        self.part_straight = Cards(Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3))
        self.part_flush = Cards(Card(2, 1), Card(4, 1), Card(6, 1))
        self.part_both = Cards(Card(6, 0), Card(7, 0))

    def test_is_satisfied_by(self):
        pattern = StraightOrFlushPattern(straight=True)
        self.assertEqual(pattern.matches_with(self.straight), True)
        self.assertEqual(pattern.matches_with(self.part_straight), False)

        pattern = StraightOrFlushPattern(flush=True)
        self.assertEqual(pattern.matches_with(self.flush), True)
        self.assertEqual(pattern.matches_with(self.part_flush), False)

        pattern = StraightOrFlushPattern(straight=True, flush=True)
        self.assertEqual(pattern.matches_with(self.both), True)
        self.assertEqual(pattern.matches_with(self.part_both), False)
    
    def test_distance(self):
        pattern = StraightOrFlushPattern(straight=True)
        self.assertEqual(pattern.distance(self.straight), 0)
        self.assertEqual(pattern.distance(self.part_straight), 1)

        pattern = StraightOrFlushPattern(flush=True)
        self.assertEqual(pattern.distance(self.flush), 0)
        self.assertEqual(pattern.distance(self.part_flush), 2)

        pattern = StraightOrFlushPattern(straight=True, flush=True)
        self.assertEqual(pattern.distance(self.both), 0)
        self.assertEqual(pattern.distance(self.part_both), 3)


if __name__ == '__main__':
    unittest.main()
