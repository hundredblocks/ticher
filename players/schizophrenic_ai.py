from cards import Cards
from players.player import Player

__author__ = 'EmmanuelAmeisen'


class SchizophrenicAI(Player):

    modes = ['GO_OUT',
             'GET_POINTS',
             'HELP_PARTNER',
             'KILL_TICHU']

    lead_preference = ['STRAIGHT',
                       'STEPS',
                       'FULLHOUSE',
                       'TRIO',
                       'PAIR',
                       'SINGLE',
                       'SQUAREBOMB',
                       'STRAIGHTBOMB']

    mode = None
    player_to_stop = None

    def __init__(self, name, hand):
        super(SchizophrenicAI, self).__init__(name=name, hand=hand)
        # TODO - Tichu and wish (both give and fulfil)


        # self.call_tichu()

    # Gets what mode the AI is currently in
    def update_mode(self):
        partner = self.get_partner()
        # TODO Better way to do opponents
        opponents = [self.other_players[0], self.other_players[2]]
        opponent_tichus = [opponent for opponent in opponents if opponent.tichu_called]

        # TODO rethink tichu logic

        if (not (self.tichu_called or partner.tichu_called)) and self.has_not_played():
            if self.should_i_tichu():
                self.call_tichu()

        # If we call Tichu, we go out
        if self.tichu_called:
            self.mode = 'GO_OUT'

        # If partner calls Tichu, we help while we can. If he fails we avoid the 1-2, if he does it we try to get points.
        elif partner.tichu_called:
            if not partner.is_out():
                if all([not opponent.is_out() for opponent in opponents]):
                    self.mode = 'HELP_PARTNER'
                else:
                    self.mode = 'GO_OUT'
            else:
                self.mode = 'GET_POINTS'

        # If enemy calls tichu we try to stop them, if they make it we avoid the 1-2-Tichu.
        elif any(opponent_tichus):
            if any([not opponent.is_out() for opponent in opponent_tichus]):
                self.mode = 'KILL_TICHU'
                if len(opponent_tichus) == 1:
                    self.player_to_stop = opponent_tichus
                # TODO better logic here
                else:
                    self.player_to_stop = opponent_tichus[0]
            else:
                self.mode = 'GO_OUT'

        # When no tichu is called, we go for points, unless an enemy is out, we try to go out
        else:
            if all([not opponent.is_out() for opponent in opponents]):
                self.mode = 'GET_POINTS'
            else:
                self.mode = 'GO_OUT'

    def should_i_tichu(self):
        # We call tichu if we have at least 6 "Power Cards"
        power_cards = Cards(cards_string='A_Pa, A_Sw, A_Ja, A_St, K_Pa, K_Sw, K_Ja, K_St, Dragon, Phoenix')
        power_limit = 6

        power_card_counter = 0
        for card in self.hand.cards:
            if card in power_cards:
                power_card_counter += 1
        return power_card_counter >= power_limit


    # TODO Change the strategy here
    def combination_to_go_out(self, trick, wish):
        # For now, jsut plays like the dumb AI
        return self.get_lowest_combination(trick, wish)

    def combination_to_get_points(self, trick, wish):
        # We want to get the most point in our trick
        # There is a 100 points total
        # If a trick has more than 15 points in it, we try to win it
        points_in_trick = trick.points
        if points_in_trick < 15:
            return self.get_lowest_combination(trick, wish)
        else:
            return self.get_highest_combination(trick, wish)
        pass

    def combination_to_help_partner(self, trick, wish):
        # Logic here, we pass as long as our partner hasn't passed. If our partner passes, we try to get the lead and play a low single whenever we have the lead

        last_play = trick.get_last_play()
        if last_play:
            actions = trick.actions
            last_combination = last_play.combination

            # If either our partner started or the opponent before him we pass
            if len(actions) <= 2:
                return None

            else:
                partner_actions = [action for action in actions if action.player == self.get_partner()]
                if len(partner_actions) == 1:
                    last_partner_action = partner_actions
                else:
                    last_partner_action = partner_actions[-1]

                # We pass if our partner hasn't
                if not last_partner_action.has_passed():
                    return None

                # We get the lead if he passed
                # TODO play_highest instead of lowest (debatable)
                else:
                    combination_to_play = self.hand.find_lowest_combination(last_combination.level, last_combination.type)
                    return combination_to_play

        else:
            combination_to_play = self.hand.find_lowest_combination(-1, 'SINGLE')
            return combination_to_play

    # TODO implement that
    def get_highest_combination(self, trick, wish):
        pass

    def combination_to_kill_tichu(self, trick, wish):
        # How to kill a Tichuer, you prevent him from playing his non winners by going high instantly
        # 1/If he starts the trick or plays after you, you go super high
        # 2/ If he passed, you unload your cards
        # 3/ If your partner has the lead you assume he played the same logic, so you don't play on top of him
        # 4/If you have the lead, play something exotic
        # Basically, you almost always play super high, than play an exotic combination

        # Go high unless he passed, or he didn't pass and your partner played
        combination_to_play = None
        enemy = self.player_to_stop

        last_play = trick.get_last_play()
        if last_play:
            actions = trick.actions
            last_combination = last_play.combination
            enemy_actions = [action for action in actions if action.player == enemy]

            if len(enemy_actions) == 1:
                last_enemy_action = enemy_actions
            else:
                last_enemy_action = enemy_actions[-1]

            # If the Tichu caller passes, we enjoy it
            if last_enemy_action.has_passed():
                return self.hand.find_lowest_combination(last_combination.level, last_combination.type)

            elif trick.get_last_player() == self.get_partner():
                return None

            else:
                return self.get_highest_combination()

        else:
            for combination_type in self.lead_preference:
                # -1 otherwise the dog is never played
                combination_to_play = self.hand.find_lowest_combination(-1, combination_type)
                # as soon as a combination is found, play it
                if combination_to_play:
                    break

        return combination_to_play

    # takes in a game state and returns what to play
    def get_combination_to_play(self, trick, wish=None):
        combination_to_play = None

        self.update_mode()
        if self.mode == 'GO_OUT':
            return self.combination_to_go_out(trick, wish)

        if self.mode == 'GET_POINTS':
            return self.combination_to_get_points(trick, wish)

        if self.mode == 'HELP_PARTNER':
            return self.combination_to_help_partner(trick, wish)

        if self.mode == 'KILL_TICHU':
            return self.combination_to_kill_tichu(trick, wish)

        # EXAMPLE
        # if Mahjong() in self.hand.cards:
        #     return Combination(cards_list=[Mahjong()])

        # if there is a trick being played

    def get_lowest_combination(self, trick, wish=None):
        combination_to_play = None
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

        # self.wish = lowest_card.cards[0].power

        return [lowest_card.cards[0], third_lowest_card.cards[0], second_lowest_card.cards[0]]

    def get_player_to_pass_dragon_to(self):
        # TODO - check guys is not out
        return self.other_players[-1].name