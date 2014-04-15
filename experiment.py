__author__ = 'john'

from poker.card import Card, Cards, Deck

cards = [Card(14, 0), Card(2, 0), Card(3, 0), Card(4, 0), Card(6, 0)]
# cards = [Card(2, 0), Card(2, 1), Card(3, 0), Card(3, 1), Card(4, 0)]

if __name__ == "__main__":
    tally = 0
    divisor = 2162
    multiplier = 1.13
    testing = 'straight'

    deck = Deck()
    for card in cards:
        deck.draw_card(card)

    for i in range(int(divisor * multiplier)):
        _deck = deck._copy()
        _deck.draw_random()
        _deck.draw_random()

        # _deck.draw_random()
        # _deck.draw_random()
        # _deck.draw_random()

        # _deck.draw_random()
        # _deck.draw_random()
        _cards = Cards(*_deck.discard)

        # if len(_cards.multiples(3)) > 0:
        if len(_cards.straight()) > 5:
            tally += 1

    print(testing)
    print('Count: {0} / {1} = {2}'.format(1.0 * tally / multiplier, divisor, 1.0 * tally / divisor / multiplier))