import itertools

RANK_ORDER = '34567890JQKA2'
SUIT_ORDER = 'DCHS'
POKER_ORDER = ['straight', 'flush', 'full house', 'four of a kind', 'straight flush']
RANK_ARRAY = list(RANK_ORDER)
SUIT_ARRAY = list(SUIT_ORDER)


def playerTurn(current_player, hand, play_to_beat, is_start_of_round):
    played = False
    while not played:
        if len(play_to_beat) == 0:
            if is_start_of_round:
                print('\n')
                print('It is the start of the round and your play must contain [\'3D\']')
                print('\n')
                play = input('Please enter a play: ')
                play = play.upper()
                if len(play) == 2:
                    if '3D' in play:
                        hand.remove(play)
                        play = [play]
                        played = True
                        return play
                    else:
                        print('That play does not contain the 3 of Diamonds!')
                elif len(play) > 3:
                    play = play.split()
                    if len(play) == 2:
                        if '3D' in play and is_pair(play[0], play[1]):
                            try:
                                for x in play:
                                    current_player.hand.remove(x)
                                played = True
                                return play
                            except ValueError:
                                print('That pair is not in your hand!')
                        else:
                            print('That is not a valid play!')
                    elif len(play) == 3:
                        if '3D' in play and is_three(play[0], play[1], play[2]):
                            try:
                                for x in play:
                                    current_player.hand.remove(x)
                                played = True
                                return play
                            except ValueError:
                                print('That triple is not in your hand!')
                    elif len(play) == 5:
                        if '3D' in play and is_quintuple(play):
                            try:
                                for x in play:
                                    current_player.hand.remove(x)
                                played = True
                                return play
                            except ValueError:
                                print('That play is not in your hand.')

            else:  # start of trick
                print('You may play anything you like.')
                print('\n')
                print('Your hand is:', sort_cards(hand))
                print('Please enter a play, separate multiple cards by a space. (3D 3S)')
                print('\n')
                play = input('Please enter a play: ')
                play = play.upper()
                if len(play) == 2:
                    try:
                        current_player.hand.remove(play)
                        play = [play.upper()]
                        played = True
                        return play
                    except ValueError:
                        print('That card is not in your hand!')
                elif 15 > len(play) > 3:
                    play = play.split()
                    if len(play) == 2:
                        try:
                            for x in play:
                                current_player.hand.remove(x)
                            played = True
                            return play
                        except ValueError:
                            print('That pair is not in your hand!')
                    if len(play) == 3:
                        try:
                            for x in play:
                                current_player.hand.remove(x)
                            played = True
                            return play
                        except ValueError:
                            print('That triple is not in your hand!')
                    if len(play) == 5:
                        try:
                            for x in play:
                                current_player.hand.remove(x)
                            played = True
                            return play
                        except ValueError:
                            print('That play is not in your hand.')
                elif len(play) == 0:
                    return []
                    played = True
                else:
                    print('That play is not valid.')
        else:
            current_play_type = identify_play(play_to_beat)
            if current_play_type == 'pair':
                possible_plays = all_pairs(hand)
            elif current_play_type == 'triple':
                possible_plays = all_threes(hand)
            elif current_play_type == 'single':
                possible_plays = sort_cards(hand)
            elif current_play_type == 'straight' or 'flush' or 'full house' or 'four of a kind' or 'straight flush':
                current_play_type = 'QUINTUPLE'
                possible_plays = all_fives(hand)
            print('It is your turn to play.')
            print('\n')
            print('The Current play to beat is:', play_to_beat)
            print('\n')
            print('YOU MUST PLAY:', current_play_type.upper())
            print('\n')
            print('POSSIBLE PLAYS:')
            print(possible_plays)
            print('\n')
            hand = sort_cards(hand)
            play = input('Please enter a play: ')
            play = play.upper()
            if len(play) == 2:
                if identify_play([play]) == current_play_type:
                    if is_higher(play, play_to_beat[0]):
                        try:
                            current_player.hand.remove(play)
                            play = [play.upper()]
                            played = True
                            return play
                        except ValueError:
                            print('That card is not in your hand!')
                    else:
                        print('That play does not beat the previous play.')
                else:
                    print('That does not match the current play type!')
            elif len(play) > 3:
                play = play.split()
                if len(play) == 2:
                    if identify_play(play) == current_play_type:
                        if is_higher_pair(play, play_to_beat):
                            try:
                                for x in play:
                                    current_player.hand.remove(x)
                                played = True
                                return play
                            except ValueError:
                                print('That pair is not in your hand!')
                        else:
                            print('That play does not beat the previous play!')
                    else:
                        print('That does not match the current play type!')
                elif len(play) == 3:
                    if identify_play(play) == current_play_type:
                        if is_higher_three(play, play_to_beat):
                            try:
                                for x in play:
                                    current_player.hand.remove(x)
                                played = True
                                return play
                            except ValueError:
                                print('That triple is not in your hand!')
                        else:
                            print('That play does not beat the previous play!')
                    else:
                        print('That does not match the current play type!')
                elif len(play) == 4:
                    print('That is not a valid play.')
                elif len(play) == 5:
                    if identify_play(
                            play) == 'straight' or 'flush' or 'full house' or 'four of a kind' or 'straight flush':
                        if is_higher_quintuple(play, play_to_beat):
                            try:
                                for x in play:
                                    current_player.hand.remove(x)
                                played = True
                                return play
                            except ValueError:
                                print('That play is not in your hand')
                        else:
                            print('That play does not beat the previous play!')
                    else:
                        print('That does not match the current play type!')
            elif len(play) == 0:
                return []
                played = True
            else:
                return []
                played = True


