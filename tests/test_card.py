import pytest
from src.card import Card # Import the simplified Card class

# --- Test Card Creation ---

def test_card_creation_valid():
    """Test valid card creations and their initial state."""
    card_ace_spade = Card('A', 'Spade')
    assert card_ace_spade.value == 'A'
    assert card_ace_spade.suit == 'Spade'
    assert repr(card_ace_spade) == 'A of Spade'

    card_ten_diamond = Card('10', 'Diamond')
    assert card_ten_diamond.value == '10'
    assert card_ten_diamond.suit == 'Diamond'
    assert repr(card_ten_diamond) == '10 of Diamond'

    card_black_joker = Card('Black Joker', None)
    assert card_black_joker.value == 'Black Joker'
    assert card_black_joker.suit is None
    assert repr(card_black_joker) == 'Black Joker'

    card_red_joker = Card('Red Joker', None)
    assert card_red_joker.value == 'Red Joker'
    assert card_red_joker.suit is None
    assert repr(card_red_joker) == 'Red Joker'

def test_card_creation_invalid_value():
    """Test creation with an invalid card value, expecting a ValueError."""
    with pytest.raises(ValueError, match="Invalid card value: 'InvalidValue'"):
        Card('InvalidValue', 'Heart')
    with pytest.raises(ValueError, match="Invalid card value: '1'"):
        Card('1', 'Spade') # '1' is not a valid value, 'A' is 1

def test_card_creation_invalid_suit():
    """Test creation with an invalid suit for a non-joker card, expecting a ValueError."""
    with pytest.raises(ValueError, match="Invalid suit: 'Stars' for value 'K'"):
        Card('K', 'Stars')

def test_card_creation_joker_with_suit():
    """Test creation of a Joker with a suit (which should be invalid), expecting a ValueError."""
    with pytest.raises(ValueError, match="Jokers cannot have a suit."):
        Card('Black Joker', 'Heart')
    with pytest.raises(ValueError, match="Jokers cannot have a suit."):
        Card('Red Joker', 'Diamond')

# --- Test Immutability ---

def test_card_immutability():
    """Test that card attributes cannot be modified after creation."""
    card = Card('Q', 'Club')

    # Attempt to modify value - this should raise an AttributeError
    with pytest.raises(AttributeError, match="can't set attribute"):
        card.value = 'K'

    # Attempt to modify suit - this should raise an AttributeError
    with pytest.raises(AttributeError, match="can't set attribute"):
        card.suit = 'Spade'

    # Verify attributes remain unchanged after failed modification attempts
    assert card.value == 'Q'
    assert card.suit == 'Club'

# --- Test Card Comparisons (__eq__, __lt__, __gt__, __ne__) ---

def test_card_equality():
    """Test equality (==) between cards."""
    assert Card('7', 'Heart') == Card('7', 'Heart')
    assert Card('A', 'Spade') == Card('A', 'Spade')
    assert Card('Black Joker', None) == Card('Black Joker', None)
    assert Card('Red Joker', None) == Card('Red Joker', None)
    assert not (Card('7', 'Heart') == Card('8', 'Heart')) # Different value
    assert not (Card('7', 'Heart') == Card('7', 'Diamond')) # Different suit

def test_card_inequality():
    """Test inequality (!=) between cards."""
    assert Card('7', 'Heart') != Card('8', 'Heart')
    assert Card('7', 'Heart') != Card('7', 'Diamond')
    assert Card('Red Joker', None) != Card('Black Joker', None)
    assert not (Card('7', 'Heart') != Card('7', 'Heart')) # Should be False

def test_card_less_than():
    """Test less than (<) comparisons."""
    # Value comparison (suit is same)
    assert Card('7', 'Heart') < Card('8', 'Heart')
    assert Card('A', 'Spade') < Card('K', 'Spade') # K=13, A=1 (based on your VALUE_ORDER)
    assert Card('10', 'Club') < Card('J', 'Club')

    # Suit comparison (value is same) - based on SUIT_ORDER: Spade < Club < Diamond < Heart
    assert Card('A', 'Spade') < Card('A', 'Club')
    assert Card('A', 'Club') < Card('A', 'Diamond')
    assert Card('A', 'Diamond') < Card('A', 'Heart')

    # Joker vs non-Joker
    assert Card('K', 'Heart') < Card('Black Joker', None) # K=13, Black Joker=14
    assert Card('Black Joker', None) < Card('Red Joker', None) # Black Joker=14, Red Joker=15

def test_card_greater_than():
    """Test greater than (>) comparisons."""
    # Value comparison (suit is same)
    assert Card('8', 'Heart') > Card('7', 'Heart')
    assert Card('K', 'Spade') > Card('A', 'Spade') # A=1, K=13 (based on your VALUE_ORDER)
    assert Card('J', 'Club') > Card('10', 'Club')

    # Suit comparison (value is same)
    assert Card('A', 'Club') > Card('A', 'Spade')
    assert Card('A', 'Diamond') > Card('A', 'Club')
    assert Card('A', 'Heart') > Card('A', 'Diamond')

    # Joker vs non-Joker
    assert Card('Black Joker', None) > Card('K', 'Heart')
    assert Card('Red Joker', None) > Card('Black Joker', None)

def test_card_less_than_or_equal():
    """Test less than or equal (<=) comparisons."""
    assert Card('7', 'Heart') <= Card('7', 'Heart') # Equal
    assert Card('7', 'Heart') <= Card('8', 'Heart') # Less than
    assert Card('A', 'Spade') <= Card('A', 'Club') # Less than by suit

def test_card_greater_than_or_equal():
    """Test greater than or equal (>=) comparisons."""
    assert Card('7', 'Heart') >= Card('7', 'Heart') # Equal
    assert Card('8', 'Heart') >= Card('7', 'Heart') # Greater than
    assert Card('A', 'Club') >= Card('A', 'Spade') # Greater than by suit

def test_card_rank_method():
    """Test the internal _rank method for correct tuple generation."""
    assert Card('A', 'Spade')._rank() == (1, 1)
    assert Card('K', 'Heart')._rank() == (13, 4)
    assert Card('Black Joker', None)._rank() == (14, 0)
    assert Card('Red Joker', None)._rank() == (15, 0)
    assert Card('7', 'Diamond')._rank() == (7, 3)

def test_comparison_with_non_card_objects():
    """Test comparisons with objects that are not instances of Card."""
    card = Card('A', 'Spade')

    # For equality (==), comparing with an incompatible type typically results in False, not TypeError.
    assert not (card == 123)
    assert card != "not a card" # Also asserts inequality

    # For ordering comparisons (<, >, <=, >=), if both sides return NotImplemented, Python raises TypeError.
    with pytest.raises(TypeError):
        card < "not a card"
    with pytest.raises(TypeError):
        "not a card" < card # Test reverse comparison as well
    with pytest.raises(TypeError):
        card > 123
    with pytest.raises(TypeError):
        123 > card

    with pytest.raises(TypeError):
        card <= "not a card"
    with pytest.raises(TypeError):
        "not a card" <= card # Test reverse comparison as well
    with pytest.raises(TypeError):
        card >= 123
    with pytest.raises(TypeError):
        123 >= card
