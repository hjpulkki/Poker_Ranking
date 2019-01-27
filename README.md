# Monte Carlo simulator for Sökö (Canadian stud)

The goal of this repository is to understand poker variant Sökö (sometimes also called Canadian stud). Rules can be found from here https://www.denexa.com/blog/soko-canadian-stud/.

I based my work on mostly on https://github.com/joeyoung33333/Poker_Ranking/blob/master/th_poker_ranking.py, which is a simple approach to poker hand evaluation. I have made some improvements to the code, added some testing and most importantly added option to include 4-card straight and flush. To keep the code simple I had to remove 6- and 7-card hand evaluation, which is only necessary for Texas Hold'em.

Deuces library (https://github.com/worldveil/deuces) was also used for testing and to deal random cards.