def sort_cards(cards):
    sorted_hand = sorted(cards, key=Card_Key)
    return sorted_hand


def Card_Key(card):
    rank_score = RANK_ORDER.index(card[0])
    suit_score = SUIT_ORDER.index(card[1])
    return rank_score, suit_score


def is_higher(card1, card2):
    if RANK_ARRAY.index(card1[0]) > RANK_ARRAY.index(card2[0]):
        return True
    elif RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(card2[0]):
        if SUIT_ARRAY.index(card1[1]) > SUIT_ARRAY.index(card2[1]):
            return True
        else:
            return False
    else:
        return False


def is_pair(card1, card2):
    if RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(card2[0]):
        return True
    else:
        return False


def low_card(cards, lastplay):
    for x in cards:
        if is_higher(x, lastplay[-1]):
            play = [x]
            return play


def all_pairs(hand):
    pairs_list = []
    for item in itertools.combinations(hand, 2):
        if is_pair(item[0], item[1]):
            pairs_list.append([item[0], item[1]])
    return pairs_list


def is_higher_pair(pair1, pair2):
    if RANK_ARRAY.index(pair1[1][0]) == RANK_ARRAY.index(pair2[1][0]):
        if SUIT_ARRAY.index(pair1[1][1]) > SUIT_ARRAY.index(pair2[1][1]) and SUIT_ARRAY.index(
                pair1[1][1]) > SUIT_ARRAY.index(pair2[0][1]):
            return True
        else:
            return False
    elif RANK_ARRAY.index(pair1[1][0]) > RANK_ARRAY.index(pair2[1][0]):
        return True
    else:
        return False


def low_pair(pairs, lastplay):
    for x in pairs:
        if is_higher_pair(x, lastplay):
            play = x
            return play


def is_three(card1, card2, card3):
    if RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(card2[0]) and RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(
            card3[0]):
        return True
    else:
        return False


def all_threes(hand):
    threes_list = []
    for item in itertools.combinations(hand, 3):
        # print(item)
        if is_three(item[0], item[1], item[2]):
            threes_list.append([item[0], item[1], item[2]])
    return threes_list


def is_higher_three(three1, three2):
    if RANK_ARRAY.index(three1[0][0][0]) == RANK_ARRAY.index(three2[0][0][0]):
        if SUIT_ARRAY.index(three1[2][1]) > SUIT_ARRAY.index(three2[2][1]):
            return True
    elif RANK_ARRAY.index(three1[0][0][0]) > RANK_ARRAY.index(three2[0][0][0]):
        return True
    else:
        return False


