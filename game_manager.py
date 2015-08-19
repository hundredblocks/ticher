from card import Mahjong
from cards import Deck
import itertools
from hand import Hand
from player import DumbAI

__author__ = 'EmmanuelAmeisen'


class GameManager():
    players = None
    lead_player = None
    present_trick = None
    game_not_finished = None

    def __init__(self, players=None):
        self.game_not_finished = True
        self.update_trick(reset=True)
        cards = Deck()
        divided_cards = cards.split_equally(4)
        if players is None:
            players = [DumbAI(Hand(cards_list=hand), 'Player %s' % index) for index, hand in enumerate(divided_cards)]
        if all(player.hand is None for player in players):
            for idx, player in enumerate(players):
                player.hand = divided_cards[idx]
        for player in players:
            if Mahjong() in player.hand.cards:
                self.lead_player = player
                break
        #TODO How to decide lead player
        else:
            self.lead_player = players[0]

        self.players = players
        print(*['%s - %s' % (player.player_id, player.hand) for player in self.players], sep='\n')

    def check_if_game_finished(self):
        number_still_in = sum([1 if not x.is_out() else 0 for x in self.players])
        if number_still_in <= 1:
            self.game_not_finished = False
        else:
            self.game_not_finished = True

    def run_game(self):

        # Until 3 players are out
        # Game
        while self.game_not_finished:

            starts = len(self.present_trick) == 0
            player_action = self.lead_player.play(self.present_trick)
            self.update_trick(action=player_action)
            self.publish_action_to_players(player_action, self.lead_player, starting=starts)

            self.check_if_game_finished()
            if not self.game_not_finished:
                break
            player_iterator = self.next_active_player()
            if self.lead_player.is_out():
                print('=====> %s is out' % self.lead_player)
                self.lead_player = next(player_iterator)
                continue
            active_player = next(player_iterator)

            # Until somebody wins the hand
            while active_player != self.lead_player:
                player_action = active_player.play(self.present_trick)
                self.update_trick(action=player_action)
                self.publish_action_to_players(player_action, active_player)

                if not player_action.has_passed():
                    self.lead_player = active_player
                    self.check_if_game_finished()
                    if not self.game_not_finished:
                        break
                    if active_player.is_out():
                        print('=====> %s is out' % self.lead_player)
                        self.lead_player = next(player_iterator)
                active_player = next(player_iterator)
            self.update_trick(reset=True)

    def update_lead_player(self, action, player):
        if action:
            if not player.is_out():
                self.lead_player = player
            else:
                player_iterator = self.next_active_player()
                self.lead_player = next(player_iterator)
                #TODO game over ?
                self.check_if_game_finished()

    def publish_action_to_players(self, action, active_player, starting=False):
        print(action, active_player, starting)
        for player in self.players:
            player.publish_action(action, active_player, starting)

    # Returns a cyclic iterators on players still n starting after the start player
    def next_active_player(self):
        # should always be 4
        cycle = itertools.cycle(self.players)
        player = next(cycle)

        while player != self.lead_player:
            player = next(cycle)

        while True:
            player = next(cycle)
            if not player.is_out():
                yield player

    def update_trick(self, action=None, reset=False):
        if reset:
            self.present_trick = []
        else:
            self.present_trick.append(action)




