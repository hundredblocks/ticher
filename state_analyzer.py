from settings import VALUES

__author__ = 'EmmanuelAmeisen'


# We assume that the combinations are valid
def get_type(curr_combination):
    if curr_combination:
        last_played = curr_combination[-1]
        combination_size = len(last_played)
        if combination_size == 1:
            return 'SINGLE'
        if combination_size == 2:
            return 'PAIR'
        if combination_size == 3:
            return 'TRIO'
        #TODO Check for phoenix here
        if combination_size == 4:
            value_list = [x.get('value') for x in last_played]
            if value_list[0] == value_list[1] and value_list[1] == value_list[2]:
                return 'SQUAREBOMB'
            else:
                return 'STEPS'
        last_played_sorted = sorted(last_played, key=lambda card:  VALUES.get(card.get('value')))
        if combination_size == 5:
            value_list = [x.get('value') for x in last_played_sorted]

            if value_list[0] == value_list[1]:
                #TODO get_fullhouse_level()
                return 'FULLHOUSE'

            if are_same_suit(last_played_sorted):
                return 'STRAIGHTBOMB'

            else:
                return 'STRAIGHT'

        if combination_size >= 6:
            value_list = [x.get('value') for x in last_played_sorted]
            if value_list[0] == value_list[1]:
                return 'STEPS'
            if are_same_suit(last_played_sorted):
                return 'STRAIGHTBOMB'
            else:
                return 'STRAIGHT'
    else:
        return 'LEAD'


def are_same_suit(cards):
    suits = [x.get('suit') for x in cards]
    current_suit = suits[0]
    for i in range(1, len(suits)):
        if not suits[i] == current_suit:
            return False
    return True