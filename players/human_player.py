from action import Action
from card import Mahjong, Card
from combinations.combination import Combination
from hand import Hand
from players.player import Player

__author__ = 'marc.henri'


class HumanPlayer(Player):
    cards_played = None

    def __init__(self, name, hand):
        super().__init__(name=name, hand=hand)

    # TODO - Replace lowest by pulling from combinations (than update combinations)
    # takes in a game state and returns what to play
    def get_combination_to_play(self, trick, wish=None):
        print('Trick is', trick)
        print('Your Hand is', self.hand)

        play_chosen = input('Choose your play:')

        if play_chosen == 'pass':
            return None

        else:
            return Combination(cards_string=play_chosen)

    # TODO - Replace lowest by pulling from combinations (than update combinations)
    def get_cards_to_give(self):

        print('Your Hand is', self.hand)

        play_chosen = input('Choose cards to give (1, left, 2, artner, 3, right play) - press auto:')

        if play_chosen == 'auto':
            lowest_card = self.hand.find_lowest_combination(-1, 'SINGLE')
            second_lowest_card = (self.hand - lowest_card).find_lowest_combination(-1, 'SINGLE')
            third_lowest_card = (self.hand - lowest_card - second_lowest_card).find_lowest_combination(-1, 'SINGLE')

            return [lowest_card.cards[0], third_lowest_card.cards[0], second_lowest_card.cards[0]]

        cards = play_chosen.split(',', 2)
        return [Card(card_string=cards[0]), Card(card_string=cards[1]), Card(card_string=cards[2])]

    def bomb(self, trick):
        if len(self.hand.combinations['SQUAREBOMB']) > 0:
            play_chosen = input('Do you want to play your bomb')
            if play_chosen == 'y':
                return self.hand.combinations['SQUAREBOMB'][0]

        print('Too bad you can not bomb it')