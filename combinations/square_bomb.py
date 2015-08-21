from combinations.combination_analyzer import CombinationAnalyzer


class SquareBomb(CombinationAnalyzer):
    name = 'SQUAREBOMB'
    bomb = True

    @staticmethod
    def analyze(combination_cards):
        if len(combination_cards.cards) != 4:
            return

        if combination_cards.phoenix_flag:
            return

        if len(combination_cards.get_distinct_powers(with_phoenix=True)) != 1:
            return

        # Assuming that the level of the Phoenix has been setup
        level = max(combination_cards.get_distinct_powers(with_phoenix=False))
        return [level]
