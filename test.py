from card import Card, Phoenix
from cards import Cards
from game_manager import GameManager
from hand import Hand
from players.dumb_ai import DumbAI
from players.human_player import HumanPlayer

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

# players = [DumbAI, DumbAI, DumbAI, DumbAI]
players = [HumanPlayer, DumbAI, DumbAI, DumbAI]

# players = [DumbAI(Hand(), 'AI1'), DumbAI(Hand(), 'AI2'), DumbAI(Hand(), 'AI3'), DumbAI(Hand(), 'AI4')]

# gman = GameManager(players)
gman = GameManager(players)
#
gman.run_game()
