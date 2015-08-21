from card import Phoenix
from cards import Cards
from combinations.combination_analyzer import CombinationAnalyzer

__author__ = 'marc.henri'


class Steps(CombinationAnalyzer):
    name = 'STEPS'
    bomb = False

    @staticmethod
    def analyze(combination_cards):
        if combination_cards.size % 2 != 0:
            return

        if combination_cards.size < 4:
            return

        buckets = Cards.bucketize_hands((combination_cards - Phoenix()).cards)

        phoenix_used = False
        buckets_level = buckets.keys()
        for bucket_level in buckets_level:

            if len(buckets[bucket_level]) > 2:
                return

            if bucket_level != max(buckets_level) and bucket_level + 1 not in buckets:
                return

            if len(buckets[bucket_level]) == 1:
                if not combination_cards.phoenix_flag:
                    return
                elif not phoenix_used:
                    phoenix_used = True
                else:
                    return

        # Assuming that the level of the Phoenix has been setup
        level = max(buckets_level)
        return [level]
