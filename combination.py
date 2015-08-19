from card import Card, Phoenix, Dog, Dragon, Mahjong
from cards import Cards

__author__ = 'EmmanuelAmeisen'

TYPES = ['LEAD',
         'SINGLE',
         'PAIR',
         'TRIO',
         'FULLHOUSE',
         'STEPS',
         'STRAIGHT',
         'SQUAREBOMB',
         'STRAIGHTBOMB']


BOMBS = ['SQUAREBOMB', 'STRAIGHTBOMB']


class Combination(Cards):
    level = None
    type = None

    def __init__(self, cards_list: list=None, cards_dict_list: list=None, cards_string: str=None, phoenix_power: int=None):
        super(Combination, self).__init__(cards_list, cards_dict_list, cards_string)
        self.get_type()
        self.get_level()
        self._assert_valid()

    def get_type(self):
        phoenixless_combination = [card for card in self.cards if card != Phoenix()]
        combination = [card for card in self.cards]
        phoenixless_combination_size = len(phoenixless_combination)

        if phoenixless_combination_size == 0:
            self.type = 'SINGLE'
            return

        if Dog() in phoenixless_combination and len(combination) > 1:
            raise ValueError('Dog is played alone')

        if Dragon() in phoenixless_combination and len(combination) > 1:
            raise ValueError('Dragon is played alone')

        if Mahjong() in phoenixless_combination and len(combination) == 2 and self.phoenix_flag:
            raise ValueError('No pairs with Mahjong')

        distinct_values = list(set([card.power for card in phoenixless_combination]))
        number_of_values_except_ph = len(distinct_values)

        distinct_suits = list(set([card.suit for card in phoenixless_combination]))
        number_of_suits = len(distinct_suits)

        value_span = max(distinct_values) - min(distinct_values) + 1

        if number_of_values_except_ph == 1:

            if phoenixless_combination_size == 1:
                if not self.phoenix_flag:
                    self.type = 'SINGLE'
                else:
                    self.type = 'PAIR'
                    self.get_phoenix().set_power(max(distinct_values))
                return

            if phoenixless_combination_size == 2:
                if not self.phoenix_flag:
                    self.type = 'PAIR'
                else:
                    self.type = 'TRIO'
                    self.get_phoenix().set_power(max(distinct_values))
                return

            if phoenixless_combination_size == 3:
                self.type = 'TRIO'
                return

            if phoenixless_combination_size == 4 and not self.phoenix_flag:
                self.type = 'SQUAREBOMB'
                return

        elif phoenixless_combination_size == number_of_values_except_ph and len(combination) >= 5:
            if self.phoenix_flag:
                if value_span == phoenixless_combination_size:
                    self.type = 'STRAIGHT'
                    self.get_phoenix().set_power(max(distinct_values) + 1)
                    return
                elif value_span == phoenixless_combination_size + 1:
                    # it is a straight with the phoenix in the middle
                    self.type = 'STRAIGHT'
                    # Not assigning level because of no interest
                    return
                else:
                    raise ValueError('Incoherent Straight')
            if not self.phoenix_flag:
                if value_span != phoenixless_combination_size:
                    raise ValueError('Incoherent Straight')
                if number_of_suits == 1:
                    self.type = 'STRAIGHTBOMB'
                    return
                else:
                    self.type = 'STRAIGHT'
                    return

        # STEPS AND FULLHOUSE
        elif phoenixless_combination_size / 2 == number_of_values_except_ph:
            if self.phoenix_flag and phoenixless_combination_size == 4:
                self.type = 'FULLHOUSE'
                # Not assigning level because of no interest
                return

            elif value_span == phoenixless_combination_size / 2:
                self.type = 'STEPS'
                return
        # TODO [Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St] not working
        elif value_span == phoenixless_combination_size // 2 + 1 and phoenixless_combination_size % 2 == 1 and self.phoenix_flag:
            self.type = 'STEPS'
            # Not assigning level because of no interest
            return

        elif number_of_values_except_ph == 2 and phoenixless_combination_size == 5 and not self.phoenix_flag:
            self.type = 'FULLHOUSE'
            return

        raise ValueError('Unknown Combination %s' % self)

    def get_level(self):
        self.level = max([card.power for card in self.cards])

    def _assert_valid(self):
        assert self.type in TYPES

    def __repr__(self):
        return str({'level': self.level,
                    'type': self.type,
                    'size': self.size,
                    'cards': self.cards,
                    'phoenix': self.phoenix_flag})

    def __ge__(self, other):
        if self.type == other.type:
            return self.level >= other.level
        elif self.type in BOMBS or other.type in BOMBS:
            return TYPES.index(self.type) >= TYPES.index(other.type)

        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __le__(self, other):
        if self.type == other.type:
            return self.level <= other.level
        elif self.type in BOMBS or other.type in BOMBS:
            return TYPES.index(self.type) <= TYPES.index(other.type)
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __gt__(self, other):
        if self.type == other.type:
            return self.level > other.level
        elif self.type in BOMBS or other.type in BOMBS:
            return TYPES.index(self.type) > TYPES.index(other.type)
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __lt__(self, other):
        if self.type == other.type:
            return self.level < other.level
        elif self.type in BOMBS or other.type in BOMBS:
            return TYPES.index(self.type) < TYPES.index(other.type)
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __eq__(self, other):
        return self.level == other.level and self.type == other.type

    def __ne__(self, other):
        return self.level != other.level and self.type != other.type


class Pass(Combination):

    def __init__(self):
        self.size = 0
        self.cards = None
        self.phoenix_flag = False
        self.type = 'PASS'
        self.level = 0

