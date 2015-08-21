from combinations.combination_analyzer import CombinationAnalyzer

__author__ = 'marc.henri'


class Pair(CombinationAnalyzer):
    name = 'PAIR'
    bomb = False

    @staticmethod
    def analyze(combination_cards):
        if len(combination_cards.cards) != 2:
            return

        if len(combination_cards.get_distinct_powers(with_phoenix=True)) != 1 and not combination_cards.phoenix_flag:
            return

        # Assuming that the level of the Phoenix has been setup
        level = max(combination_cards.get_distinct_powers(with_phoenix=False))
        return [level]