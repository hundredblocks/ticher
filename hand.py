from collections import defaultdict
import itertools
from card import Phoenix, Dragon, Dog, Mahjong
from cards import Cards
from combinations.combination import Combination

__author__ = 'EmmanuelAmeisen'


# TODO array of combination
# TODO hash of combinations
# TODO sequence of combinations for the AI
# TODO Combinations like hand

# Card, combination, Hand, trick, game, match
class Hand(Cards):
    # TODO Dict with eys = combination name and items is sorted array
    combinations = None

    # Should take in string or list of cards
    def __init__(self, cards_list: list=None, cards_dict_list: list=None, cards_string: str=None):
        super(Hand, self).__init__(cards_list, cards_dict_list, cards_string)
        self.bucketized_cards = self.bucketize_hands(self.cards)
        self.combinations = defaultdict(list)
        self.find_all_combinations()

    def find_all_combinations(self):
        # Find all Single
        cards = Cards(cards_list=self.cards)
        self.combinations['SINGLE'].extend(Hand.find_all_multiples(cards, 1))
        self.combinations['PAIR'].extend(Hand.find_all_multiples(cards, 2))
        self.combinations['TRIO'].extend(Hand.find_all_multiples(cards, 3))
        self.combinations['SQUAREBOMB'].extend(Hand.find_all_multiples(cards, 4))
        self.combinations['STEPS'].extend(Hand.find_all_steps(cards))
        self.combinations['STRAIGHT'].extend(Hand.find_all_straights(cards))
        self.combinations['STRAIGHTBOMB'].extend(Hand.find_all_straights(cards, bomb=True))
        self.combinations['FULLHOUSE'].extend(Hand.find_all_fullhouses(cards))

    def find_lowest_combination(self, level_to_beat, combination_type, length=None):
        potential_combinations = self.combinations[combination_type]
        if len(potential_combinations) == 0:
            return

        # Length
        if combination_type in ['STEPS', 'STRAIGHT']:
            if length is None or length == 0:
                raise ValueError('Please provide combination length for steps and straight')

            potential_combinations = [combination for combination in potential_combinations if combination.size == length]
        potential_combinations = [combination for combination in potential_combinations if combination.level > level_to_beat]

        if len(potential_combinations) > 0:
            potential_combinations.sort()
            return potential_combinations[0]

    # TODO Flag for multiples called favor_no_phoenix, true by default, if false then will just output lowest multiple
    def find_lowest_combination_to_delete(self, level_to_beat, combination_type, length=None):
        # call find_pairs

        multiples = ['SINGLE', 'PAIR', 'TRIO', 'SQUAREBOMB']
        if combination_type in multiples:
            cards_combination = self.find_multiple(self, level_to_beat, multiples.index(combination_type) + 1)

        # TODO Straight and steps length
        elif combination_type == 'STRAIGHT':
            cards_combination = self.find_straight(self, level_to_beat, length)

        elif combination_type == 'STRAIGHTBOMB':
            cards_combination = self.find_straight(self, level_to_beat, length, bomb=True)

        elif combination_type == 'FULLHOUSE':
            trio = self.find_multiple(self, level_to_beat, 3)
            if trio is None:
                return
            duo = self.find_multiple(self - trio, level_to_beat, 2)
            if duo is None:
                return
            cards_combination = duo + trio

        elif combination_type == 'STEPS':
            cards_combination = self.find_steps(self, level_to_beat, length)

        else:
            raise ValueError()

        if cards_combination:
            return Combination(cards_list=cards_combination.cards)

    @staticmethod
    def find_multiple(cards: Cards, level_to_beat: int, cards_to_find: int):
        """
        :param cards:
        :param level_to_beat:
        :param cards_to_find:
        :rtype: Combination
        """

        if cards_to_find <= 0 or cards_to_find > 4:
            raise ValueError('Illegal combination_type %s' % cards_to_find)

        if cards_to_find == 1:
            for card in (cards - Phoenix()).cards:
                if card.power > level_to_beat:
                    return Combination(cards_list=[card])

            # if no card could have been player, try to take the lead with your Phoenix
            # Phoenix can not be played on a Dragon
            if cards.phoenix_flag and level_to_beat < Dragon().power:
                return Combination(cards_list=[Phoenix()])

        # TODO - TO REFACTOR WITH LOGIC
        if cards_to_find == 2:
            for i in range(len(cards.cards) - 1):
                card = cards.cards[i]
                if card.power > level_to_beat and card.power == cards.cards[i+1].power:
                    return Cards(cards_list=[card, cards.cards[i+1]])

        if cards_to_find == 3:
            for i in range(len(cards.cards) - 2):
                card = cards.cards[i]
                if card.power > level_to_beat and card.power == cards.cards[i+2].power:
                    return Cards(cards_list=[card, cards.cards[i+1], cards.cards[i+2]])

        if cards_to_find == 4:
            for i in range(len(cards.cards) - 3):
                card = cards.cards[i]
                if card.power > level_to_beat and card.power == cards.cards[i+3].power:
                    return Cards(cards_list=[card, cards.cards[i+1], cards.cards[i+2], cards.cards[i+3]])

        # If no combination found, try to use Phoenix to play
        if cards.phoenix_flag and 1 <= cards_to_find < 4 and cards.size > 1:
            return Hand.find_multiple(cards - Phoenix(), level_to_beat, cards_to_find - 1) + Phoenix()

    @staticmethod
    def find_straight(cards, level_to_beat, length=None, bomb=False):
        """
        1/ Start at level_to_beat - length +2:
        if level_to_beat is 10, length 6, their straight starts at 5, your straight has to start at 6
        2/ see if you can find a straight that beats that
        3/ see if you can find a length-1 straight at level_to_beat -1
        """
        # Get all possible start points for the straight
        if length is None:
            length = 5
        elif length <= 0:
            return None

        start_point = max(1, level_to_beat - length + 2)
        max_strength_power = Dragon().power - 1
        max_start_point = max_strength_power - length + 2
        start_points = range(start_point, max_start_point + 1)

        for card in cards.cards:
            for start in start_points:
                if card.power == start:
                    if length == 1:
                        return Cards(cards_list=[card])
                    else:
                        # TODO - jump in straights
                        # Issue constantly increasing threshold
                        rest = Hand.find_straight(cards - card, card.power + length - 2, length-1, bomb=bomb)

                        # TODO BOMB
                        if rest:
                            if not rest.phoenix_flag:
                                if min(rest.cards).power == card.power + 1:
                                    return rest + card
                            elif (len(rest.cards) == 1 and Phoenix() in rest.cards) or min((rest - Phoenix()).cards).power <= card.power + 2:
                                    return rest + card

        if cards.phoenix_flag:
            if length == 1:
                return Cards(cards_list=[Phoenix()])

            rest = Hand.find_straight(cards - Phoenix(), level_to_beat, length-1, bomb=bomb)
            if rest:
                return rest + Phoenix()

    @staticmethod
    def find_steps_old(cards, level_to_beat, steps_length=None):
        if steps_length is None:
            steps_length = 2

        starting_pairs_level = level_to_beat - steps_length + 1

        first_pair = Hand.find_multiple(cards, starting_pairs_level, 2)
        # If no pairs
        if not first_pair:
            return

        starting_step_pair = Combination(cards_list=first_pair.cards)

        while starting_step_pair:
            start_pair_level = starting_step_pair.level
            curr_steps_combination = starting_step_pair

            # for i in range(1, length):
            # while number_of_steps < steps_length:
            for number_of_steps in range(1, steps_length + 1):
                target_level = start_pair_level + number_of_steps - 1
                # TODO - Potential issue if the phoenix is need in the middle of it or at the beginning
                next_pair = Hand.find_multiple(cards - starting_step_pair, target_level, 2)
                if next_pair:

                    next_pair_combi = Combination(cards_list=next_pair.cards)

                    if next_pair_combi.level == target_level + 1:
                        curr_steps_combination = curr_steps_combination + next_pair
                        number_of_steps += 1

                        if number_of_steps == steps_length:
                            return Cards(cards_list=curr_steps_combination.cards)

                    else:
                        # Next pairs level is too high - Use this pair as a new start
                        starting_step_pair = next_pair_combi
                        break

                # if there is no next pair, the hand does not contain any pairs
                # No steps could be done, return None
                else:
                    return

    @staticmethod
    def find_steps(cards, level_to_beat, steps_length=None):
        if steps_length is None:
            steps_length = 2

        first_straight = Hand.find_straight(cards, level_to_beat, steps_length)
        # If no pairs
        if not first_straight:
            return
        if first_straight.phoenix_flag:
            return Hand.find_steps(cards, level_to_beat+1, steps_length)

        while first_straight:
            level_to_beat = max(first_straight.cards).power - 1
            second_straight = Hand.find_straight(cards-first_straight, level_to_beat, steps_length)

            if not second_straight:
                return

            # THe level of the second straight can not be lower than the first one
            if max(first_straight.cards).power == max(second_straight.cards).power:
                return first_straight + second_straight

            else:
                if second_straight.phoenix_flag and (max(first_straight.cards)).power - 1 == (max(second_straight.cards)).power:
                    return first_straight + second_straight
                else:
                    first_straight = second_straight

    @staticmethod
    def find_all_steps(cards: Cards):
        buckets = Cards.bucketize_hands((cards - Phoenix()).cards)

        steps = []

        for start in range(Mahjong().power + 1, Dragon().power):
            length = 0
            current_steps = {}
            phoenix_used = False

            for value in range(start, Dragon().power):
                found = False
                cards_at_value = None

                if value in buckets:
                    if len(buckets[value]) >= 2:
                        found = True
                        cards_at_value = buckets[value]

                    elif len(buckets[value]) == 1 and cards.phoenix_flag and not phoenix_used:
                        phoenix_used = True
                        cards_at_value = Cards(cards_list=buckets[value]) + Phoenix()
                        found = True

                if found and value not in current_steps:
                    current_steps[value] = cards_at_value
                    length += 1
                    if length >= 2:
                        steps_cards = [list(itertools.combinations(cards, 2)) for level, cards in current_steps.items()]

                        for combinations in itertools.product(*steps_cards):
                            cards_list = list(itertools.chain(*combinations))
                            combination = Combination(cards_list=cards_list)
                            if combination not in steps:
                                steps.append(combination)
                elif not found:
                    break

        if cards.phoenix_flag:
            Hand.substitute_phoenix_in_combinations(steps)
        return steps

    @staticmethod
    def find_all_multiples(cards: Cards, multiple: int):
        cards = cards - Dog() - Dragon()
        buckets = Cards.bucketize_hands(cards.cards)
        multiples = []
        if multiple == 1:
            for card in cards:
                multiples.append(Combination(cards_list=[card]))
            return multiples

        for level in range(Mahjong().power+1, Dragon().power):
            cards_this_level = buckets[level]
            if (Phoenix().power in buckets.keys()) and (multiple != 4):
                cards_this_level.append(Phoenix())
            if len(cards_this_level) > 1:
                for pair in itertools.combinations(cards_this_level, multiple):
                    multiples.append(Combination(cards_list=list(pair)))
        multiples.sort()

        return multiples

    @staticmethod
    def find_all_straights(cards: Cards, bomb=False):
        # remove Dog and Dragon from any straights
        cards = cards - Dog() - Dragon()

        buckets = Cards.bucketize_hands(cards.cards)
        power_values = buckets.keys()
        possible_straights_power_values = []

        # Get all possible power combinations
        for start in range(Mahjong().power, Dragon().power):

            length = 0
            current_straight_values = []

            for next_value in range(start, Dragon().power):
                found = False
                new_value = None

                if next_value in power_values:
                    found = True
                    new_value = next_value

                elif Phoenix().power in power_values and Phoenix().power not in current_straight_values:
                    if next_value != 1:
                        found = True
                        new_value = Phoenix().power

                if found and new_value not in current_straight_values:
                    current_straight_values.append(new_value)
                    length += 1
                    if length >= 5:
                        possible_straights_power_values.append(current_straight_values.copy())

                elif not found:
                    break

        # Now that we have the powers, we get all possible straights
        straights = []
        for straight in possible_straights_power_values:
            straight_cards = [buckets[power] for power in straight]
            # level = max(straight)
            for combinations in itertools.product(*straight_cards):

                new_combination = Combination(cards_list=list(combinations),)

                if bomb:
                    if new_combination.bomb_level > 0:
                        straights.append(new_combination)
                    else:
                        continue
                else:
                    if new_combination in straights:
                        straights.append(Combination(cards_list=new_combination.cards, combo_type=new_combination.type, combo_level=new_combination.level - 1))
                    else:
                        straights.append(new_combination)

        # We replace the phoenix in all the straights where we can
        if not bomb and cards.phoenix_flag:
            Hand.substitute_phoenix_in_combinations(straights)

        # straights.extend(new_straights)
        straights.sort()
        return straights

    @staticmethod
    def find_all_fullhouses(cards_hand: Cards):
        duos = Hand.find_all_multiples(cards_hand, 2)
        trios = Hand.find_all_multiples(cards_hand, 3)
        fullhouses = []
        for trio in trios:
            possible_duos = [duo for duo in duos if trio.level != duo.level]
            if trio.phoenix_flag:
                possible_duos = [duo for duo in possible_duos if not duo.phoenix_flag]

            for possible_duo in possible_duos:
                fullhouse_cards = trio.cards.copy()
                fullhouse_cards.extend(possible_duo.cards)
                new_fullhouses = Combination(cards_list=fullhouse_cards)

                if new_fullhouses not in fullhouses:
                    fullhouses.append(new_fullhouses)

                if new_fullhouses.phoenix_flag and trio.phoenix_flag:
                    low_fullhouse = Combination(cards_list=fullhouse_cards,
                                                combo_type=new_fullhouses.type,
                                                combo_level=min(new_fullhouses.get_distinct_powers(with_phoenix=False)))

                    if low_fullhouse not in fullhouses:
                        fullhouses.append(low_fullhouse)

        fullhouses.sort()

        return fullhouses

    @staticmethod
    def substitute_phoenix_in_combinations(combinations_list):
        for combination in combinations_list:
            if Phoenix() not in combination:
                for card in combination:
                    if not card == Mahjong():
                        new_cards = combination - card + Phoenix()
                        new_combo = Combination(cards_list=new_cards.cards, combo_level=combination.level, combo_type=combination.type)
                        if new_combo not in combinations_list:
                            combinations_list.append(new_combo)

    def __sub__(self, other):
        cards = super().__sub__(other)
        return Hand(cards_list=cards.cards)

    def __add__(self, other):
        cards = super().__add__(other)
        return Hand(cards_list=cards.cards)
