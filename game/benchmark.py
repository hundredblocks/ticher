from cards.cards import Deck
from cards.hand import Hand
from game.game_manager import GameManager
from players.dumb_ai import DumbAI
from players.player import Player


class Bench:

    def __init__(self, to_bench:Player, bench_against:Player=DumbAI, num_iterations=100):
        self.to_bench = to_bench
        self.bench_against = bench_against
        self.num_iterations = num_iterations

    def bench(self):
        for i in range(self.num_iterations):
            deck = Deck()
            hands = deck.split_equally(4)
            players = [self.to_bench(hand=Hand(hands[0]), name='AI1'), self.bench_against(hand=Hand(hands[1]), name='AI2'),
                       self.to_bench(hand=Hand(hands[2]), name='AI3'), self.bench_against(hand=Hand(hands[3]), name='AI4')]

            gman = GameManager(players=players)
            gman.run_game()
            print("=========>", gman)
