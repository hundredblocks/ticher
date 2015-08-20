import hashlib

__author__ = 'EmmanuelAmeisen'



suits = ['Star',
         'Sword',
         'Pagoda',
         'Jade']

CARD_VALUES = {'2': 2,
               '3': 3,
               '4': 4,
               '5': 5,
               '6': 6,
               '7': 7,
               '8': 8,
               '9': 9,
               '10': 10,
               'J': 11,
               'Q': 12,
               'K': 13,
               'A': 14,
               'Dragon': 15,
               'Phoenix': 0.5,
               'Mahjong': 1,
               'Dog': 0,
               'unknown': None}


# Format '4_Pa'
class Card():
    point = None
    power = None
    suit = None
    name = None
    special_card = None

    def __init__(self, name=None, suit=None, card_string: str=None, card_dict: dict=None):

        if card_string is not None:
            card_dict = self.parse_string_card(card_string)

        if card_dict is not None:
            self.__init__(**card_dict)
            return

        if name is None and suit is None:
            raise ValueError('Invalid argument name %s or suit %s' % (name, suit))

        self.name = name
        self.suit = suit
        self.special_card = 'Special' == suit
        self.power = CARD_VALUES[self.name]
        self.point = 0
        if self.name in ['5','10', 'K']:
            self.point = (self.power // 5)*5
        if self.name == 'Dragon':
            self.point = 25
        if self.name == 'Phoenix':
            self.point = - 25
        self._assert_valid()

    def _assert_valid(self):
        if not self.special_card:
            assert self.suit in suits

        assert CARD_VALUES[self.name] == self.power

    @staticmethod
    def parse_string_card(string_card):
        if '_' in string_card:
            card = string_card.split('_')
            name = card[0]
            card_suit = card[1]
            for suit in suits:
                if suit.startswith(card_suit):
                    card_suit = suit
                    break
        else:
            name = string_card
            card_suit = 'Special'

        return {'name': name, 'suit': card_suit}

    @staticmethod
    def parse_string(cards_string: str):
        split_string = cards_string.replace(' ', '').split(',')
        return [Card(card_string=card_string) for card_string in split_string]

    def __repr__(self):
        if not self.special_card:
            return '%s_%s' % (self.name, self.suit[0:2])
        return self.name

    def __ge__(self, other):
        return self.power >= other.power

    def __le__(self, other):
        return self.power <= other.power

    def __gt__(self, other):
        return self.power > other.power

    def __lt__(self, other):
        return self.power < other.power

    def __eq__(self, other):
        if self.suit != 'Special':
            return self.power == other.power
        else:
            return self.name == other.name

    def __ne__(self, other):
        return self.power != other.power

    def __hash__(self):
        card_hash = hashlib.md5()
        card_hash.update(self.__repr__().encode())
        card_hash = card_hash.hexdigest()
        card_hash = int(card_hash, 16)
        return card_hash

    def set_power(self, power):
        if self.name != 'Phoenix':
            raise ValueError('Could not set power of a card other than Phoenix')
        self.power = power


class Phoenix(Card):
    name = 'Phoenix'

    def __init__(self):
        # TODO - Update when Card is Updated
        super().__init__(name='Phoenix', suit='Special')

class Dog(Card):

    def __init__(self):
        # TODO - Update when Card is Updated
        super().__init__(name='Dog', suit='Special')


class Dragon(Card):

    def __init__(self):
        # TODO - Update when Card is Updated
        super().__init__(name='Dragon', suit='Special')

class Mahjong(Card):

    def __init__(self):
        # TODO - Update when Card is Updated
        super().__init__(name='Mahjong', suit='Special')


class Unknown(Card):

    def __init__(self):
        super(Unknown, self).__init__(name='unknown', suit='Special')

    def _assert_valid(self):
        return True