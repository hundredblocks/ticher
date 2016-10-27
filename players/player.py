from abc import abstractmethod

from cards.card import Mahjong
from cards.combination import Combination
from game.action import Action
from game.trick import Trick
from players.base_player import BasePlayer
from players.other_player import OtherPlayer

__author__ = 'EmmanuelAmeisen'

# TODO Look into reinforcment learning ? Reducing space of universe ?
# TDLearninfg for temporal differences


class Player(BasePlayer):
    other_players = None
    wish = None

    def __init__(self, name, hand=None):
        super().__init__(name, hand)
        self.other_players = []

    def create_players(self, players_name: list):
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
        combination_to_play = self.get_combination_to_play(trick, wish)

        if combination_to_play is not None:
            action_params = {}

            if self.has_not_played():
                action_params['tichu'] = self.tichu_called

            if Mahjong() in combination_to_play.cards:
                action_params['wish'] = self.wish

            self.hand -= combination_to_play
            # self.hand.remove_played(combination_to_play)
            self.hand_size -= combination_to_play.size

            return Action.play(player=self, combination=combination_to_play, **action_params)

        else:
            # Empty action means passing
            return Action.passes(player=self)

    @abstractmethod
    def get_combination_to_play(self, trick, wish):
        """
            :rtype: Combination
        """
        pass

    @abstractmethod
    def bomb(self, trick):
        pass

    def give_cards(self):
        """
            :rtype: Dict (player_name, card)
        """
        cards = self.get_cards_to_give()
        gifts = {}
        for index, player in enumerate(self.other_players):
            card = cards[index]
            player_name = player.name

            gifts[player_name] = card
            self.hand -= card
            self.get_player(player_name).give(card)
            for other_player in self.other_players:
                if other_player.name != player_name:
                    self.get_player(other_player.name).update_potential_cards([card])

        return gifts

    @abstractmethod
    def get_cards_to_give(self):
        pass

    def received_card(self, from_player_name, card):
        from_player = self.get_player(from_player_name)
        from_player.update_potential_cards([card])
        self.hand += card

    @abstractmethod
    def get_player_to_pass_dragon_to(self):
        pass

    # TODO - logic for misplayed
    def misplay(self, action, trick):
        raise ValueError('Illegal Move %s on trick %s' % (action, trick))

    def publish_action(self, action, starting):
        if action.player.name != self.name:
            player = self.get_player(action.player.name)
            player.play_action(action)

            if not action.has_passed():
                for player in self.other_players:
                    player.update_potential_cards(action.combination.cards)

                    # TODO - Temp
                    if not self.is_out() and not player.is_out() and player.is_hand_known():
                        print('!!!###!!! Careful %s - %s knows your hand' % (player.name, self.name),
                              '          cards %s - points %s' % (player.get_hand(), player.points),
                              sep='\n')

            if action.tichu:
                player.call_tichu()

    def player_out(self, player_name, is_first=False):
        if self.name != player_name:
            player = self.get_player(player_name)
            player.out(first_out=is_first)
        else:
            self.out(first_out=is_first)

    def end_of_trick(self, trick_owner_name, trick):
        if trick_owner_name != self.name:
            player = self.get_player(trick_owner_name)
            player.get_trick(trick)
        else:
            self.get_trick(trick)

    def get_player(self, player_name):
        for other_player in self.other_players:
            if other_player.name == player_name:
                return other_player

    def get_partner(self):
        return self.other_players[1]
