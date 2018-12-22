import th_poker_ranking


def test_two_cards():
    pair = th_poker_ranking.ranker('2C 2C')
    ace_high = th_poker_ranking.ranker('AC 3C')
    assert pair > ace_high
    
    king_high = th_poker_ranking.ranker('KC 3C')
    assert ace_high > king_high
    
    
def test_high_card_kicker():
    ace_high_kicker_2card = th_poker_ranking.ranker('AC 4C')
    ace_high_2card = th_poker_ranking.ranker('AS 3C')
    assert ace_high_kicker_2card > ace_high_2card
    
    ace_high_kicker = th_poker_ranking.ranker('AC KC 2S 8H 4D')
    ace_high = th_poker_ranking.ranker('AC 3C 2S 8H 4D')
    assert ace_high_kicker > ace_high
    
    ace_high_kicker = th_poker_ranking.ranker('AC KC 2S 8H 4D')
    ace_high_average_high = th_poker_ranking.ranker('AC QC JS TH 8D')
    assert ace_high_kicker > ace_high_average_high

    
def test_pairs_kicker():
    pair_kicker = th_poker_ranking.ranker('2S 2H 4D 5C AC')
    pair = th_poker_ranking.ranker('2S 2H 4D 5C KC')
    assert pair_kicker > pair
    
    
def test_wheel():
    two_sight_straight = th_poker_ranking.ranker('2S 3H 4D 5C 6C')
    wheel = th_poker_ranking.ranker('AS 2H 3D 4C 5C')
    assert two_sight_straight > wheel
    
    three_of_kind = th_poker_ranking.ranker('2S 2H 2D 5C AC')
    assert wheel > three_of_kind
    
def test_hand_types():    
    straight_flush = th_poker_ranking.ranker('2C 3C 4C 5C 6C')
    
    four_of_kind  = th_poker_ranking.ranker('2S 2H 2D 2C AC')
    assert straight_flush > four_of_kind

    full_house = th_poker_ranking.ranker('2S 2H 2D 3C 3C')
    assert four_of_kind > full_house

    flush = th_poker_ranking.ranker('2C 3C AC TC 6C')
    assert full_house > flush
    
    straight = th_poker_ranking.ranker('2S 3H 4D 5C 6C')
    assert flush > straight

    three_of_kind = th_poker_ranking.ranker('2S 2H 2D 5C AC')
    assert straight > three_of_kind

    two_pair = th_poker_ranking.ranker('2S 2H 4D 4C AC')
    assert three_of_kind > two_pair

    pair = th_poker_ranking.ranker('2S 2H 4D 5C AC')
    assert two_pair > pair

    ace_high = th_poker_ranking.ranker('2S 3H 4D 7C AC')
    assert pair > ace_high

    seven_high = th_poker_ranking.ranker('2S 3H 4D 6C 7C')
    assert ace_high > seven_high
    
    
def test_canadian_types():    
    straight_flush = th_poker_ranking.ranker('2C 3C 4C 5C 6C', canadian=True)
    
    four_of_kind  = th_poker_ranking.ranker('2S 2H 2D 2C AC', canadian=True)
    assert straight_flush > four_of_kind

    full_house = th_poker_ranking.ranker('2S 2H 2D 3C 3C', canadian=True)
    assert four_of_kind > full_house

    flush = th_poker_ranking.ranker('2C 3C AC TC 6C', canadian=True)
    assert full_house > flush
    
    straight = th_poker_ranking.ranker('2S 3H 4D 5C 6C', canadian=True)
    assert flush > straight

    three_of_kind = th_poker_ranking.ranker('2S 2H 2D 5C AC', canadian=True)
    assert straight > three_of_kind

    two_pair = th_poker_ranking.ranker('2S 2H 4D 4C AC', canadian=True)
    assert three_of_kind > two_pair

    canadian_flush = th_poker_ranking.ranker('2S 3S 5S 7S AC', canadian=True)
    assert three_of_kind > canadian_flush

    canadian_flush_and_pair = th_poker_ranking.ranker('2S 3S 5S 7S 7C', canadian=True)
    assert canadian_flush > canadian_flush_and_pair

    canadian_straight = th_poker_ranking.ranker('3H 4D 5C 6S AC', canadian=True)
    assert canadian_flush_and_pair > canadian_straight

    canadian_straight_and_pair = th_poker_ranking.ranker('3H 4D 5C 6S 6C', canadian=True)
    assert canadian_straight > canadian_straight_and_pair
    
    pair = th_poker_ranking.ranker('2S 2H 4D 5C AC', canadian=True)
    assert canadian_straight_and_pair > pair

    ace_high = th_poker_ranking.ranker('2S 3H 5D 7C AC', canadian=True)
    assert pair > ace_high

    seven_high = th_poker_ranking.ranker('2S 3H 4D 6C 7C', canadian=True)
    assert ace_high > seven_high
    
    
def test_straight_flushes():
    straight_flush_7 = th_poker_ranking.ranker('7C 3C 4C 5C 6C')
    straight_flush_6 = th_poker_ranking.ranker('2C 3C 4C 5C 6C')
    assert straight_flush_7 > straight_flush_6

