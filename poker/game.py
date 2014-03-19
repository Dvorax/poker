from poker.card import Cards, Deck
from poker.player import Players
from poker.chips import Pot


class TexasHoldEm(object):

    def __init__(self):
        super(TexasHoldEm, self).__init__()
        self.players = Players()

    def play(self):
        round_no = 1
        min_bet = 200

        while self.players.has_human():
            if round_no % 5 == 0:
                min_bet += 200
            PokerRound(self.players.copy(), min_bet).play()
            self.players = self.players.rotate()
            round_no += 1


class PokerRound(object):

    def __init__(self, players, min_bet):
        self.players = players
        self.min_bet = min_bet
        self.deck = Deck()
        self.community = Cards()
        self.pot = Pot()

    # def post_blinds(self):
    #     big_blind = self.players.big_blind()
    #     little_blind = self.players.little_blind()
    #
    #     # big_blind = big_blind.bet(self.min_bet)
    #     # little_blind = little_blind.bet(self.min_bet / 2)

    def deal_cards(self):
        # for __ in range(2):
        #     for player in self.players:
        #         card = self.deck.draw_card()
        #         player = player.add_card(card)
        pass

    # def betting(self):
    #     while True:
    #         break

    def draw_community(self, amount):
        for __ in range(amount):
            card = self.deck.draw_card()
            self.deck = self.deck.remove(card)
            self.community = self.community.add(card)

    def award_winner(self, player):
        pass

    def play(self):
        self.deal_cards()
        # self.post_blinds()
        for draw_amount in (3, 1, 1, 0):
            # self.betting()

            if len(self.players) > 1:
                self.draw_community(draw_amount)
            else: 
                break

        # self.award_winner()
