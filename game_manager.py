import itertools

from card import Mahjong, Dragon, Dog

from cards import Deck
from hand import Hand
from players.dumb_ai import DumbAI
from trick import Trick


__author__ = 'EmmanuelAmeisen'


class GameManager():
    players = None
    lead_player = None
    present_trick = None
    game_over = None

    wish_for_power = None

    def __init__(self, players=None):
        self.game_over = False
        cards = Deck()
        divided_cards = cards.split_equally(4)
        if players is None:
            players = [DumbAI(hand=Hand(cards_list=hand), name='Player %s' % index) for index, hand in enumerate(divided_cards)]
        if all(player.hand is None for player in players):
            for idx, player in enumerate(players):
                player.hand = divided_cards[idx]

        self.players = players
        for player in self.players:
            player.create_players([p.name for p in self.players])

        print(*['%s - %s' % (player.name, player.hand) for player in self.players], sep='\n')

        self.present_trick = Trick(len(self.get_player_still_game()))

    def check_if_game_finished(self):
        number_still_in = sum([1 if not x.is_out() else 0 for x in self.players])
        if number_still_in <= 1:
            self.game_over = False
        else:
            self.game_over = True

    def is_game_over(self):
        if self.game_over:
            return True

        # CHECK if both people from same team are out
        self.game_over = sum([1 if not x.is_out() else 0 for x in self.players]) <= 1
        return self.game_over

    def run_game(self):

        # Until 3 players are out
        # Game
        self.exchange_cards()

        for player in self.players:
            if Mahjong() in player.hand.cards:
                self.lead_player = player
                break

        #TODO How to decide lead player
        else:
            self.lead_player = self.players[0]

        while not self.is_game_over():
            print('',
                  '### new trick with players %s' %
                  (', '.join(['%s (%spts)' % (player.name, player.points) for player in self.get_player_still_game()])),
                  '### leading player is %s' % self.lead_player,
                  '### trick - %s' % self.present_trick,
                  '',
                  sep='\n')
            # Take action from the lead player
            self.get_player_action(self.lead_player)

            # Check if game is over
            if self.is_game_over():
                continue
            self.check_for_bomb()

            # Initialize the rolling cycle of player
            player_iterator = self.next_active_player()

            if self.lead_player.is_out():
                self.lead_player = next(player_iterator)
                continue

            active_player = next(player_iterator)

            # Until somebody wins the hand
            while not self.present_trick.is_over() and not self.is_game_over():
                player_action = self.get_player_action(active_player)

                if not player_action.has_passed():

                    # Check if game is over
                    if self.is_game_over():
                        break

                    self.check_for_bomb()

                    if self.lead_player.is_out():
                        self.lead_player = next(player_iterator)

                self.check_for_bomb()
                active_player = next(player_iterator)

            self.end_of_trick()

    def publish_action_to_players(self, action, starting=False):
        for player in self.players:
            player.publish_action(action, starting)

    def end_of_trick(self):

        last_play = self.present_trick.get_last_play()
        trick_owner = self.present_trick.get_last_player()

        if Dragon() in last_play.combination.cards:
            trick_owner_name = trick_owner.get_player_to_pass_dragon_to()
            print('Trick is given to %s' % trick_owner_name)
        else:
            trick_owner_name = trick_owner.name

        # notify all players
        for player in self.players:
                player.end_of_trick(trick_owner_name=trick_owner_name, trick=self.present_trick)

        self.present_trick.reset()

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

    def get_player_action(self, player=None, bomb=False):
        if player is None:
            player = self.lead_player

        # Check for any bomb here
        if bomb:
            player_action = player.bomb(self.present_trick)
            # Do not update anything for bomb
            if player_action is None:
                return
        else:
            player_action = player.play(self.present_trick, self.wish_for_power)

        print(player_action)
        # Ensure action is valid
        try:
            self.assert_valid_action(player, player_action)

            if player_action.wish is not None:
                self.wish_for_power = player_action.wish

            # TODO - TEMP
            if player.is_out():
                print('=====> %s is out' % player)

            self.present_trick.update(action=player_action, out=player.is_out())
            self.publish_action_to_players(action=player_action,
                                           starting=self.present_trick.is_first_run())

            if not player_action.has_passed():
                self.lead_player = player

                if Dog() in player_action.combination.cards:
                    self.lead_player = self.get_player(player.get_partner().name)
                    self.end_of_trick()

            return player_action

        except Exception as e:
            print('AI Error - %s' % e)
            # If not valid, publish an error message to the player
            player.misplay(player_action, self.present_trick)
            raise ValueError(e)

    # FOR THE MOMENT ONLY check for bomb in the order
    def check_for_bomb(self):
        for player in self.get_player_still_game():
            # Assuming that people would not terminate on a Bomb
            self.get_player_action(player, bomb=True)

    def assert_valid_action(self, player, action):
        if self.present_trick.is_first_run() and action.has_passed() and not player.is_out():
            raise GameManagerException('Cannot pass on an empty trick')

        if self.present_trick is not None and not action.has_passed():
            # Make sure action is valid
            action.assert_valid()
            last_play = self.present_trick.get_last_play()

            if last_play:
                if last_play.combination >= action.combination:
                    raise GameManagerException('Combination should be greater than last played')

        if self.wish_for_power is not None:
            if self.wish_for_power in [card.power for card in action.combination.cards]:
                self.wish_for_power = None

            # TODO assert for combination not possible
            elif self.wish_for_power in [card.power for card in player.hand.cards]:
                raise GameManagerException('Wish should be fulfilled')

    def get_player_still_game(self):
        return [player for player in self.players if not player.is_out()]

    def exchange_cards(self):
        # Get all cards
        exchanged_cards = {}
        for player in self.players:
            exchanged_cards[player.name] = player.give_cards()

            print('%s gives %s' % (player.name, exchanged_cards[player.name]))

        for from_player, gifts in exchanged_cards.items():
            for player_to_give, card in gifts.items():
                self.get_player(player_to_give).received_card(from_player, card)

    def get_player(self, player_name):
        for player in self.players:
            if player.name == player_name:
                return player


class GameManagerException(Exception):
    pass




