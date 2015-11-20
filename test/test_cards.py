import unittest
from card import Card, Phoenix
from cards import Cards
from combinations.combination import Combination

__author__ = 'EmmanuelAmeisen'


class TestCards(unittest.TestCase):

    def test_sub(self):
        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='2', suit='Sword')]
        cards = Cards(cards_list=cards)

        cards_to_remove = Cards(cards_list=[Card(name='2', suit='Sword')])

        cards = cards - cards_to_remove
        self.assertEqual(cards.size, 1)

    def test_add(self):
        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='2', suit='Sword')]
        cards = Cards(cards_list=cards)

        cards_to_remove = Cards(cards_list=[Card(name='3', suit='Sword')])

        cards = cards + cards_to_remove
        self.assertEqual(cards.size, 3)

    def test_add_card(self):
        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='2', suit='Sword')]
        cards = Cards(cards_list=cards)

        cards = cards + Card(name='3', suit='Sword')
        self.assertEqual(cards.size, 3)

    @unittest.expectedFailure
    def test_add_same(self):
        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='2', suit='Sword')]
        cards = Cards(cards_list=cards)
        cards_to_remove = Cards(cards_list=[Card(name='2', suit='Sword')])
        cards = cards + cards_to_remove
        self.assertEqual(cards.size, 3)

if __name__ == '__main__':
    unittest.main()
