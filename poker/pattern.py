class Pattern(object):

    def matches_with(self, cards):
        return self.distance(cards) <= 0

    def distance(self, cards):
        pass


class MultiplesPattern(Pattern):

    def __init__(self, *lengths):
        if len(lengths) == 0:
            raise PatternError(
                'Pattern must have declaration for lengths of \
                multiples')
        self.lengths = list(lengths)

    def distance(self, cards):
        distance = 0

        if len(cards) < len(self.lengths):
            distance += len(self.lengths) - len(cards)

        for length in sorted(self.lengths):
            found_multi = cards.multiples(length, 1)
            if len(found_multi) > 0:
                cards = cards.remove(*found_multi)
            else:
                while length >= 2 and len(found_multi) < 1:
                    distance += 1
                    length -= 1
                    found_multi = cards.multiples(length, 1)

        return distance


class StraightOrFlushPattern(Pattern):

    def __init__(self, straight=False, flush=False):
        if not (straight or flush):
            raise PatternError(
                'Pattern must be declared straight and/or flush')
        self.straight = straight
        self.flush = flush

    def distance(self, cards):
        straight_cards = cards.straight()
        flush_cards = cards.flush()

        if self.straight and self.flush:
            hand = straight_cards.intersect(flush_cards)
        elif self.flush:
            hand = flush_cards
        elif self.straight:
            hand = straight_cards
        else:
            hand = []

        return 5 - len(hand)


class PatternError(Exception):
    pass