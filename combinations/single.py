from combinations.combination_analyzer import CombinationAnalyzer

__author__ = 'marc.henri'


class Single(CombinationAnalyzer):
    name = 'SINGLE'
    bomb = False

    @staticmethod
    def analyze(combination_cards):
        if len(combination_cards.cards) != 1:
            return

        # Assuming that the level of the Phoenix has been setup
        level = combination_cards.cards[0].power
        return [level]
