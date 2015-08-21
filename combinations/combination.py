from cards import Cards
from combinations.fullhouse import Fullhouse
from combinations.pair import Pair
from combinations.single import Single
from combinations.square_bomb import SquareBomb
from combinations.steps import Steps
from combinations.straight import Straight
from combinations.straight_bomb import StraightBomb
from combinations.trio import Trio

__author__ = 'EmmanuelAmeisen'


TYPES = {Single.name: Single,
         Pair.name: Pair,
         Trio.name: Trio,
         SquareBomb.name: SquareBomb,
         Straight.name: Straight,
         StraightBomb.name: StraightBomb,
         Fullhouse.name: Fullhouse,
         Steps.name: Steps
}


class Combination(Cards):
    level = None
    type = None
    bomb_level = None

    def __init__(self, level: int=None, type: str=None, cards_list: list=None, cards_dict_list: list=None, cards_string: str=None, ):
        super(Combination, self).__init__(cards_list, cards_dict_list, cards_string)

        self.level = level
        self.type = type

        if level is not None and type is None:
            raise ValueError('Both parameters should be passed')

        if type is not None and level is None:
            raise ValueError('Both parameters should be passed')

        if self.level is None and self.type is None:
            self.find_combination()

        self._assert_valid()

    def find_combination(self):
        for combination_name, combination_analyzer in TYPES.items():
            analysis = combination_analyzer.analyze(self)
            if analysis:
                self.type = combination_name
                self.level = combination_analyzer.analyze(self)[0]
                if combination_analyzer.bomb:
                    self.bomb_level = self.size
                else:
                    self.bomb_level = 0
                break

    def _assert_valid(self):
        if self.level is None or self.type is None:
            raise ValueError('A combination must have a type and a level')

        if self.type not in TYPES:
            raise ValueError('%s - not in the expected Types' % self.type)

        analysis = TYPES[self.type].analyze(self)

        if analysis:
            if self.level not in analysis:
                raise ValueError('%s - Incoherent analysis of the combinations' % self)
        else:
            raise ValueError('Incoherent combinations type')

    def __repr__(self):
        return str({'level': self.level,
                    'type': self.type,
                    'size': self.size,
                    'cards': self.cards,
                    'phoenix': self.phoenix_flag})

    def __ge__(self, other):
        if self.type == other.type:
            return self.level >= other.level
        elif self.bomb_level > 0 or other.bomb_level > 0:
            return self.bomb_level >= other.bomb_level
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __le__(self, other):
        if self.type == other.type:
            return self.level <= other.level
        elif self.bomb_level > 0 or other.bomb_level > 0:
            return self.bomb_level <= other.bomb_level
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __gt__(self, other):
        if self.type == other.type:
            return self.level > other.level
        elif self.bomb_level > 0 or other.bomb_level > 0:
            return self.bomb_level > other.bomb_level
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __lt__(self, other):
        if self.type == other.type:
            return self.level < other.level
        elif self.bomb_level > 0 or other.bomb_level > 0:
            return self.bomb_level < other.bomb_level
        else:
            raise ValueError('Could not compare different type %s and %s' % (self.type, other.type))

    def __eq__(self, other):
        return self.level == other.level \
                   and self.type == other.type \
                   and self.bomb_level == other.bomb_level \
                   and super(Combination, self).__hash__() == super(Combination, other).__hash__()

    def __ne__(self, other):
        return self.level != other.level and self.type != other.type


class Pass(Combination):

    def __init__(self):
        self.size = 0
        self.cards = None
        self.phoenix_flag = False
        self.type = 'PASS'
        self.level = 0

