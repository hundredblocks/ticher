from action import Action
from hand import Hand
from players.player import Player

__author__ = 'marc.henri'


class DumbAI(Player):
    cards_played = None
    lead_preference = ['STRAIGHT',
                       'STEPS',
                       'FULLHOUSE',
                       'TRIO',
                       'PAIR',
                       'SINGLE',
                       'SQUAREBOMB',
                       'STRAIGHTBOMB']

    def __init__(self, hand: Hand, name):
        super(DumbAI, self).__init__(hand, name)

    # takes in a game state and returns what to play
    def play(self, trick, wish=None):
        combination_to_play = None

        # if there is a trick being played
        last_play = trick.get_last_play()
        if last_play:

            last_combination = last_play.combination

            combination_to_play = self.hand.find_lowest_combination(last_combination.level, last_combination.type)

        # If we are leading
        else:
            for combination_type in self.lead_preference:
                # -1 otherwise the dog is never played
                combination_to_play = self.hand.find_lowest_combination(-1, combination_type)
                # as soon as a combination is found, play it
                if combination_to_play:
                    break

        if combination_to_play is not None:
            self.hand = self.hand - combination_to_play
            return Action(combination=combination_to_play, player=self)
        else:
            # Empty action means passing
            return Action.passes(player=self)

    def pass_cards(self):
        lowest_card = self.hand.find_lowest_combination(0, 'SINGLE')
        second_lowest_card = (self.hand - lowest_card).find_lowest_combination(0, 'SINGLE')
        third_lowest_card = (self.hand - lowest_card - second_lowest_card).find_lowest_combination(0, 'SINGLE')
        return [lowest_card, third_lowest_card, second_lowest_card]