from deuces import *
from th_poker_ranking import rank_array
import itertools
from copy import deepcopy
from joblib import Parallel, delayed
import numpy as np
import os


DATA_FOLDER = 'data'

C = Card()
E = Evaluator()
def rank_deuces_hand(hand):
    # Add two to the numbers since deuces does numbering for 0-12 and not 2-14. Wheel is not correct.
    return rank_array([(C.get_rank_int(card)+2, C.get_suit_int(card)) for card in hand], canadian=True)

def run_simulation(hands):
    MC_hands = deepcopy(hands)
    deck = Deck()
    for hand in hands:
        for card in hand:
            deck.remove(card)
        MC_hands = deepcopy(hands)

    for hand in MC_hands:
        while len(hand) < 5:
            hand.append(deck.draw())

    scores = [rank_deuces_hand(hand) for hand in MC_hands]
    best_score = max(scores)
    if scores[0] == best_score:
        return 1 / scores.count(best_score)
    return 0

def hand_string(hand):
    return " ".join([C.int_to_pretty_str(card) for card in hand])


def main():
    filename = input("Who are you (output filename)? ")
    
    N = 10000
    all_errors = []
    
    while True:
        print("New game")
        hands = [[], []]
        deck = Deck()
        
        errors = []
        equities = []
        estimates = []
        for i in range(5):
            hands[0].append(deck.draw())
            hands[1].append(deck.draw())
            for i, hand in enumerate(hands):
                print("Player {}: {}".format(i+1, hand_string(hand)))

            # wins = sum([run_simulation(hands) for i in range(N)])
            wins = sum(Parallel(-1)(delayed(run_simulation)(hands) for i in range(N)))

            equity = int(wins/N*100)
            while True:
                try:
                    inp = input("Estimate Player 1 equity (exit with q)")
                    if inp == 'q':
                        try:
                            mae = sum(np.abs(all_errors))/len(all_errors)
                            print("Average error in {} guesses was {}".format(len(all_errors), mae))
                        except:
                            1
                        print("Bye")
                        return

                    estimate = int(inp)
                    break
                except:
                    print("Error. Try again.")

            error = estimate-equity
            estimates.append(str(estimate))
            equities.append(str(equity))
            errors.append(str(error))
            all_errors.append(error)
            print("Player 1 equity: {}. Error: {}".format(equity, error))

        with open(os.path.join(DATA_FOLDER,"{}.csv".format(filename)),"a+") as f:
            f.write(",".join(errors + estimates + equities) + "\n")
        

if __name__ == '__main__':
    main()
