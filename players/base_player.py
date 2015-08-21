from abc import abstractmethod

__author__ = 'marc.henri'


class BasePlayer():
    hand = None
    name = None
    points = None
    tichu_called = None
    is_first_out = None

    def __init__(self, name, hand=None):
        self.name = name
        self.points = 0
        self.hand = hand
        self.tichu_called = False
        self.is_first_out = False

        if self.hand is not None:
            self.hand_size = len(self.hand.cards)
        else:
            self.hand_size = 14

    def get_trick(self, trick):
        self.points += trick.points

    def is_out(self):
        return self.hand_size == 0

    def out(self, first_out=False):
        self.is_first_out = first_out
        if self.tichu_called:
            if self.is_first_out:
                self.succeed_tichu()
            else:
                self.fail_tichu()

    def call_tichu(self):
        self.tichu_called = True

    def succeed_tichu(self):
        self.points += 100

    def fail_tichu(self):
        self.points -= 100

    def has_not_played(self):
        return self.hand_size == 14

    def __repr__(self):
        return '%s - %s:  %s points' % (self.name, self.hand.cards, self.points)
