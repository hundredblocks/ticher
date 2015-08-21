from combinations.combination_analyzer import CombinationAnalyzer

__author__ = 'marc.henri'


class StraightBomb(CombinationAnalyzer):
    name = 'STRAIGHTBOMB'
    bomb = True

    @staticmethod
    def analyze(combination_cards):
        if len(combination_cards.cards) < 5:
            return

        # Make sure it is not a straight bomb
        if len(combination_cards.get_distinct_suits()) != 1:
            return

        distinct_powers = combination_cards.get_distinct_powers(with_phoenix=True)
        if len(distinct_powers) != combination_cards.size:
            return
        # Check value span, depends on Phoenix or not
        if combination_cards.phoenix_flag:
            return

        value_span = combination_cards.get_power_span()
        if value_span != combination_cards.size:
            return

        return [max(distinct_powers)]
