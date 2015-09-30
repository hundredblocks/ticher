import itertools
from settings import VALUES
from utils import pretty_print


__author__ = 'EmmanuelAmeisen'

# TODO - Refactor/Remove
def get_hand_combinations(hand):
    hand_sorted = sorted(hand, key=lambda card:  VALUES.get(card.get('value')))

    singles = hand_sorted

    pairs = _find_pairs(hand_sorted)

    triples = _find_triples(hand_sorted)
    fullhouses = _find_fullhouses(hand_sorted)
    steps = _find_steps(hand_sorted)
    straights = _find_straights(hand_sorted)
    print('hand')
    pretty_print(hand)
    print('hand_sorted')
    pretty_print(hand_sorted)
    print('singles')
    # pretty_print(singles)
    print('pairs')
    pretty_print(pairs)
    print('triples')
    # pretty_print(triples)
    print('fullhouses')
    # pretty_print(fullhouses)
    print('steps')
    pretty_print(steps)
    print('straights')
    pretty_print(straights)
    combinations = [singles, pairs, triples, fullhouses, steps]
    print('combinations')
    # pretty_print(combinations)
    return combinations


def _find_pairs(hand_sorted):
    pairs = []
    if hand_sorted[0].get('value') == 'Phoenix':
        phoenix = hand_sorted[0]
        for card in hand_sorted:
            if not card == phoenix and not card.get('suit') == 'Special':
                pairs.append([phoenix, card])

    for index in range(len(hand_sorted)-1):
        if hand_sorted[index].get('value') == hand_sorted[index+1].get('value'):
            pairs.append([hand_sorted[index], hand_sorted[index+1]])
    for index in range(len(hand_sorted)-2):
        if hand_sorted[index].get('value') == hand_sorted[index+2].get('value'):
            pairs.append([hand_sorted[index], hand_sorted[index+2]])
    for index in range(len(hand_sorted)-3):
        if hand_sorted[index].get('value') == hand_sorted[index+3].get('value'):
            pairs.append([hand_sorted[index], hand_sorted[index+3]])

    pairs_sorted = sorted(pairs, key=lambda pair: VALUES.get(pair[0].get('value'))+VALUES.get(pair[1].get('value')))

    return pairs_sorted


def _find_triples(hand_sorted):
    triples = []
    if hand_sorted[0].get('value') == 'Phoenix':
        phoenix = hand_sorted[0]

        for index in range(len(hand_sorted)-1):
            if hand_sorted[index].get('value') == hand_sorted[index+1].get('value'):
                if not hand_sorted[index] == phoenix and not hand_sorted[index].get('suit') == 'Special':
                    triples.append([phoenix, hand_sorted[index], hand_sorted[index+1]])

        for index in range(len(hand_sorted)-2):
            if hand_sorted[index].get('value') == hand_sorted[index+2].get('value'):
                if not hand_sorted[index] == phoenix and not hand_sorted[index].get('suit') == 'Special':
                    triples.append([phoenix, hand_sorted[index], hand_sorted[index+2]])

    for index in range(len(hand_sorted)-2):
        if hand_sorted[index].get('value') == hand_sorted[index+1].get('value') and hand_sorted[index+1].get('value') == hand_sorted[index+2].get('value'):
            triples.append([hand_sorted[index], hand_sorted[index+1], hand_sorted[index+2]])

    triples_sorted = sorted(triples, key=lambda triple: VALUES.get(triple[0].get('value'))+VALUES.get(triple[1].get('value'))+VALUES.get(triple[2].get('value')))

    return triples_sorted


def _find_fullhouses(hand_sorted):
    pairs = _find_pairs(hand_sorted)
    triples = _find_triples(hand_sorted)
    fullhouses = []

    for pair in pairs:
        for triple in triples:
            # if they have the same value, it means phoenix is used incorrecly or cards are repeated
            if not pair[0].get('value') == triple[0].get('value') and not pair[1].get('value') == triple[1].get('value'):
                pair_copy = pair.copy()
                pair_copy.extend(triple)
                fullhouses.append(pair_copy)
    fullhouses_sorted = sorted(fullhouses, key=lambda fullhouse: VALUES.get(fullhouse[0].get('value'))+VALUES.get(fullhouse[1].get('value')) +
                               VALUES.get(fullhouse[2].get('value'))+VALUES.get(fullhouse[3].get('value'))+VALUES.get(fullhouse[4].get('value')))

    return fullhouses_sorted


