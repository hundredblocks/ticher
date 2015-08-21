from card import Phoenix, Dragon
from combinations.combination_analyzer import CombinationAnalyzer

__author__ = 'marc.henri'


class Straight(CombinationAnalyzer):
    name = 'STRAIGHT'
    bomb = False

    @staticmethod
    def analyze(combination_cards):
        if len(combination_cards.cards) < 5:
            return

        distinct_powers = combination_cards.get_distinct_powers(with_phoenix=True)
        if len(distinct_powers) != combination_cards.size:
            return

        # TODO - Phoenix can be instead of One or Dragon

        # Make sure it is not a straight bomb
        if len(combination_cards.get_distinct_suits()) == 1:
            return

        # Check value span, depends on Phoenix or not
        value_span = combination_cards.get_power_span()
        if not combination_cards.phoenix_flag:
            if value_span != combination_cards.size:
                return
            level = max(distinct_powers)

        # If with Phoenix
        else:
            value_span = combination_cards.get_power_span(with_phoenix=False)
            # Check if Phoenix is in the middle
            if value_span == (combination_cards - Phoenix()).size + 1:
                level = max(distinct_powers)
            # If Phoenix is at the end
            elif value_span == (combination_cards - Phoenix()).size:
                return [min(Dragon().power - 1, max(distinct_powers) + 1), max(distinct_powers)]

            else:
                return
        if level:
            return [level]
