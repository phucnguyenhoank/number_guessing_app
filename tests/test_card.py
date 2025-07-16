import pytest
from src.card import Card # Import the simplified Card class
# Unit tests for the Card class using pytest style
# No longer inherits from unittest.TestCase
def test_init():
    # Test initialization with valid value and suit
    card1 = Card('A', 'Spade')
    assert card1.value == 'A'
    assert card1.suit == 'Spade'

    # Test initialization with valid value and no suit (e.g., Joker)
    card2 = Card('Red Joker')
    assert card2.value == 'Red Joker'
    assert card2.suit is None

    # Test initialization with invalid value (should raise ValueError)
    with pytest.raises(ValueError):
        Card('InvalidValue', 'Spade')

    # Test initialization with invalid suit (should raise ValueError)
    with pytest.raises(ValueError):
        Card('A', 'InvalidSuit')

def test_lt():
    # Test less than comparison based on value
    card_2_spade = Card('2', 'Spade')
    card_3_spade = Card('3', 'Spade')
    assert card_2_spade < card_3_spade
    assert not (card_3_spade < card_2_spade)

    # Test less than comparison based on suit when values are equal
    card_A_club = Card('A', 'Club')
    card_A_diamond = Card('A', 'Diamond') # Diamond (3) > Club (2)
    assert card_A_club < card_A_diamond
    assert not (card_A_diamond < card_A_club)

    # Test less than comparison with Jokers (no suit)
    black_joker = Card('Black Joker')
    red_joker = Card('Red Joker')
    card_K = Card('K', 'Heart')

    assert card_K < black_joker # K (13) < Black Joker (14)
    assert not (black_joker < card_K)
    assert black_joker < red_joker # Black Joker (14) < Red Joker (15)

    # Test edge case: same card
    assert not (card_2_spade < card_2_spade)

def test_gt():
    # Test greater than comparison based on value
    card_K_heart = Card('K', 'Heart')
    card_Q_heart = Card('Q', 'Heart')
    assert card_K_heart > card_Q_heart
    assert not (card_Q_heart > card_K_heart)

    # Test greater than comparison based on suit when values are equal
    card_10_heart = Card('10', 'Heart')
    card_10_spade = Card('10', 'Spade') # Heart (4) > Spade (1)
    assert card_10_heart > card_10_spade
    assert not (card_10_spade > card_10_heart)

    # Test greater than comparison with Jokers (no suit)
    red_joker = Card('Red Joker')
    black_joker = Card('Black Joker')
    card_K = Card('K', 'Heart')

    assert red_joker > black_joker # Red Joker (15) > Black Joker (14)
    assert not (black_joker > red_joker)
    assert black_joker > card_K # Black Joker (14) > K (13)

    # Test edge case: same card
    assert not (card_K_heart > card_K_heart)

def test_eq():
    # Test equality for identical cards
    card_A_spade1 = Card('A', 'Spade')
    card_A_spade2 = Card('A', 'Spade')
    assert card_A_spade1 == card_A_spade2

    # Test inequality for different values
    card_2_spade = Card('2', 'Spade')
    assert not (card_A_spade1 == card_2_spade)

    # Test inequality for different suits
    card_A_heart = Card('A', 'Heart')
    assert not (card_A_spade1 == card_A_heart)

    # Test equality for Jokers (no suit)
    black_joker1 = Card('Black Joker')
    black_joker2 = Card('Black Joker')
    red_joker = Card('Red Joker')
    assert black_joker1 == black_joker2
    assert not (black_joker1 == red_joker)

    # Test inequality between card with suit and card without suit
    assert not (card_A_spade1 == black_joker1)

def test_repr():
    # Test representation with suit
    card1 = Card('A', 'Spade')
    assert repr(card1) == "A of Spade"

    # Test representation without suit (Joker)
    card2 = Card('Black Joker')
    assert repr(card2) == "Black Joker"

    card3 = Card('10', 'Club')
    assert repr(card3) == "10 of Club"
    