__author__ = 'EmmanuelAmeisen'


class Action():
    action = None

    def __init__(self, combination=None):
        if combination:
            self.action = combination

    def has_passed(self):
        return not self.action

    @staticmethod
    def passes():
        return Action()

    def __repr__(self):
        if self.has_passed():
            return 'pass'
        else:
            return str(self.action)