from old_combinations import get_hand_combinations
from state_analyzer import get_type

__author__ = 'EmmanuelAmeisen'





drag = {'value': 'Dragon',
        'suit': 'Special'}

one = {'value': 'Mahjong',
        'suit': 'Special'}


dog = {'value': 'Dog',
        'suit': 'Special'}


phoenix = {'value': 'Phoenix',
        'suit': 'Special'}



ace1 = {'value': 'A',
        'suit': 'Pagoda'}

ace2 = {'value': 'A',
        'suit': 'Sword'}

three1 = {'value': '3',
          'suit': 'Jade'}

three2 = {'value': '3',
          'suit': 'Star'}

three3 = {'value': '3',
          'suit': 'Sword'}

two1 = {'value': '2',
        'suit': 'Sword'}

six1 = {'value': '6',
        'suit': 'Sword'}

eight1 = {'value': '8',
        'suit': 'Sword'}

four1 = {'value': '4',
          'suit': 'Sword'}

four2 = {'value': '4',
          'suit': 'Pagoda'}

five1 = {'value': '5',
          'suit': 'Sword'}

five2 = {'value': '5',
          'suit': 'Star'}

hand1 = [ace1, drag, five2,  dog, five1, eight1, two1, six1,  one, three3, four2, phoenix, three2, four1, ace2, three1]

pair2 = [ace1, ace2]
pair1 = [three1, three2]

#Last played at the end of the array
combination = [pair1, pair2]


def main():
    get_hand_combinations(hand1)


def naive_bot(curr_combinations, hand, cards_played):
    get_lowest_playable_card(curr_combinations, hand)


def get_lowest_playable_card(curr_combinations, hand):
    current_type = get_type(curr_combinations)
    if current_type == 'SINGLE':
        get_lowest_playable_single(curr_combinations, hand)


def get_lowest_playable_single(curr_single, hand):
    pass


def is_card_lower(curr_combinations, card):
    pass


if __name__ == '__main__':
    main()