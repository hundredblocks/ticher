from action import Action
from card import Mahjong
from combination import Combination
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

    def __init__(self, name, hand):
        super(DumbAI, self).__init__(name=name, hand=hand)

    # takes in a game state and returns what to play
    def get_combination_to_play(self, trick, wish=None):
        combination_to_play = None

        if Mahjong() in self.hand.cards:
            return Combination(cards_list=[Mahjong()])

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

        return combination_to_play

    def get_cards_to_give(self):

        lowest_card = self.hand.find_lowest_combination(-1, 'SINGLE')
        second_lowest_card = (self.hand - lowest_card).find_lowest_combination(-1, 'SINGLE')
        third_lowest_card = (self.hand - lowest_card - second_lowest_card).find_lowest_combination(-1, 'SINGLE')

        self.wish = lowest_card.cards[0].power

        return [lowest_card.cards[0], third_lowest_card.cards[0], second_lowest_card.cards[0]]

    def get_player_to_pass_dragon_to(self):
        # TODO - check guys is not out
        return self.other_players[-1].name

    # def bomb(self, trick):
    #     if self.name == 'Player 1':
    #         combination = Combination(cards_string='J_Pa, J_Sw, J_Ja, J_St')
    #         # if combination > trick.get_last_play().combination:
    #         return Action(self, combination=combination)
    #     if self.name == 'Player 2':
    #         combination = Combination(cards_string='A_Pa, A_Sw, A_Ja, A_St')
    #         return Action(self, combination= combination)