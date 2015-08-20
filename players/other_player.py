from card import Card
from cards import Cards, Deck

__author__ = 'marc.henri'


class OtherPlayer():
    hand = None
    hand_size = None
    initial_hand = None
    actions = None
    name = None
    points = None
    potential_cards = None

    def __init__(self, name):
        self.name = name
        self.hand_size = 14
        # TODO - Unknown Cards to initial hand
        self.initial_hand = Cards(cards_list=[])
        self.hand = self.initial_hand
        self.potential_cards = Deck()
        self.actions = []

    def set_name(self, name):
        self.name = name

    def update_initial_card(self, cards: list):
        for card in cards:
            # TODO with Unknwon
            # self.initial_hand = self.initial_hand - Unknown() + card
            self.initial_hand = self.initial_hand + card

    def give(self, card: Card):
        self.update_initial_card([card])
        # TODO with Unknwon
        # self.hand = self.hand - Unknown() + card
        self.hand = self.hand + card

    def update_potential_cards(self, cards_played: list):
        for card in cards_played:
            self.potential_cards -= card
        if self.potential_cards.size == self.hand_size:
            self.hand = self.potential_cards

    def play_action(self, action):
        self.actions.append(action)
        if not action.has_passed():
            combination = action.combination
            self.update_initial_card(combination.cards)
            self.update_potential_cards(combination.cards)
            self.hand_size -= combination.size

    def win_trick(self, trick):
        for action in trick:
            if not action.has_passed():
                self.points += action.combination.get_points()

    def is_hand_known(self):
        return self.potential_cards.size == self.hand_size

    def get_hand(self):
        if self.is_hand_known():
            return self.hand

    def is_out(self):
        return self.hand_size == 0