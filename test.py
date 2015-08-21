import itertools
from card import Card, Phoenix, Dragon
from cards import Cards
from combinations.steps import Steps
from hand import Hand

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
test = [[[1, 2], [1, 3]], [5, 6]]

cards = '5_Sw, 5_Pa, 6_Sw, Phoenix, 7_Sw, 7_Pa, 8_Sw, 8_Pa'
# cards = '5_Sw, 5_Pa, 6_Sw, 6_St, 7_Sw, 7_Pa, 8_Sw, 8_Pa'
cards = Cards(cards_string=cards)

print(*Hand.find_all_steps(cards), sep='\n')

# players = [DumbAI(hand1, 'AI1'), DumbAI(hand2, 'AI2'), DumbAI(hand3, 'AI3'), DumbAI(hand4, 'AI4')]
# players = [DumbAI(Hand(), 'AI1'), DumbAI(Hand(), 'AI2'), DumbAI(Hand(), 'AI3'), DumbAI(Hand(), 'AI4')]

# gman = GameManager(players)
# gman = GameManager()
#
# gman.run_game()
