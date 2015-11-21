import unittest
from card import Card, Phoenix
from combinations.combination import Combination
from combinations.straight import Straight

__author__ = 'EmmanuelAmeisen'


class TestCombination(unittest.TestCase):

    def test_pairs(self):

        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='2', suit='Sword')]
        combination = Combination(cards_list=cards)
        self.assertEqual(combination.type, 'PAIR')
        self.assertEqual(combination.level, 2)

    @unittest.expectedFailure
    def test_wrong_pairs(self):

        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='3', suit='Sword')]
        Combination(cards_list=cards)

    def test_pairs_with_phoenix(self):

        cards = [Card(name='2', suit='Pagoda'),
                 Phoenix()]
        combination = Combination(cards_list=cards)
        self.assertEqual(combination.type, 'PAIR')
        self.assertEqual(combination.level, 2)

    def test_triples(self):

        cards = [Card(name='2', suit='Pagoda'),
                 Card(name='2', suit='Sword'),
                 Card(name='2', suit='Jade')]
        combination = Combination(cards_list=cards)
        self.assertEqual(combination.type, 'TRIO')

    @unittest.expectedFailure
    def test_to_fix(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St'
        combination = Combination(cards_string=cards)
        self.assertIsNone(combination.type)

    def test_straight(self):
        cards = 'Phoenix, 3_Pa, 4_Sw, 5_St, 6_Ja, 7_St'
        combination = Combination(cards_string=cards)
        self.assertEqual(combination.type, Straight.name)

    def test_fullhouse(self):
        cards = ' 2_Pa, 2_Sw, 2_Ja, 5_Pa, 5_Sw'
        combination = Combination(cards_string=cards)
        self.assertEqual(combination.type, 'FULLHOUSE')

    def test_straight_with_phoenix(self):
        cards = '2_Sw, 3_Pa, 5_Pa, Phoenix, 6_Pa'
        combination = Combination(cards_string=cards)
        self.assertEqual(combination.type, 'STRAIGHT')

    def test_straight_force_level(self):
        cards = 'Phoenix, 3_Pa, 4_Sw, 5_St, 6_Ja, 7_Sw'
        combination = Combination(cards_string=cards, combo_type=Straight.name, combo_level=7)
        self.assertEqual(combination.type, 'STRAIGHT')

    def test_full_house(self):
        cards = '2_Sw, 2_St, 2_Ja, Phoenix, 3_St'
        combination = Combination(cards_string=cards)

    @unittest.expectedFailure
    def test_full_house_2(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St'
        combination = Combination(cards_string=cards)

    def test_squarebomb(self):
        cards = 'Phoenix, 5_Sw, 5_Pa, 6_Sw'
        combination = Combination(cards_string=cards)
        print(combination)

if __name__ == '__main__':
    unittest.main()