def _find_steps(hand_sorted):
    pairs = _find_pairs(hand_sorted)
    steps = []
    for pair1 in pairs:
        curr_top_pair = pair1
        pair_copy = pair1.copy()
        curr_has_phoenix = pair1[0].get('value') == 'Phoenix'
        for pair2 in itertools.filterfalse(lambda x: x == pair1, pairs):
            adds_phoenix = pair2[0].get('value') == 'Phoenix'
            possible = not (curr_has_phoenix and adds_phoenix)
            if VALUES.get(curr_top_pair[1].get('value'))+1 == VALUES.get(pair2[1].get('value')) and possible:
                curr_has_phoenix = curr_has_phoenix or adds_phoenix

                curr_top_pair = pair2
                # need to copy to not modify the list inside steps
                pair_c = pair_copy.copy()
                pair_copy.extend(pair2)
                pair_c.extend(pair2)

                steps.append(pair_c)

    steps_sorted = sorted(steps, key=lambda step: VALUES.get(step[0].get('value'))+VALUES.get(step[2].get('value')))

    return steps_sorted


def _find_straights(hand_sorted):
    straights = []

    for card1_index in range(len(hand_sorted)):
        straight = [hand_sorted[card1_index]]

        for card2_index in range(card1_index, len(hand_sorted)):

            if VALUES.get(hand_sorted[card1_index].get('value'))+1 == VALUES.get(hand_sorted[card2_index].get('value')):
                straight.append(hand_sorted[card2_index])

        if len(straight) > 4:
            straights.append(straight)

    '''
    1/ find normal straights
    2/ add a phoenix at start/end of each of them, and replace each of the cards with a phoenix
    3/ find one hole straights and fill them
    '''
    # Phoenix in middle/end
    if hand_sorted[0].get('value') == 'Phoenix':
        phoenix = hand_sorted[0]
        phoenix_used = False

        for card1_index in range(1, len(hand_sorted)):
            value = hand_sorted[card1_index].get('value')
            is_legal = not(value == 'Dog' or value == 'Dragon')

            if is_legal:
                straight = [hand_sorted[card1_index]]
                max_value = VALUES.get(hand_sorted[card1_index].get('value'))

                for card2_index in range(card1_index, len(hand_sorted)):
                    value2 = hand_sorted[card1_index].get('value')
                    is_legal2 = not(value2 == 'Dog' or value2 == 'Dragon')

                    if is_legal2:

                        if max_value+1 == VALUES.get(hand_sorted[card2_index].get('value')):
                            straight.append(hand_sorted[card2_index])
                            max_value += 1

                            if len(straight) > 4:
                                straight_2 = straight.copy()
                                straights.append(straight_2)

                        elif max_value + 1 < VALUES.get(hand_sorted[card2_index].get('value')) and not phoenix_used:
                            straight.append(phoenix)
                            phoenix_used = True
                            max_value += 1

                            if len(straight) > 4:
                                straight_2 = straight.copy()
                                straights.append(straight_2)

    straights_sorted = sorted(straights, key=lambda comb: VALUES.get(comb[0].get('value')) + len(comb)*100)

    return straights_sorted


# a straight bomb is a straight, without the 1, that is of only one color
def find_straight_bomb():
    pass


# two pairs of the same level without a phoenix
def find_square_bomb(hand_sorted):
    for card_index in range(len(hand_sorted)-3):
        if hand_sorted[card_index].get('value') == hand_sorted[card_index+1].get('value') == hand_sorted[card_index+2].get('value') == hand_sorted[card_index+3].get('value'):
            pass