def low_three(threes, lastplay):
    for x in threes:
        if is_higher_three(x, lastplay):
            play = x
            return play


def is_a_full_house(cards):
    cards_list = sort_cards(cards)
    if is_pair(cards_list[0], cards_list[1]) and is_three(cards_list[2], cards_list[3], cards_list[4]):
        return True
    elif is_three(cards_list[0], cards_list[1], cards_list[2]) and is_pair(cards_list[3], cards_list[4]):
        return True
    else:
        return False


def all_full_houses(hand):
    house_list = []
    for item in itertools.combinations(hand, 5):
        # print(item)
        if is_a_full_house(item):
            house_list.append([item[0], item[1], item[2], item[3], item[4]])
    return house_list


def is_better_full_house(first, second):
    house1 = all_threes(first)
    house2 = all_threes(second)
    if is_higher_three(house1, house2):
        return True
    else:
        return False


def low_five(fives, lastplay):
    for x in fives:
        if is_better_full_house(x, lastplay):
            play = x
            return play


def is_straight(play):
    cards = sort_cards(play)
    i = 0
    for x in range(len(cards) - 1):
        if RANK_ARRAY.index(cards[x + 1][0]) == RANK_ARRAY.index(cards[x][0]) + 1:
            i = i + 1
    if i == 4:
        return True
    else:
        return False


def is_flush(cards):
    i = 0
    for x in range(len(cards)):
        if SUIT_ARRAY.index(cards[0][1]) == SUIT_ARRAY.index(cards[x][1]):
            i = i + 1
    if i == 5:
        return True
    else:
        return False


def all_straights(hand):
    straights_list = []
    for item in itertools.combinations(hand, 5):
        # print(item)
        if is_straight(item):
            straights_list.append([item[0], item[1], item[2], item[3], item[4]])
    return straights_list


def all_flush(hand):
    flush_list = []
    for item in itertools.combinations(hand, 5):
        # print(item)
        if is_flush(item):
            flush_list.append([item[0], item[1], item[2], item[3], item[4]])
    return flush_list


def all_straight_flush(hand):
    straight_flush_list = []
    for item in itertools.combinations(hand, 5):
        # print(item)
        if is_straight_flush(item):
            straight_flush_list.append([item[0], item[1], item[2], item[3], item[4]])
    return straight_flush_list


def is_four(card1, card2, card3, card4):
    if RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(card2[0]) and RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(
            card3[0]) and RANK_ARRAY.index(card1[0]) == RANK_ARRAY.index(card4[0]):
        return True
    else:
        return False


def is_four_kind(cards):
    card = sort_cards(cards)
    if is_four(card[0], card[1], card[2], card[3]):
        return True
    elif is_four(card[1], card[2], card[3], card[4]):
        return True
    else:
        return False


def is_straight_flush(cards):
    if is_straight(cards):
        if is_flush(cards):
            return True
        else:
            return False
    else:
        return False


def is_higher_quintuple(quint1, quint2):
    play_to_beat_type = identify_play(quint2)
    play_type = identify_play(quint1)

    play = sort_cards(quint1)
    play_to_beat = sort_cards(quint2)

    if POKER_ORDER.index(play_type) > POKER_ORDER.index(play_to_beat_type):
        return True
    elif POKER_ORDER.index(play_type) == POKER_ORDER.index(play_to_beat_type):
        if play_type == 'straight':
            if is_higher(play[-1], play_to_beat[-1]):
                return True
            else:
                return False
        elif play_type == 'flush':
            if is_higher(play[-1], play_to_beat[-1]):
                return True
            else:
                return False
        elif play_type == 'full house':
            if is_better_full_house(play, play_to_beat):
                return True
            else:
                return False
        elif play_type == 'straight flush':
            if is_higher(play[-1], play_to_beat[-1]):
                return True
            else:
                return False
        else:
            return False
    else:
        return False




