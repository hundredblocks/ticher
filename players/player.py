from queue import Queue

from cards import Cards
from hand import Hand
from players.other_player import OtherPlayer
from trick import Trick
from action import Action


__author__ = 'EmmanuelAmeisen'

# TODO Look into reinforcment learning ? Reducing space of universe ?
# TDLearninfg for temporal differences


class Player():
    hand = None
    name = None
    other_players = None

    def __init__(self, hand: Hand, name):
        self.hand = hand
        self.name = name
        self.other_players = []
        pass

    def set_players_name(self, players_name: list):
        if len(players_name) != 4:
            raise ValueError('incoherent players name passed')

        player_index = players_name.index(self.name)
        for i in range(1, 4):
            index = (player_index + i) % 4
            player_name = players_name[index]
            other_player = OtherPlayer(name=player_name)
            other_player.update_potential_cards(self.hand.cards)
            # other_player.give(self.hand.cards[0])
            self.other_players.append(other_player)

    def play(self, trick: Trick, wish=None):
        pass

    # TODO - Should I bomb or not
    def bomb(self, trick):
        pass

    # TODO - give card logic to implement
    def pass_cards(self):
        pass

    def received_cards(self):
        pass

    def number_of_cards(self):
        return self.hand.size

    def is_out(self):
        return self.number_of_cards() == 0

    def publish_action(self, action, starting):
        if action.player.name != self.name:
            player = self.get_player(action.player)
            player.play_action(action)
        if not action.has_passed():
            for player in self.other_players:
                player.update_potential_cards(action.combination.cards)

                # TODO - Temp
                if not self.is_out() and not player.is_out() and player.is_hand_known():
                    print('!!!###!!! Careful %s - %s knows your hand' % (player.name, self.name),
                          '          cards %s' % (player.get_hand()), sep='\n')

    def __repr__(self):
        return '%s - %s' % (self.name, self.hand.cards)

    # TODO - logic for misplayed
    def misplay(self, action, trick):
        raise ValueError('Illegal Move')

    def get_player(self, player):
        for other_player in self.other_players:
            if other_player.name == player.name:
                return other_player

    def get_partner(self):
        return self.other_players[1]
