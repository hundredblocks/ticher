__author__ = 'EmmanuelAmeisen'


def pretty_print(combination):
    if combination:
        if isinstance(combination[0], list):
            for value in combination:
                if isinstance(value, list):
                    pretty_print(value)
        else:
            pretty_str(combination)


def pretty_str(card_list):
    out = ''
    for card in card_list:
        if card.get('suit') == 'Special':
            card_name = card.get('value')
        else:
            card_name = '%s_%s' % (card.get('value'), card.get('suit')[0:2])
        out = out+card_name+' '
    print(out)