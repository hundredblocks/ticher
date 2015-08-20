from card import Card
from cards import Cards, Deck
from players.base_player import BasePlayer

__author__ = 'marc.henri'


class OtherPlayer(BasePlayer):
    hand = None
    initial_hand = None
    actions = None
    name = None
    potential_cards = None

    def __init__(self, name, hand=None):
        super().__init__(name, hand)
        self.initial_hand = Cards(cards_list=[])
        self.hand = self.initial_hand
        self.potential_cards = Deck()
        self.actions = []

    def update_initial_card(self, cards: list):
        for card in cards:
            if card not in cards:
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

    def is_hand_known(self):
        return self.potential_cards.size == self.hand_size

    def get_hand(self):
        if self.is_hand_known():
            return self.hand