def is_quintuple(cards):
    if is_straight(cards):
        return True
    elif is_flush(cards):
        return True
    elif is_a_full_house(cards):
        return True
    elif is_four_kind(cards):
        return True
    elif is_straight_flush(cards):
        return True
    else:
        return False


def identify_play(cards):
    cards = sort_cards(cards)
    if len(cards) == 2:
        return 'pair'
    if len(cards) == 1:
        return 'single'
    if len(cards) == 3:
        return 'triple'
    else:
        if is_straight(cards):
            if is_flush(cards):
                return 'straight flush'
            else:
                return 'straight'
        elif is_flush(cards):
            return 'flush'
        elif is_a_full_house(cards):
            return 'full house'
        elif is_four_kind(cards):
            return 'four of a kind'
        else:
            return 'invalid play'


def all_fives(hand):
    straights = all_straights(hand)
    flushs = all_flush(hand)
    full_houses = all_full_houses(hand)
    straight_flushs = all_straight_flush(hand)
    fives = []
    for x in straights:
        fives.append(x)
    for x in flushs:
        fives.append(x)
    for x in full_houses:
        fives.append(x)
    for x in straight_flushs:
        fives.append(x)
    return fives


def five_card_play(hand, play_to_beat):
    pairs_list = all_pairs(hand)
    threes_list = all_threes(hand)
    full_house_list = all_full_houses(hand)
    straights_list = all_straights(hand)
    flush_list = all_flush(hand)
    straight_flush_list = all_straight_flush(hand)

    five_list = [straights_list, flush_list, full_house_list, straight_flush_list]

    beat_type = identify_play(play_to_beat)
    lastplay = sort_cards(play_to_beat)

    print(five_list)


def play(current_player, hand, is_start_of_round, play_to_beat):
    hand = sort_cards(hand)
    pairs_list = all_pairs(hand)
    threes_list = all_threes(hand)
    full_house_list = all_full_houses(hand)
    straights_list = all_straights(hand)
    flush_list = all_flush(hand)
    quintuple_list = all_fives(hand)
    if len(play_to_beat) == 0:
        if is_start_of_round:
            for x in quintuple_list:
                if '3D' in x:
                    return x
            if len(pairs_list) > 0:
                if '3D' in pairs_list[0]:
                    return pairs_list[0]
            if len(threes_list) > 0:
                if '3D' in threes_list[0]:
                    return threes_list[0]
            else:
                play = [hand[0]]
                current_player.hand.remove(play[0])
                return play
        else:  # Start of Trick
            if len(hand) <= 2:  # If only two cards in hand at start of trick, play highest card.
                play = [hand[-1]]
                current_player.hand.remove(play[0])
                return play
            else:
                play = [hand[0]]
                current_player.hand.remove(play[0])
                return play
    elif len(play_to_beat) == 1:  # One Card Play.
        if is_higher(play_to_beat[0], hand[-1]):
            return []
        else:
            if len(hand) <= 2:
                play = [hand[-1]]
                current_player.hand.remove(play[0])
            else:
                play = low_card(hand, play_to_beat)
                current_player.hand.remove(play[0])
        return play
    elif len(play_to_beat) == 2:  # Two Card Play
        if len(pairs_list) == 0:
            return []
        elif is_higher_pair(sort_cards(play_to_beat), pairs_list[-1]):
            return []
        else:
            play = low_pair(pairs_list, sort_cards(play_to_beat))
            for x in play:
                current_player.hand.remove(x)
            return play
    elif len(play_to_beat) == 3:  # Three Card Play
        if len(threes_list) == 0:
            return []
        elif is_higher_three(sort_cards(play_to_beat), threes_list[-1]):
            return []
        else:
            play = low_three(threes_list, play_to_beat)
            for x in play:
                current_player.hand.remove(x)
            return play
    elif len(play_to_beat) == 5:
        for x in quintuple_list:
            if is_higher_quintuple(x, play_to_beat):
                for i in x:
                    current_player.hand.remove(i)
                return x
        return []
