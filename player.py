from queue import Queue
from hand import Hand
from combination import Pass
from action import Action

__author__ = 'EmmanuelAmeisen'

# TODO Look into reinforcment learning ? Reducing space of universe ?
# TDLearninfg for temporal differences


class Player():
    hand = None
    initial_hand = None
    player_id = None
    other_players = None
    queue = None

    def __init__(self, hand: Hand, player_id):
        self.hand = hand
        self.player_id = player_id
        self.queue = Queue()

    def play(self):
        """

        :param game:
        :rtype: Action
        """
        pass

    def pass_cards(self):
        """

        :rtype: Cards
        """
        pass

    def number_of_cards(self):
        return self.hand.size

    def is_out(self):
        return self.number_of_cards() == 0

    def publish_action(self, action, player_id, starting):
        self.queue.put({'action': action,
                         'player': player_id,
                         'starting': starting})

    def __repr__(self):
        return self.player_id


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

    def __init__(self, hand: Hand, player_id):
        super(DumbAI, self).__init__(hand, player_id)

    # takes in a game state and returns what to play
    def play(self, trick):
        combination_to_play = None

        # if there is a trick being played
        if trick:

            trick_no_passes = [play for play in trick if not play.has_passed()]
            # TODO ???
            last_play = trick_no_passes[-1]
            last_combination = last_play.action

            combination_to_play = self.hand.find_lowest_combination(last_combination.level, last_combination.type)

        # If we are leading
        else:
            for combination_type in self.lead_preference:
                combination_to_play = self.hand.find_lowest_combination(0, combination_type)
                # as soon as a combination is found, play it
                if combination_to_play:
                    break

        if combination_to_play:
            self.hand = self.hand - combination_to_play
            return Action(combination=combination_to_play)
        else:
            # Empty action means passing
            return Action.passes()

    def pass_cards(self):
        lowest_card = self.hand.find_lowest_combination(0, 'SINGLE')
        second_lowest_card = (self.hand - lowest_card).find_lowest_combination(0, 'SINGLE')
        third_lowest_card = (self.hand - lowest_card - second_lowest_card).find_lowest_combination(0, 'SINGLE')
        return [lowest_card, third_lowest_card, second_lowest_card]



