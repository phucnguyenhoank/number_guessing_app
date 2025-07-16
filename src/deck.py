from .card import Card # Assuming Card class is in a 'card' module
import random

class Deck:
    def __init__(self, cards, shuffle_on_init=False):
        # Initialize _cards as a list of Card objects
        self._cards = list(cards)
        if shuffle_on_init:
            self.shuffle()

    def shuffle(self):
        """Shuffles the cards in the deck randomly."""
        random.shuffle(self._cards)

    def deal_card(self):
        """
        Deals a single card from the top of the deck.
        Raises IndexError if the deck is empty.
        """
        if not self._cards:
            raise IndexError("Cannot deal card from an empty deck.")
        return self._cards.pop(0)

    def add_card(self, card):
        """
        Adds a single card to the bottom of the deck.
        Args:
            card (Card): The Card object to add to the deck.
        """
        if not isinstance(card, Card):
            raise TypeError("Only Card objects can be added to the deck.")
        self._cards.append(card)

    def __len__(self):
        """
        Returns the number of cards currently in the deck.
        This replaces the cards_left() method.
        """
        return len(self._cards)

    def __contains__(self, card):
        """
        Checks if a given card exists in the deck.
        Args:
            card (Card): The Card object to check for.
        Returns:
            bool: True if the card is in the deck, False otherwise.
        """
        if not isinstance(card, Card):
            # If the item is not a Card, it cannot be in the deck
            return False
        return card in self._cards

    def __repr__(self):
        """Returns a string representation of the Deck."""
        return f"Deck with {len(self)} cards remaining."

class DeckFactory:
    """Abstract base class for creating decks."""
    def create_deck(self):
        """
        Creates and returns a new deck.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_deck()")

class StandardDeckFactory(DeckFactory):
    """Factory for creating a standard 52-card deck."""
    def create_deck(self, shuffle_on_init=False):
        """
        Creates a standard 52-card deck (A-K of Spades, Clubs, Diamonds, Hearts).
        Args:
            shuffle_on_init (bool): If True, shuffles the deck upon creation.
        Returns:
            Deck: A new standard deck.
        """
        cards = []
        suits = ['Spade', 'Club', 'Diamond', 'Heart']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for value in values:
                cards.append(Card(value, suit))
        return Deck(cards, shuffle_on_init)

class JokerDeckFactory(DeckFactory):
    """Factory for creating a deck with standard cards plus two Jokers."""
    def create_deck(self, shuffle_on_init=False):
        """
        Creates a deck with 52 standard cards and two Jokers (Black and Red).
        Args:
            shuffle_on_init (bool): If True, shuffles the deck upon creation.
        Returns:
            Deck: A new deck including Jokers.
        """
        # Start with a standard deck's cards
        standard_deck_cards = StandardDeckFactory().create_deck()._cards
        cards = standard_deck_cards.copy() # Make a copy to avoid modifying the original list
        cards.append(Card('Black Joker')) # Note: No suit for Jokers
        cards.append(Card('Red Joker'))
        return Deck(cards, shuffle_on_init) # Pass shuffle_on_init to the Deck constructor
