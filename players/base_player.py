from abc import abstractmethod

__author__ = 'marc.henri'


class BasePlayer():
    hand = None
    name = None
    points = None

    def __init__(self, name, hand=None):
        self.name = name
        self.points = 0
        self.hand = hand
        if self.hand is not None:
            self.hand_size = len(self.hand.cards)
        else:
            self.hand_size = 14

    def get_trick(self, trick):
        self.points += trick.points

    def is_out(self):
        return self.hand_size == 0