#
# Texas Holdem Poker Ranking System
#    by Joseph A Young
#
# rules taken from World Series of Poker: http://www.wsop.com/poker-games/texas-holdem/rules/
#
# winner is the one with the best five card hand made out of the possible 5, 6, or 7 cards:
#    set ranking:    Royal Flush, Straight Flush, Four of a Kind, Full House, Flush, Straight,
#                    Three of a Kind, Two Pairs, One Pair, High Card
#    number ranking: A, K, Q, J, 10, 9, 8, 7, 6, 5 ,4 ,3, 2
#
# statistics:
#    max score: 9144
#    average score after 1,000,000 trials was 1626.356483
#    test results show a normal distribution with a high center peak
#    over 133,784,560 hands for 7 hand poker (52 C 7)
#
# Notes:
# too many loops and repeated calculations
#

import random
import math

import matplotlib.pyplot as plt

card_values = dict((r, i) for i, r in enumerate('..23456789TJQKA'))
max_value = max(card_values.values())
hand_value = {
    "straight_flush": 12,
    "4 of kind": 11,
    "full house": 10,
    "flush": 9,
    "straight": 8,
    "wheel": 7,
    "3 of kind": 6,
    "two pair": 5,
    "canadian flush": 4,
    "canadian straight": 3,
    "canadian wheel": 2,
    "2 of kind": 1,
    }
hand_value_multiplier = 10**7

def get_kicker_score(counter, hand_numbers):
    # Gives a minor score which is used to rank hand with kickers etc. correctly.
    # Inputs are the number values of card sorted from least important card to the hand
    # to the most important. Usually largest card is the most important, but pairs for
    # example are an exception. Max value 759374 for 5 aces.
    
    counts_by_importance = sorted([(v, counter[v]*max_value + v) for v in hand_numbers], key=lambda x: x[1])
    ordered_cards = [i[0] for i in counts_by_importance[:len(hand_numbers)]]
    
    score = 0
    for i, card_value in enumerate(ordered_cards):
        weight = (max_value+1)**i  # ensures that a_1*weight_1 < a_2*weight_2 for any values of a_i
        score += card_value*weight
    return score
   

def is_pairs(counter):
    # 4 of a kind: 4 cards of the same number
    if 4 in counter:
        return hand_value['4 of kind']

    # Full House: 3 of a Kind and 2 of a Kind
    if 3 in counter and 2 in counter:
        return hand_value['full house']

    # 3 of a Kind: 3 cards of the same number
    if 3 in counter:
        return hand_value['3 of kind']

    # 2 Pairs: 2 Pairs of 2 of a kind (One Pair): 2 cards of the same number
    if counter.count(2) == 2:
        return hand_value['two pair']

    # 2 of a Kind (One Pair): 2 cards of the same number
    if 2 in counter:
        return hand_value['2 of kind']

    return 0


def is_flush(hand, length=5, prefix=''):
    # find all suits in hand and count to see if there are 5 or greater
    # find all suit values in hand and return a list of all cards containing that suit (5, 6, or 7 possible cards)
    suits = [s for r, s in hand]

    for i in suits:
        if suits.count(i) >= length:
            return hand_value['{}flush'.format(prefix)]
        
    return 0


def is_straight(hand_numbers, length=5, prefix=''):
    sorted_hand = sorted(set(hand_numbers))
    
    # Wheel: Ace to 5 straight. Highest card is 5
    flag = True
    for v in range(2,length+1):
        if v not in sorted_hand:
            flag = False
            break
    if flag and 14 in sorted_hand:
        return hand_value['{}wheel'.format(prefix)]

    for end_ind in range(len(sorted_hand),length-1,-1):
        if sorted_hand[end_ind-1]-sorted_hand[end_ind-length] == length-1:
            return hand_value['{}straight'.format(prefix)]
        
    return 0


def is_straight_flush(flush, straight):
    if ((flush > 0) and (straight > 0)):
        return flush+straight  # takes care of the wheel too by giving lower rank to A-5 straight flush.
    return 0


def ranker(string_input, canadian=False):
    temp_hand = string_input.split()
    hand = [(card_values[r], s) for r, s in temp_hand]
    return rank_array(hand, canadian=canadian)
    
def rank_array(hand, canadian=False):
    hand_numbers = [v for v, s in hand]
    
    counter = [0]*(max_value+1)
    for v in hand_numbers:
        counter[v] += 1
        
    kicker_score = get_kicker_score(counter, hand_numbers)
    
    pairs = is_pairs(counter)
    if pairs == 0:
        straight = is_straight(hand_numbers)
        flush = is_flush(hand)
    else:
        straight, flush = 0, 0
    straight_flush = is_straight_flush(flush, straight)
    
    hand_values = [straight_flush, flush, straight, pairs]
    if canadian:
        hand_values.append(is_flush(hand, length=4, prefix='canadian '))
        hand_values.append(is_straight(hand, length=4, prefix='canadian '))
    
    score = max(hand_values)*hand_value_multiplier + kicker_score

    return score

