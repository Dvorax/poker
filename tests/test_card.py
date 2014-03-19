import unittest
from poker.card import Card, Cards, Deck, straights_by_high_rank, CardError
from poker.utility import CollectionError


class CardTest(unittest.TestCase):

    def setUp(self):
        self.low = Card(2, 0)
        self.low2 = Card(2, 1)
        self.high = Card(14, 2)
        self.high2 = Card(14, 2)

    def test_comparisons(self):
        self.assertTrue(self.low < self.high)
        self.assertTrue(self.high > self.low)
        self.assertTrue(self.high == self.high2)
        self.assertTrue(self.low <= self.high)
        self.assertTrue(self.high >= self.low)
        self.assertTrue(self.low != self.low2)
    
    def test_rank_from_zero(self):
        self.assertEqual(self.low.rank_from_zero(), 0)
        self.assertEqual(self.high.rank_from_zero(), 12)
    
    def test_rank_name(self):
        self.assertEqual(self.low.rank_name(), 'Two')
        self.assertEqual(self.high.rank_name(), 'Ace')
    
    def test_suit_name(self):
        self.assertEqual(self.low.suit_name(), 'Club')
        self.assertEqual(self.high.suit_name(), 'Heart')
    
    #maybe belongs in a different test class
    def test_straights_by_high_rank(self):
        self.assertEqual(straights_by_high_rank(2), [5, 6])
        self.assertEqual(straights_by_high_rank(3), [5, 6, 7])
        self.assertEqual(straights_by_high_rank(4), [5, 6, 7, 8])
        self.assertEqual(straights_by_high_rank(5), [5, 6, 7, 8, 9])
        self.assertEqual(straights_by_high_rank(6), [6, 7, 8, 9, 10])
        self.assertEqual(straights_by_high_rank(7), [7, 8, 9, 10, 11])
        self.assertEqual(straights_by_high_rank(8), [8, 9, 10, 11, 12])
        self.assertEqual(straights_by_high_rank(9), [9, 10, 11, 12, 13])
        self.assertEqual(straights_by_high_rank(10), [10, 11, 12, 13, 14])
        self.assertEqual(straights_by_high_rank(11), [11, 12, 13, 14])
        self.assertEqual(straights_by_high_rank(12), [12, 13, 14])
        self.assertEqual(straights_by_high_rank(13), [13, 14])
        self.assertEqual(straights_by_high_rank(14), [5, 14])

    def test_bad_inputs(self):
        self.assertRaises(CardError, Card, 100, 100)


class CardsTest(unittest.TestCase):

    def setUp(self):
        self.card1, self.card2, self.card3 = Card(2, 0), Card(3, 1), Card(4, 2)
        self.card_list = [self.card1, self.card2, self.card3]
        self.cards = Cards(*self.card_list)

    def test_add(self):
        new_card = Card(5, 3)
        self.cards = self.cards.add(new_card)
        self.assertIn(new_card, self.cards)
        self.assertRaises(CollectionError, self.cards.add, self.card1)

    def test_remove(self):
        self.cards = self.cards.remove(self.card1)
        self.assertNotIn(self.card1, self.cards)
        self.cards = self.cards.remove(self.card2, self.card3)
        self.assertNotIn(self.card2, self.cards)
        self.assertNotIn(self.card3, self.cards)
        self.assertRaises(CollectionError, self.cards.remove, self.card1)

    def test_copy(self):
        copy = self.cards._copy()
        self.assertEqual(self.cards, copy)
        self.cards = self.cards.remove(self.card2)
        self.assertNotIn(self.card2, self.cards)
        self.assertIn(self.card2, copy)

    def test_limit(self):
        limited = self.cards.limit(2)
        self.assertNotIn(self.card1, limited)

    def test_filler(self):
        filler = self.cards.filler(1, self.card3)
        self.assertEqual(self.card2, filler)
    
    def test_intersect(self):
        cards2 = Cards(self.card2, self.card3, Card(5, 3))
        expectation = Cards(self.card2, self.card3)
        self.assertEqual(self.cards.intersect(cards2), expectation)

    def test_ranks_represented(self):
        self.cards = self.cards.add(Card(2, 1))
        self.assertEqual(self.cards.ranks_represented(), {2, 3, 4})
    
    def test_suits_represented(self):
        self.cards = self.cards.add(Card(2, 1))
        self.assertEqual(self.cards.suits_represented(), {0, 1, 2})
    
    def test_multiples(self):
        pass

    def test_singlets(self):
        cards = Cards(self.card1)
        cards2 = Cards()
        self.assertEqual(len(cards.singlets()), 1)
        self.assertEqual(cards.singlets()[0], Cards(self.card1))
        self.assertEqual(len(cards2.singlets()), 0)
    
    def test_pairs(self):
        cards1 = Cards(Card(2, 0), Card(2, 1))
        cards2 = Cards(Card(2, 0), Card(2, 1), Card(2, 2))
        cards3 = Cards(Card(2, 0), Card(2, 1), Card(3, 0), Card(3, 1))
        self.assertEqual(len(self.cards.pairs()), 0)
        self.assertEqual(len(cards1.pairs()), 1)
        self.assertEqual(len(cards2.pairs()), 0)
        self.assertEqual(len(cards3.pairs()), 2)
    
    def test_triplets(self):
        cards1 = Cards(Card(2, 0), Card(2, 1))
        cards2 = Cards(Card(2, 0), Card(2, 1), Card(2, 2))
        cards3 = Cards(Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3))
        cards4 = Cards(
            Card(2, 0), Card(2, 1), Card(2, 2), Card(3, 0), Card(3, 1), Card(3, 2))
        self.assertEqual(len(self.cards.triplets()), 0)
        self.assertEqual(len(cards1.triplets()), 0)
        self.assertEqual(len(cards2.triplets()), 1)
        self.assertEqual(len(cards3.triplets()), 0)
        self.assertEqual(len(cards4.triplets()), 2)
    
    def test_quadruplets(self):
        cards1 = Cards(Card(2, 0), Card(2, 1), Card(2, 2))
        cards2 = Cards(Card(2, 0), Card(2, 1), Card(2, 2), Card(2, 3))
        self.assertEqual(len(cards1.quadruplets()), 0)
        self.assertEqual(len(cards2.quadruplets()), 1)
    
    def test_flush(self):
        cards1 = Cards(Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1), Card(10, 1))
        cards2 = Cards(Card(2, 1), Card(4, 1), Card(6, 1), Card(9, 1))
        self.assertEqual(len(cards1.flush()), 5)
        self.assertEqual(len(cards2.flush()), 4)
    
    def test_straight(self):
        cards1 = Cards(Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(6, 2))
        cards2 = Cards(Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3))
        cards3 = Cards(Card(2, 3), Card(3, 0), Card(4, 2), Card(5, 3), Card(14, 0))
        self.assertEqual(len(cards1.straight()), 5)
        self.assertEqual(len(cards2.straight()), 4)
        self.assertEqual(len(cards3.straight()), 5)

    def test_kicker_value(self):
        cards = Cards(Card(8, 1), Card(6, 1), Card(4, 1), Card(2, 3))
        self.assertEqual(cards.kicker_value(), 0.48611743286299497)


class DeckTest(unittest.TestCase):
    
    def setUp(self):
        self.deck = Deck()
    
    def test_generate(self):
        pass
    
    def test_shuffle(self):
        pass
    
    def test_draw_card(self):
        pass
    
    def test_add(self):
        pass


if __name__ == '__main__':
    unittest.main()
