import pytest
import random
from src.card import Card
from src.deck import Deck, StandardDeckFactory, JokerDeckFactory

# --- Test Deck Class Functionality ---

def test_deck_initialization_and_count():
    """Test that a deck is initialized with the correct number of cards."""
    # Create some dummy cards for testing the Deck class directly
    cards = [Card('A', 'Spade'), Card('K', 'Heart')]
    deck = Deck(cards)
    assert deck.cards_left() == 2

    # Ensure the deck makes a copy of the list, not just a reference
    original_cards_list = [Card('A', 'Club')]
    deck_from_list = Deck(original_cards_list)
    assert deck_from_list.cards_left() == 1
    original_cards_list.append(Card('J', 'Diamond')) # Modify original list
    assert deck_from_list.cards_left() == 1 # Deck's internal state should be unaffected

def test_deck_shuffle():
    """Test that shuffling changes the order of cards."""
    # Create a predictable deck for testing shuffle
    cards = [Card(str(i), 'Spade') for i in range(1, 14)] # 13 cards
    deck = Deck(list(cards)) # Pass a copy to Deck's constructor
    
    # Capture initial state (before any random draws)
    initial_full_deck_cards = list(deck._cards) 
    
    # Create a new deck instance for comparison to ensure a fresh, unshuffled state
    unshuffled_deck_for_comparison = Deck(list(cards))
    
    # Deal all cards from the initially shuffled deck (order is random)
    order_after_initial_shuffle = []
    temp_deck_for_initial_draw = Deck(list(initial_full_deck_cards)) # Use the initially shuffled list
    for _ in range(temp_deck_for_initial_draw.cards_left()):
        order_after_initial_shuffle.append(temp_deck_for_initial_draw.draw_card(replace=False))

    # Shuffle the original deck again
    deck.shuffle()
    
    # Deal all cards from the re-shuffled deck
    order_after_reshuffle = []
    for _ in range(deck.cards_left()):
        order_after_reshuffle.append(deck.draw_card(replace=False))
    
    # It's highly improbable for two random shuffles to be in the exact same order
    assert order_after_initial_shuffle != order_after_reshuffle
    assert len(order_after_initial_shuffle) == len(order_after_reshuffle) # Ensure no cards were lost

def test_deck_draw_card_no_replacement():
    """
    Test drawing cards without replacement (default behavior) and deck count reduction.
    This simulates the "deal_card" behavior.
    """
    cards = [Card('A', 'Spade'), Card('K', 'Heart'), Card('Q', 'Diamond')]
    deck = Deck(list(cards)) # Use a copy
    initial_count = deck.cards_left() # Should be 3
    
    drawn_cards = []

    # Draw all cards without replacement
    for i in range(initial_count):
        dealt_card = deck.draw_card(replace=False) # Explicitly test no replacement
        assert deck.cards_left() == initial_count - (i + 1)
        assert isinstance(dealt_card, Card)
        assert dealt_card in cards # Ensure the drawn card is one of the original cards
        assert dealt_card not in drawn_cards # Ensure it's a unique card (no replacement)
        drawn_cards.append(dealt_card)

    # After drawing all cards, the deck should be empty
    assert deck.cards_left() == 0
    assert set(drawn_cards) == set(cards) # Ensure all original cards were drawn exactly once

    # Test drawing from an empty deck (no replacement)
    with pytest.raises(IndexError, match="Cannot draw card from an empty deck"):
        deck.draw_card(replace=False)

def test_deck_draw_card_with_replacement():
    """Test drawing cards with replacement; deck count should not change."""
    cards = [Card('A', 'Spade'), Card('K', 'Heart')]
    deck = Deck(list(cards))
    initial_count = deck.cards_left() # Should be 2

    drawn_card_list = []
    # Draw multiple cards with replacement
    for _ in range(10): # Draw more than initial count to emphasize replacement
        drawn_card = deck.draw_card(replace=True)
        assert deck.cards_left() == initial_count # Count should not change
        assert isinstance(drawn_card, Card)
        assert drawn_card in cards # Ensure it's a valid card
        drawn_card_list.append(drawn_card)
    
    # Verify that cards were indeed drawn (not just an empty loop)
    assert len(drawn_card_list) == 10
    # It's possible to draw the same card multiple times with replacement
    # No assertion on uniqueness of drawn_card_list elements.

def test_deck_dealt_card_immutability():
    """Test that cards drawn from the deck are immutable."""
    deck = StandardDeckFactory().create_deck()
    dealt_card = deck.draw_card(replace=False) # Draw one card

    with pytest.raises(AttributeError, match="can't set attribute"):
        dealt_card.value = "New Value"
    with pytest.raises(AttributeError, match="can't set attribute"):
        dealt_card.suit = "New Suit"

# --- Test StandardDeckFactory ---

def test_standard_deck_factory_creates_52_cards():
    """Test that StandardDeckFactory creates a deck with 52 cards."""
    factory = StandardDeckFactory()
    deck = factory.create_deck()
    assert deck.cards_left() == 52

def test_standard_deck_factory_no_jokers():
    """Test that a standard deck does not contain Jokers."""
    factory = StandardDeckFactory()
    deck = factory.create_deck()
    
    # Deal all cards and check for Jokers
    has_jokers = False
    for _ in range(52): # Iterate 52 times to deal all cards
        card = deck.draw_card(replace=False)
        if card.value in ['Black Joker', 'Red Joker']:
            has_jokers = True
            break
    assert not has_jokers, "Standard deck should not contain Jokers."
    assert deck.cards_left() == 0 # Ensure all cards were dealt

def test_standard_deck_factory_unique_cards():
    """Test that all cards in a standard deck are unique."""
    factory = StandardDeckFactory()
    deck = factory.create_deck()
    
    cards_in_deck = []
    for _ in range(deck.cards_left()): # Deal all cards
        cards_in_deck.append(deck.draw_card(replace=False))
    
    unique_cards = set(cards_in_deck)
    assert len(unique_cards) == 52, "Standard deck should have 52 unique cards."
    assert deck.cards_left() == 0 # Ensure all cards were dealt

# --- Test JokerDeckFactory ---

def test_joker_deck_factory_creates_54_cards():
    """Test that JokerDeckFactory creates a deck with 54 cards."""
    factory = JokerDeckFactory()
    deck = factory.create_deck()
    assert deck.cards_left() == 54

def test_joker_deck_factory_contains_jokers():
    """Test that a joker deck contains exactly one Black Joker and one Red Joker."""
    factory = JokerDeckFactory()
    deck = factory.create_deck()
    
    black_joker_count = 0
    red_joker_count = 0
    
    for _ in range(deck.cards_left()): # Deal all cards
        card = deck.draw_card(replace=False)
        if card.value == 'Black Joker':
            black_joker_count += 1
        elif card.value == 'Red Joker':
            red_joker_count += 1
            
    assert black_joker_count == 1, "Joker deck should contain exactly one Black Joker."
    assert red_joker_count == 1, "Joker deck should contain exactly one Red Joker."
    assert deck.cards_left() == 0 # Ensure all cards were dealt

def test_joker_deck_factory_unique_cards():
    """Test that all cards in a joker deck are unique."""
    factory = JokerDeckFactory()
    deck = factory.create_deck()
    
    cards_in_deck = []
    for _ in range(deck.cards_left()): # Deal all cards
        cards_in_deck.append(deck.draw_card(replace=False))
    
    unique_cards = set(cards_in_deck)
    assert len(unique_cards) == 54, "Joker deck should have 54 unique cards."
    assert deck.cards_left() == 0 # Ensure all cards were dealt

