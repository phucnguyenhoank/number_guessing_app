import pytest
import random
from src.card import Card
from src.deck import Deck, StandardDeckFactory, JokerDeckFactory

# Helper function to create a simple deck for testing
@pytest.fixture
def empty_deck():
    return Deck([])

@pytest.fixture
def standard_deck():
    return StandardDeckFactory().create_deck()

@pytest.fixture
def joker_deck():
    return JokerDeckFactory().create_deck()

def test_deck_init(standard_deck):
    # Test initialization with cards
    assert len(standard_deck) == 52
    
    # Test shuffle_on_init
    deck_shuffled = StandardDeckFactory().create_deck(shuffle_on_init=True)
    # It's hard to assert randomness, but we can check length
    assert len(deck_shuffled) == 52

def test_deck_shuffle(standard_deck):
    # Create a known order
    initial_order = list(standard_deck._cards)
    
    # Shuffle the deck
    standard_deck.shuffle()
    
    # After shuffling, the order should generally be different
    # (though there's a tiny chance it could be the same)
    # We assert that it's still the same length
    assert len(standard_deck) == 52
    # And that it's not exactly the same order (most of the time)
    # This test might occasionally fail due to random chance, but it's rare.
    assert standard_deck._cards != initial_order

def test_deck_deal_card(standard_deck, empty_deck):
    # Deal a card from a non-empty deck
    initial_len = len(standard_deck)
    dealt_card = standard_deck.deal_card()
    assert isinstance(dealt_card, Card)
    assert len(standard_deck) == initial_len - 1

    # Test dealing from an empty deck
    with pytest.raises(IndexError, match="Cannot deal card from an empty deck."):
        empty_deck.deal_card()

def test_deck_add_card(empty_deck, standard_deck):
    # Add a card to an empty deck
    card_to_add = Card('A', 'Spade')
    empty_deck.add_card(card_to_add)
    assert len(empty_deck) == 1
    assert card_to_add in empty_deck

    # Add a card to a non-empty deck
    initial_len = len(standard_deck)
    new_card = Card('K', 'Diamond')
    standard_deck.add_card(new_card)
    assert len(standard_deck) == initial_len + 1
    assert new_card in standard_deck
    
    # Test adding non-Card object
    with pytest.raises(TypeError, match="Only Card objects can be added to the deck."):
        empty_deck.add_card("not a card")

def test_deck_len(standard_deck, empty_deck):
    # Test len for a full standard deck
    assert len(standard_deck) == 52
    
    # Test len for an empty deck
    assert len(empty_deck) == 0

    # Test len after dealing
    standard_deck.deal_card()
    assert len(standard_deck) == 51

    # Test len after adding
    empty_deck.add_card(Card('2', 'Club'))
    assert len(empty_deck) == 1

def test_deck_contains(standard_deck, empty_deck):
    # Create some cards for testing
    card_A_spade = Card('A', 'Spade')
    card_K_heart = Card('K', 'Heart')
    # card_non_existent = Card('Q', 'Club') # Assuming this card is not in the standard deck initially if it's dealt

    # Test if existing cards are found
    assert card_A_spade in standard_deck
    assert card_K_heart in standard_deck

    # Deal a card and check if it's no longer in the deck
    dealt_card = standard_deck.deal_card()
    assert dealt_card not in standard_deck

    # # Test if a non-existent card is not found
    # assert card_non_existent not in standard_deck

    # Test contains on an empty deck
    assert card_A_spade not in empty_deck

    # Test contains with a non-Card object
    assert "not a card" not in standard_deck

def test_deck_repr(standard_deck, empty_deck):
    # Test repr for a full deck
    assert repr(standard_deck) == "Deck with 52 cards remaining."

    # Test repr for an empty deck
    assert repr(empty_deck) == "Deck with 0 cards remaining."

    # Test repr after dealing
    standard_deck.deal_card()
    assert repr(standard_deck) == "Deck with 51 cards remaining."

def test_standard_deck_factory():
    factory = StandardDeckFactory()
    deck = factory.create_deck()
    assert len(deck) == 52
    # Check a couple of specific cards to ensure they are there
    assert Card('A', 'Spade') in deck
    assert Card('K', 'Heart') in deck
    assert Card('2', 'Club') in deck
    # Ensure no jokers are present
    assert Card('Black Joker') not in deck

def test_joker_deck_factory():
    factory = JokerDeckFactory()
    deck = factory.create_deck()
    assert len(deck) == 54 # 52 standard + 2 jokers
    # Check for standard cards
    assert Card('A', 'Spade') in deck
    # Check for jokers
    assert Card('Black Joker') in deck
    assert Card('Red Joker') in deck
