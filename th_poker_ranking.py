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


def get_card_score(ordered_cards):
    # Gives a minor score which is used to rank hand with kickers etc. correctly.
    # Inputs are the number values of card sorted from least important card to the hand
    # to the most important. Usually largest card is the most important, but pairs for
    # example are an exception.
    
    score = 0
    for i, card_value in enumerate(ordered_cards):
        weight = (max_value+1)**1  # ensures that a_1*weight_1 < a_2*weight_2 for any values of a_i
        score += card_value*weight
    return score


def is_pairs(hand):
    hand_numbers = [card_values[r] for r, s in hand]

    counter = [0]*(max_value+1)
    for v in hand_numbers:
        counter[v] += 1
        
    # Sort primary by card count and secondary by card size
    counts_by_importance = sorted([(v, counter[v]*max_value + v) for v in hand_numbers], key=lambda x: x[1])
    score = get_card_score([i[0] for i in counts_by_importance[:len(hand)]])

    # 4 of a kind: 4 cards of the same number
    if 4 in counter:
        return score + 70000

    # Full House: 3 of a Kind and 2 of a Kind
    if 3 in counter and 2 in counter:
        return score + 60000

    # 3 of a Kind: 3 cards of the same number
    if 3 in counter:
        return score + 30000

    # 2 Pairs: 2 Pairs of 2 of a kind (One Pair): 2 cards of the same number
    if counter.count(2) == 2:
        return score + 20000

    # 2 of a Kind (One Pair): 2 cards of the same number
    if 2 in counter:
        return score + 10000

    return score


def is_high_card(current_hand):
    ordered_cards = sorted([card_values[r] for r, s in current_hand])
    score = get_card_score(ordered_cards)
    return score


def is_flush(hand):
    # find all suits in hand and count to see if there are 5 or greater
    # find all suit values in hand and return a list of all cards containing that suit (5, 6, or 7 possible cards)
    suits = [s for r, s in hand]

    for i in set(suits):
        if suits.count(i) >= 5:
            score = is_high_card(hand)
            return score + 50000
        
    return 0


def is_straight(hand):
    hand_numbers = [card_values[r] for r, s in hand]
    num_list = sorted(set(hand_numbers))
    straight_hand_cards =[]

    # can only be len(num_list) from 7 to 5 - straight has to be 5 cards in a row
    # will account for multiple straights (2,3,4,5,6,7,8), then the whole list will be returned
    # will return duplicate card values for the straight (to help match if straight/flush)
    # counts Ace as 14 so does not count A, 2, 3, 4, 5 as a straight (using Ace Low Rule)
    if len(num_list) >= 5:
        for i in range(len(num_list) - 4):
            temp = num_list[i:i+5]
            if (temp[4] - temp[0]) == 4:
                # have to account for multiple straights in a given set of 7, unable to return value at this point
                straight_hand_cards += [j for j in hand if card_values[j[0]] in temp]

    straight_hand_cards = sorted(set(straight_hand_cards))

    if len(straight_hand_cards) >= 5:
        score = max(hand_numbers)   # Max card determines how good the straight is
        print(hand, score)
        return score + 40000
    return 0


def is_straight_flush(flush, straight):
    if ((flush > 0) and (straight > 0)):
        return straight + 80000
    return 0


def ranker(hand):
    hand = hand.split()
    
    high_card_suit = is_high_card(hand)
    pairs = is_pairs(hand)
    straight = is_straight(hand)
    flush = is_flush(hand)
    straight_flush = is_straight_flush(flush, straight)
    
    score = max(straight_flush, flush, straight, pairs, high_card_suit)

    return score
