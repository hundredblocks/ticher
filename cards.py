from collections import defaultdict
import random
from card import Card, Phoenix, Dragon, Mahjong, Dog

__author__ = 'EmmanuelAmeisen'

#TODO make cards iterable ?
class Cards():
    size = None
    cards = None
    phoenix_flag = None

    def __init__(self, cards_list: list=None, cards_dict_list: list=None, cards_string: str=None):
        # Get phoenix, get type, get level
        new_cards_list = None
        if cards_string is not None:
            new_cards_list = self.parse_string(cards_string)

        if cards_dict_list is not None:
            new_cards_list = [Card(card_dict=card_dict) for card_dict in cards_dict_list]

        if new_cards_list is not None:
            Cards.__init__(self, cards_list=new_cards_list)
            return

        # TODO - Should we break on empty cards list
        # if cards_list is None or len(cards_list) == 0:
        #     raise ValueError('Empty cards list')

        # Check that we do not have duplicates

        if len(set(cards_list)) != len(cards_list):
            raise ValueError('duplicated cards')

        cards_list.sort()
        self.cards = cards_list
        self.size = len(cards_list)
        self.phoenix_flag = Phoenix() in self.cards

    @staticmethod
    def parse_string(cards_string: str):
        split_string = cards_string.replace(' ', '').split(',')
        return [Card(card_string=card_string) for card_string in split_string]

    def get_phoenix(self):
        if not self.phoenix_flag:
            raise ValueError('Can not get phoenix from a hand without it')
        for card in self.cards:
            # if card == Phoenix():
            if card.name == Phoenix.name:
                return card

    def __repr__(self):
        return str({'size': self.size,
                    'cards': self.cards,
                    'phoenix': self.phoenix_flag})

    def __sub__(self, cards_to_remove):
        if type(cards_to_remove) in [Card, Phoenix, Dog, Mahjong, Dragon]:
            cards_to_remove = Cards(cards_list=[cards_to_remove])

        # TODO - using set
        temp_cards = []
        for hand_card in self.cards:
            in_flag = False
            for card in cards_to_remove.cards:
                if card == hand_card and card.suit == hand_card.suit:
                   in_flag = True
            if not in_flag:
                temp_cards.append(hand_card)
        #TODO check for subclasses
        return Cards(temp_cards)
        # return self.__init__(cards_list=temp_cards)

    def __add__(self, cards_to_add):
        if type(cards_to_add) in [Card, Phoenix, Dog, Mahjong, Dragon]:
            cards_to_add = Cards(cards_list=[cards_to_add])

        new_cards = self.cards.copy()
        new_cards.extend(cards_to_add.cards)
        return Cards(new_cards)

    def split_equally(self, integer):
        cards_copy = self.cards.copy()
        random.shuffle(cards_copy)
        return [cards_copy[i::integer] for i in range(integer)]

    @staticmethod
    def bucketize_hands(cards):
        buckets = defaultdict(list)
        for card in cards:
            buckets[card.power].append(card)

        return buckets

    def get_points(self):
        return sum([card.point for card in self.cards])


class Deck(Cards):

    def __init__(self):
        cards = '2_Pa, 3_Pa, 4_Pa, 5_Pa, 6_Pa, 7_Pa, 8_Pa, 9_Pa,10_Pa, J_Pa, Q_Pa, K_Pa, A_Pa, ' \
                '2_Sw, 3_Sw, 4_Sw, 5_Sw, 6_Sw, 7_Sw, 8_Sw, 9_Sw,10_Sw, J_Sw, Q_Sw, K_Sw, A_Sw, ' \
                '2_Ja, 3_Ja, 4_Ja, 5_Ja, 6_Ja, 7_Ja, 8_Ja, 9_Ja,10_Ja, J_Ja, Q_Ja, K_Ja, A_Ja, ' \
                '2_St, 3_St, 4_St, 5_St, 6_St, 7_St, 8_St, 9_St,10_St, J_St, Q_St, K_St, A_St, ' \
                'Mahjong, Dog, Phoenix, Dragon'
        super(Deck, self).__init__(cards_string=cards)