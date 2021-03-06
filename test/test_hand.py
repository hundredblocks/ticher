import unittest

from cards.cards import Cards
from cards.card import Dragon
from cards.hand import Hand

__author__ = 'EmmanuelAmeisen'


class TestHand(unittest.TestCase):

    def test_find_pair(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(4, 'PAIR')
        print(combination)
        self.assertIsNotNone(combination)

    def test_no_mahjong_pair(self):
        cards = 'Phoenix, Mahjong'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(-1, 'PAIR')
        print(combination)
        self.assertIsNone(combination)

    def test_find_low_pair(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(1, 'PAIR')
        print(combination)
        self.assertFalse(combination.phoenix_flag)

    def test_find_low_pair_with_phoenix(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(1, 'PAIR')
        print(combination)
        self.assertTrue(combination.phoenix_flag)

    def test_find_pairs_with_phoenix(self):
        cards = 'Phoenix, 2_Ja, 2_St, 4_Pa, 5_Sw, 5_St, 5_Pa, 7_St, 7_Sw, 8_Sw, 10_St, Q_St, K_St, A_Sw'
        hand = Hand(cards_string=cards)
        cards = Cards(cards_string=cards)
        combination = hand.find_multiple(cards, 11, 3)
        self.assertIsNone(combination)

    def test_find_trio(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(4, 'TRIO')
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_squarebomb(self):
        cards = 'Phoenix, 2_Pa, 3_Pa, 4_Pa, 5_Pa, 5_Sw, 5_Ja, 5_St'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(4, 'SQUAREBOMB')
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_straight_bomb(self):
        cards = '2_Pa, 2_Sw, 3_Pa, 4_Pa, 5_Pa, 6_Pa, 5_Ja, 5_St'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(5, 'STRAIGHT')
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_straight(self):
        cards = '2_Sw, 3_Pa, 4_Pa, 5_Pa, 6_Pa, 5_Ja, 5_St'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(5, 'STRAIGHT')
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_straight_with_phoenix(self):
        cards = '2_Sw, 3_Pa, Phoenix, 5_Pa, 6_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(5, 'STRAIGHT')
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_straight_with_unneeded_phoenix(self):
        cards = '2_Sw, 3_Pa, 4_Sw, Phoenix, 5_Pa, 6_Pa, 7_Sw, 8_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(5, 'STRAIGHT')
        print(combination)
        self.assertIsNotNone(combination)

        combination = hand.find_lowest_combination(5, 'STRAIGHT', length=6)
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_straight_going_up(self):
        cards = ' 4_Sw, Phoenix, 5_Pa, 6_Pa, 7_Sw, 8_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(5, 'STRAIGHT')
        print(combination)
        self.assertIsNotNone(combination)

        combination = hand.find_lowest_combination(5, 'STRAIGHT', length=6)
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_straight_with_card_discard(self):
        cards = ' 4_Sw, 6_Pa, 7_Sw, 8_Pa, 9_Sw, 10_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(3, 'STRAIGHT')
        print(combination)
        self.assertIsNotNone(combination)

    def test_find_steps(self):
        cards = '2_Sw, 2_Pa, 3_Sw,3_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(2, 'STEPS')
        print(combination)
        self.assertEqual(combination.type, 'STEPS')

    def test_find_steps_jump(self):
        cards = '2_Sw, 2_Pa,' \
                ' 6_Sw,6_Pa, 7_Sw, 7_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(2, 'STEPS')
        print(combination)
        self.assertEqual(combination.type, 'STEPS')

    def test_find_steps_no_solution_no_pairs(self):
        cards = '2_Sw, 6_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(2, 'STEPS')

        print(combination)
        self.assertIsNone(combination)

    def test_find_steps_no_solution_with_pairs(self):
        cards = '6_Sw, 6_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(2, 'STEPS')

        print(combination)
        self.assertIsNone(combination)

    def test_3_straights(self):
        cards = '5_Sw, 6_Sw, Phoenix'
        hand = Hand(cards_string=cards)

        straight = hand.find_straight(hand, 6, 3)
        print(straight)

    def test_find_long_steps(self):
        cards = '5_Sw, 5_Pa, 6_Sw,6_Pa, 7_Sw, 7_Pa'
        hand = Hand(cards_string=cards)

        straight = hand.find_straight(hand, 2, 3)
        print(straight)

        combination = hand.find_lowest_combination(2, 'STEPS', 3)
        print(combination)
        self.assertEqual(combination.type, 'STEPS')

    def test_find_long_steps_with_phoenix(self):
        cards = '5_Sw, 5_Pa, 6_Sw, 6_Pa, 7_Sw, Phoenix'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(2, 'STEPS', length=3)
        print(combination)
        self.assertEqual(combination.type, 'STEPS')

    def test_steps_with_phoenix_not_need(self):
        cards = '5_Sw, 5_Pa, 6_Sw, Phoenix, 7_Sw, 7_Pa, 8_Sw, 8_Pa'
        hand = Hand(cards_string=cards)

        combination = hand.find_lowest_combination(2, 'STEPS')
        print(combination)
        self.assertEqual(combination.type, 'STEPS')

    def test_fullhouse(self):

        cards = ' 2_Pa, 2_Sw, 2_Ja, 5_Pa, 5_Sw'
        hand = Hand(cards_string=cards)
        combination = hand.find_lowest_combination(1, 'FULLHOUSE')
        self.assertEqual(combination.type, 'FULLHOUSE')

    def test_stght(self):

        cards = 'Dog, Phoenix, Mahjong, 2_St, 3_Sw, 3_Pa,4_Pa,  5_St, 6_Sw, 6_Ja, 8_Pa, 9_Pa, J_Sw, K_Sw, A_Ja'
        hand = Hand(cards_string=cards)
        combination = hand.find_lowest_combination(0, 'STRAIGHT')
        self.assertEqual(combination.type, 'STRAIGHT')

    def test_stght_2(self):

        # cards = ' 2_St, 2_Sw, 3_Sw, 4_Pa, 5_St, 6_Sw, Phoenix, 8_Ja ' #, 8_Pa, 9_Pa, J_Sw, K_Sw, A_Ja'
        # cards = 'Dog, Phoenix, Mahjong, 2_St, 3_Sw, 3_Pa, 5_St, 6_Sw, 6_Ja, 8_Pa, 9_Pa, J_Sw, Q_Sw, K_Sw, A_Ja'
        # cards = 'Phoenix, 3_Sw, 3_Pa, 4_Sw, 5_St, 6_Sw, 6_Ja, 7_Sw, K_Sw, A_Ja'
        cards = 'Phoenix, 3_Pa, 4_Sw, 5_St, 6_Sw, 6_Ja, 7_Sw, K_Sw, A_Ja'
        # cards = 'Phoenix,2_Pa, 3_Pa, 4_Sw, 5_St, K_Sw, A_Ja'
        # cards = 'Dragon, Phoenix,2_Pa, 3_Pa, J_Sw, Q_St, K_Sw, A_Ja'
        # hand = Hand(cards_string=cards)
        cards = Cards(cards_string=cards)
        combination = Hand.find_all_straights(cards)
        print(*combination, sep='\n')

    def test_all_multiples(self):
        cards = '2_Sw, 2_St, 2_Ja, 3_St, 3_Sw, Phoenix'
        # cards = '3_Sw'
        hand = Hand(cards_string=cards)
        # combination = Hand.find_all_multiples(hand, 2)
        combination = Hand.find_all_multiples(hand, 3)
        # combination = Hand.find_all_multiples(hand, 4)
        print(*combination, sep='\n')

    def test_all_fulls(self):
        cards = '2_Sw, 2_St, 2_Ja, 3_St, 3_Sw, Phoenix'
        # cards = '3_Sw'
        hand = Hand(cards_string=cards)
        combination = Hand.find_all_fullhouses(hand)
        print(*combination, sep='\n')

    def test_phoenix_straight(self):
        # cards = 'Phoenix, 3_Pa, 7_Sw, 7_St, 9_Pa, 9_Ja, 10_St, J_Sw, J_Pa, J_St, Q_Sw, Q_Pa, Q_Ja, A_Sw'
        cards = 'Phoenix, 9_Pa, 10_St, J_Sw, Q_Sw, A_Sw'
        hand = Hand(cards_string=cards)
        combination = hand.find_lowest_combination(5, 'STRAIGHT')
        print(combination)

    def test_cant_beat_high_straight(self):
        cards = '2_Pa, 2_Sw, 3_St, 7_Ja, 8_Ja, 8_St, 8_Pa, 10_Sw, J_Sw, Q_Pa, K_Sw, K_St, A_Sw, Dragon'
        hand = Hand(cards_string=cards)
        combination = hand.find_lowest_combination(14, 'STRAIGHT')
        self.assertIsNone(combination)

    def test_cant_beat_high_straight_with_phoenix(self):
        cards = 'Phoenix, 2_Pa, 2_Sw, 3_St, 7_Ja, 8_Ja, 8_St, 8_Pa, 10_Sw, Q_Pa, K_Sw, K_St, A_Sw, Dragon'
        hand = Hand(cards_string=cards)
        combination = hand.find_lowest_combination(14, 'STRAIGHT')
        self.assertIsNone(combination)

    @unittest.expectedFailure
    def test_play_on_dragon(self):
        cards = 'Phoenix'
        hand = Hand(cards_string=cards)

        print('DRAGON')
        combination = hand.find_lowest_combination(Dragon().power, 'SINGLE')
        print('DRAGON', combination)
        self.assertIsNotNone(combination)

if __name__ == '__main__':
    unittest.main()