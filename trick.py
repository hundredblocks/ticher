from action import Action

__author__ = 'marc.henri'


class Trick():
    actions = None
    last_player = None
    players = None
    ongoing_passes = None

    def __init__(self, players: int):
        self.actions = []
        self.players = players
        self.ongoing_passes = 0

    def is_first_run(self):
        return len(self.actions) == 0

    def get_last_action(self):
        """
            :rtype Action
        """
        if not self.is_first_run():
            return self.actions[-1]

    def get_last_play(self):
        combinations_played = [play for play in self.actions if not play.has_passed()]
        if len(combinations_played) > 0:
            return combinations_played[-1]

    def reset(self):
        self.__init__(self.players)

    def update(self, valid_action: Action, out=False):
        self.actions.append(valid_action)
        if valid_action.has_passed():
            self.ongoing_passes += 1
        if out:
            self.players -= 1

    def is_over(self):
        return self.ongoing_passes == self.players - 1

    def __repr__(self):
        return 'last combination %s - ongoing passes %s' % (self.get_last_action(), self.ongoing_passes)