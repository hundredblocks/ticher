from cards.card import Mahjong
from cards.combination import Combination

__author__ = 'EmmanuelAmeisen'


class ActionsType():
    play = 'play'
    passes = 'pass'
    bomb = 'bomb'


class Action():
    combination = None
    player = None
    action_type = None
    wish = None
    tichu = None

    def __init__(self, player, combination: Combination=None, wish: int=None, bomb=False, tichu=False):
        if combination:
            self.combination = combination
        self.player = player
        if combination is None:
            self.action_type = ActionsType.passes
        else:
            self.action_type = ActionsType.play
        self.wish = wish
        self.tichu = tichu

        if bomb:
            self.action_type = ActionsType.bomb

    def has_passed(self):
        return self.action_type == ActionsType.passes

    @staticmethod
    def passes(player):
        return Action(player)

    @staticmethod
    def play(player, combination: Combination, wish=None, tichu=None):
        return Action(player, combination, wish=wish, tichu=tichu)

    def __repr__(self):
        if self.has_passed():
            return '%s passed' % self.player.name
        else:
            action_string = '%s played %s' % (self.player.name, self.combination)
            if self.wish is not None:
                action_string += ' - wished for %s' % self.wish
            if self.tichu:
                action_string += ' - calling tichu'
            return action_string

    def assert_valid(self):
        if self.action_type == ActionsType.play:
            if self.combination is None:
                raise IllegalAction('a play must come with cards')

        if self.action_type == ActionsType.passes:
            if self.combination is not None:
                raise IllegalAction('No cards can be played while passing')

        if self.wish is not None:
            if self.combination is None and Mahjong() not in self.combination:
                raise IllegalAction('Must play the Mahjong to wish for a card')


class IllegalAction(Exception):
    pass