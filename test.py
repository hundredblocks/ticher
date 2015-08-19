import inspect
import itertools
import random
from card import Card, Phoenix, Dog, Mahjong, Dragon
from cards import Cards, Deck
from combination import Combination
from game_manager import GameManager
from hand import Hand
from player import Player, DumbAI

__author__ = 'EmmanuelAmeisen'


cards_list = [
    Card(name='2', suit='Pagoda'),
    # Card(name='2', suit='Star'),
    # Card(name='2', suit='Sword'),
    # Card(name='2', suit='Jade'),
    Card(name='3', suit='Pagoda'),
    # Card(name='3', suit='Star'),
    # Card(name='3', suit='Sword'),
    # Card(name='3', suit='Jade'),
    Card(name='4', suit='Pagoda'),
    # Card(name='4', suit='Star'),
    # Card(name='4', suit='Sword'),
    # Card(name='4', suit='Jade'),
    Card(name='5', suit='Pagoda'),
    Card(name='5', suit='Sword'),
    Card(name='5', suit='Jade'),
    Card(name='5', suit='Star'),
    # Card(name='4', suit='Pagoda'),
    # Card(name='4', suit='Star'),
    # Card(name='5', suit='Star'),
    # Card(name='5', suit='Jade'),
    # Card(name='5', suit='Pagoda'),
    # Card(name='5', suit='Sword'),
    # Card(name='7', suit='Star'),
    # Card(name='8', suit='Star'),
    # Card(name='6', suit='Star'),
    # Card(name='9', suit='Star'),
    # Card(name='4', suit='Star'),
    # Card(name='4', suit='Pagoda'),
    # Card(name='4', suit='Pagoda'),
    Phoenix(),
    # Dog(),
    # Mahjong(),
    # Mahjong(),
    # Dragon(),

]
test = [1, 2, 3, 4]

hand1 = Hand(cards_string='K_Pa, K_Sw')
hand2 = Hand(cards_string='Phoenix, A_Pa, Q_Pa')
hand3 = Hand(cards_string='K_Pa, Mahjong, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 6_Pa')
hand4 = Hand(cards_string='J_Pa')
# players = [DumbAI(hand1, 'AI1'), DumbAI(hand2, 'AI2'), DumbAI(hand3, 'AI3'), DumbAI(hand4, 'AI4')]
# players = [DumbAI(Hand(), 'AI1'), DumbAI(Hand(), 'AI2'), DumbAI(Hand(), 'AI3'), DumbAI(Hand(), 'AI4')]

# gman = GameManager(players)
gman = GameManager()

gman.run_game()
