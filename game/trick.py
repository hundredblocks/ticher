from game.action import Action

__author__ = 'marc.henri'


class Trick():
    actions = None
    players = None
    ongoing_passes = None
    points = None

    def __init__(self, players: int):
        self.actions = []
        self.players = players
        self.ongoing_passes = 0
        self.points = 0

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

    def get_last_player(self):
        last_play = self.get_last_play()
        if last_play is not None:
            return last_play.player

    def reset(self):
        self.__init__(self.players)

    def update(self, action: Action, out=False):
        self.actions.append(action)
        if action.has_passed():
            self.ongoing_passes += 1
        else:
            self.points += action.combination.get_points()
        if out:
            self.players -= 1

    def is_over(self):
        return self.ongoing_passes == self.players - 1

    def __repr__(self):
        return 'last combination %s - ongoing passes %s' % (self.get_last_action(), self.ongoing_passes)