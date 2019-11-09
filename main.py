import itertools
import random
from play import *

RANK_ORDER = '34567890JQKA2'
SUIT_ORDER = 'DCHS'
POKER_ORDER = ['straight', 'flush', 'full house', 'four of a kind', 'straight flush']
RANK_ARRAY = list(RANK_ORDER)
SUIT_ARRAY = list(SUIT_ORDER)


def createArray(RANK_ORDER, SUIT_ORDER):
    CARD_ARRAY = []
    for rank in RANK_ORDER:
        for suit in SUIT_ORDER:
            combination = [rank, suit]
            card = ''.join(combination)
            CARD_ARRAY.append(card)
    return CARD_ARRAY


def dealCards(DECK, PLAYERS):
    for player in PLAYERS:
        i = 1
        hand = player.hand
        while i <= 13:
            card = DECK[0]

            hand.append(card)
            DECK.remove(card)
            i = i + 1
        sorted_hand = sort_cards(hand)
    return sorted_hand


def find3d(PLAYERS):
    for player in PLAYERS:
        if '3D' in player.hand:
            return player


def nextPlayer(player):
    if player == player4:
        next_player = player1
    elif player == player1:
        next_player = player2
    elif player == player2:
        next_player = player3
    elif player == player3:
        next_player = player4
    return next_player

def checkWinner(PLAYERS):
    if len(player1.hand) == 0:
        return True
    elif len(player2.hand) == 0:
        return True
    elif len(player3.hand) == 0:
        return True
    elif len(player4.hand) == 0:
        return True
    else:
        return False


class player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.lastplay = []

    def __str__(self):
        return self.name


# CREATE DECK
CARD_ARRAY = createArray(RANK_ORDER, SUIT_ORDER)
DECK = CARD_ARRAY.copy()

# SORT DECK
random.shuffle(DECK)

# CREATE EACH PLAYER
player1 = player('Player 1')
player2 = player('Player 2')
player3 = player('Player 3')
player4 = player('Player 4')

PLAYERS = [player1, player2, player3, player4]
players = ['Player 1', 'Player 2', 'Player 3', 'Player 4']

# DEAL CARDS TO EACH PLAYER
dealCards(DECK, PLAYERS)

print('Player 1 was dealt:', sort_cards(player1.hand))
print('Player 2 was dealt:', sort_cards(player2.hand))
print('Player 3 was dealt:', sort_cards(player3.hand))
print('Player 4 was dealt:', sort_cards(player4.hand))
print('\n')
print(find3d(PLAYERS), 'has the 3 of Diamonds and goes first.')

# FIRST TURN

# SET PLAYER WITH THE 3 OF DIAMONDS TO ACTIVE PLAYER
current_player = find3d(PLAYERS)
play_to_beat = []

if current_player == player1:
    current_play = playerTurn(current_player, current_player.hand, play_to_beat, True)
else:
    current_play = play(current_player, current_player.hand, True, play_to_beat)
    print(current_player, 'played', current_play)

hand = current_player.hand
play_to_beat = []
play_to_beat = current_play

current_player = nextPlayer(current_player)

pass_count = 0
winner = False

while not winner:

    is_start_of_round = False

    if pass_count == 3:
        play_to_beat = []
        print('\n')
        print('Everybody passed, a new trick is started.')
        print('\n')
        pass_count = 0
    else:
        play_to_beat = current_play

    if current_player == player1:
        current_play = playerTurn(current_player, current_player.hand, play_to_beat, is_start_of_round)
        current_player.lastplay = [current_play]
    else:
        current_play = play(current_player, current_player.hand, is_start_of_round, play_to_beat)
        current_player.lastplay = current_play

    if current_play == []:
        print(current_player, 'played a pass.')
        current_player = nextPlayer(current_player)
        current_play = play_to_beat
        pass_count = pass_count + 1
    else:
        print(current_player, 'played', current_play)
        pass_count = 0
        hand = current_player.hand
        play_to_beat = current_play  # update play_to_beat
        previous_player = current_player
        current_player = nextPlayer(current_player)  # update the current player to next in list
        winner = checkWinner(PLAYERS)
        # hand.remove(current_play) # remove played card from player's hand.

print('\n')
print(previous_player, 'has won the game!')
print('\n')

input('Press enter to continue...')
