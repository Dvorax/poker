from poker.card import Cards
from poker.pattern import MultiplesPattern, StraightOrFlushPattern


def find_hand(cards):
    hands = [StraightFlush, FullHouse, FourOfAKind, Flush, Straight, 
             ThreeOfAKind, TwoPair, OnePair]

    for hand in hands:
        if hand.pattern.matches_with(cards):
            return hand(cards)

    return HighCard(cards)


class Hand(object):

    def __init__(self, cards, hand_rank, high_card, *kickers):
        self.cards = cards
        self.hand_score = hand_rank * 13
        self.high_card = high_card
        self.kickers = Cards(*kickers)
    
    def score(self):
        high_card_score = self.high_card.rank_from_zero()
        kicker_score = self.kickers.kicker_value()
        in_hand_score = high_card_score + kicker_score
        return self.hand_score + in_hand_score

    def __lt__(self, other):
        return self.score() < other.score()

    def __gt__(self, other):
        return self.score() > other.score()

    def __eq__(self, other):
        return self.score() == other.score()

    def __le__(self, other):
        return self.score() <= other.score()

    def __ge__(self, other):
        return self.score() >= other.score()

    def __ne__(self, other):
        return self.score() != other.score()


class HandError(Exception):
    pass


class StraightFlush(Hand):

    pattern = StraightOrFlushPattern(straight=True, flush=True)

    def __init__(self, cards):
        if not StraightFlush.pattern.matches_with(cards):
            raise HandError('Invalid Straight Flush hand')

        straight = cards.straight()
        flush = cards.flush()
        self.straight_flush = straight.intersect(flush)
        high_card = max(self.straight_flush)

        # change high card to card of rank 5 if ace is low
        if high_card.rank == 14 and min(self.straight_flush).rank == 2:
            high_card = max(self.straight_flush.remove(high_card))

        super(StraightFlush, self).__init__(cards, 8, high_card)

    def __repr__(self):
        if self.high_card.rank == 14:
            return self.high_card.suit_name() + ' Royal flush'
        else:
            return self.high_card.rank_name() + '-high ' + \
                self.high_card.suit_name() + ' straight flush'


class FourOfAKind(Hand):

    pattern = MultiplesPattern(4)

    def __init__(self, cards):
        if not FourOfAKind.pattern.matches_with(cards):
            raise HandError('Invalid Four of a Kind hand')

        self.four = cards.quadruplets(1)
        kicker = cards.filler(1, *self.four)
        super(FourOfAKind, self).__init__(cards, 7, self.four[0])
        if kicker is not None:
            self.kickers = Cards(kicker)

    def __repr__(self):
        return 'Four of a kind ' + self.four[0].rank_name() + \
            's with a kicker ' + self.kickers[0].rank_name()


class FullHouse(Hand):

    pattern = MultiplesPattern(3, 2)

    def __init__(self, cards):
        if not FullHouse.pattern.matches_with(cards):
            raise HandError('Invalid Full House hand')
        
        self.triplet = cards.triplets(1)
        self.pair = cards.pairs(1)
        super(FullHouse, self).__init__(
            cards, 6, self.triplet[0], self.pair[0])

    def __repr__(self):
        return 'Full house with ' + self.triplet[0].rank_name() + \
            ' triplet and ' + self.pair[0].rank_name() + ' pair'


class Flush(Hand):

    pattern = StraightOrFlushPattern(flush=True)

    def __init__(self, cards):
        if not Flush.pattern.matches_with(cards):
            raise HandError('Invalid Flush hand')

        self.flush = cards.flush()
        high_card = max(self.flush)
        kickers = self.flush.filler(4, high_card)
        super(Flush, self).__init__(cards, 5, high_card, *kickers)

    def __repr__(self):
        return self.flush[0].suit_name() + ' Flush with ' + str(self.flush)


class Straight(Hand):

    pattern = StraightOrFlushPattern(straight=True)

    def __init__(self, cards):
        if not Straight.pattern.matches_with(cards):
            raise HandError('Invalid Straight hand')

        self.straight = cards.straight()
        high_card = max(self.straight)

        # change high card to card of rank 5 if ace is low
        if high_card.rank == 14 and min(self.straight).rank == 2:
            high_card = max(self.straight.remove(high_card))
        super(Straight, self).__init__(cards, 4, high_card)

    def __repr__(self):
        return self.high_card.rank_name() + '-high straight'


class ThreeOfAKind(Hand):

    pattern = MultiplesPattern(3)

    def __init__(self, cards):
        if not ThreeOfAKind.pattern.matches_with(cards):
            raise HandError('Invalid Three of a Kind hand')

        self.triplet = cards.triplets(1)
        kickers = cards.filler(2, *self.triplet)
        super(ThreeOfAKind, self).__init__(
            cards, 3, self.triplet[0], *kickers)

    def __repr__(self):
        return 'Three of a kind ' + self.triplet[0].rank_name() + \
            ' with kicker ' + str(self.kickers)


class TwoPair(Hand):

    pattern = MultiplesPattern(2, 2)

    def __init__(self, cards):
        if not TwoPair.pattern.matches_with(cards):
            raise HandError('Invalid Two Pair hand')

        pairs = cards.pairs(2)
        self.high_pair = max(pairs)
        self.low_pair = min(pairs)
        self.lone_card = cards.filler(
            1, *list(self.low_pair + self.high_pair))
        super(TwoPair, self).__init__(
            cards, 2, self.high_pair[0], self.low_pair[0])
        if self.lone_card is not None:
            self.kickers = self.kickers.add(self.lone_card)

    def __repr__(self):
        return 'Two pairs of ' + self.high_pair[0].rank_name() + 's and ' + \
            self.low_pair[0].rank_name() + 's with a kicker ' + \
            self.lone_card.rank_name()


class OnePair(Hand):

    pattern = MultiplesPattern(2)

    def __init__(self, cards):
        if not OnePair.pattern.matches_with(cards):
            raise HandError('Invalid Pair hand')

        self.pair = cards.pairs(1)
        kickers = cards.filler(3, *self.pair)
        super(OnePair, self).__init__(cards, 1, self.pair[0], *kickers)

    def __repr__(self):
        return 'Pair of ' + self.pair[0].rank_name() + 's with kicker ' + \
            str(self.kickers)


class HighCard(Hand):

    pattern = None

    def __init__(self, cards):
        if len(cards) == 0:
            raise HandError('Invalid hand')

        high_card = max(cards)
        kickers = cards.filler(4, high_card)
        super(HighCard, self).__init__(cards, 0, high_card, *kickers)

    def __repr__(self):
        return self.high_card.rank_name() + '-high with kicker ' + \
            str(self.kickers)
