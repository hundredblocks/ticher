from card import Phoenix
from cards import Cards
from combinations.combination_analyzer import CombinationAnalyzer

__author__ = 'marc.henri'


class Fullhouse(CombinationAnalyzer):
    name = 'FULLHOUSE'
    bomb = False

    @staticmethod
    def analyze(combination_cards):
        if len(combination_cards.cards) != 5:
            return

        if len(combination_cards.get_distinct_powers(with_phoenix=True)) != 2 and not combination_cards.phoenix_flag:
            return
        if len(combination_cards.get_distinct_powers(with_phoenix=True)) != 3 and combination_cards.phoenix_flag:
            return

        buckets = Cards.bucketize_hands(combination_cards.cards)

        level = None
        phoenix_used = False
        for bucket_level, bucket in buckets.items():
            if bucket_level == Phoenix().power and not combination_cards.phoenix_flag:
                return

            if len(bucket) > 3:
                return

            if len(bucket) == 1:
                if bucket_level != Phoenix().power and combination_cards.phoenix_flag:
                    if phoenix_used:
                        return
                    else:
                        phoenix_used = True

            if len(bucket) == 3:
                level = [bucket_level]

        # Assuming that the level of the Phoenix has been setup
        if level is None:
            level = combination_cards.get_distinct_powers(with_phoenix=False)
            level.sort(reverse=True)

        return level