import random
from abc import ABC, abstractmethod
from src.card import Card # Import the Card class

class Deck:
    """
    Represents a deck of playing cards.
    This is the 'Product' created by the factories.
    """
    def __init__(self, cards):
        """
        Initializes a Deck with a given list of Card objects.
        The list of cards should be created by a factory.
        """
        # _cards directly holds the cards currently in the deck.
        # We make a copy of the input list to ensure the deck's internal
        # state is independent of the list passed during initialization.
        self._cards = list(cards)
        
        self.shuffle() # Shuffle the deck immediately upon creation
        print("Deck initialized and shuffled.")

    def shuffle(self):
        """Shuffles the cards currently in the deck."""
        random.shuffle(self._cards)
        print("Deck shuffled.")

    def draw_card(self, replace=False):
        """
        Draws a card from the deck.

        Args:
            replace (bool): If True, the card is drawn with replacement (it remains
                            in the deck). If False (default), the card is drawn
                            without replacement and removed from the deck.

        Returns:
            Card: The drawn Card object.

        Raises:
            IndexError: If trying to draw from an empty deck.
        """
        if not self._cards:
            raise IndexError("Cannot draw card from an empty deck.")
        
        # Select a random index
        random_index = random.randrange(len(self._cards))
        
        drawn_card = self._cards[random_index] # Get the card at the random index

        if not replace:
            # If no replacement, remove the card from the deck
            self._cards.pop(random_index)
            print(f"Drew {drawn_card} (without replacement). Cards left: {self.cards_left()}")
        else:
            # If with replacement, the card remains in the deck
            print(f"Drew {drawn_card} (with replacement). Cards left: {self.cards_left()}")
            
        return drawn_card

    def deal_card(self):
        """
        Removes and returns the top card from the deck.
        Raises an IndexError if the deck is empty.
        """
        if not self._cards:
            raise IndexError("Cannot deal card from an empty deck.")
        return self._cards.pop() # pop() removes and returns the last item
    
    def cards_left(self):
        """Returns the number of cards remaining in the deck."""
        return len(self._cards)

    def __repr__(self):
        """Returns a string representation of the deck."""
        return f"Deck with {self.cards_left()} cards remaining."

class DeckFactory(ABC):
    """
    Abstract Base Class for creating different types of decks.
    This defines the 'factory method' interface.
    """
    @abstractmethod
    def _make_cards(self):
        """
        Abstract method that concrete factories must implement to
        return the specific list of Card objects for their deck type.
        This is the core of the Factory Method.
        """
        pass

    def create_deck(self):
        """
        The factory method. It uses the _make_cards method (implemented by subclasses)
        to get the list of cards and then creates and returns a Deck object.
        """
        cards = self._make_cards()
        return Deck(cards)

class StandardDeckFactory(DeckFactory):
    """
    Concrete Factory for creating a standard 52-card deck (no Jokers).
    """
    def _make_cards(self):
        """
        Creates a list of 52 standard playing cards.
        """
        cards = []
        suits = ['Spade', 'Club', 'Diamond', 'Heart']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for value in values:
                cards.append(Card(value, suit))
        return cards

class JokerDeckFactory(DeckFactory):
    """
    Concrete Factory for creating a 54-card deck (52 standard + 2 Jokers).
    """
    def _make_cards(self):
        """
        Creates a list of 52 standard playing cards plus two Jokers.
        """
        cards = []
        suits = ['Spade', 'Club', 'Diamond', 'Heart']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for value in values:
                cards.append(Card(value, suit))
        
        # Add Jokers
        cards.append(Card('Black Joker', None))
        cards.append(Card('Red Joker', None))
        return cards

# --- Example Usage (Client Code) ---
if __name__ == "__main__":
    print("--- Creating a Standard Deck ---")
    standard_factory = StandardDeckFactory()
    standard_deck = standard_factory.create_deck()
    print(standard_deck)

    print("\n--- Drawing cards without replacement ---")
    for _ in range(5):
        try:
            card = standard_deck.draw_card(replace=False)
        except IndexError as e:
            print(e)
            break
    print(standard_deck)

    print("\n--- Drawing cards with replacement ---")
    # Resetting the deck for a fresh start for replacement draws
    standard_deck = standard_factory.create_deck() # Re-create to get a full deck
    print(standard_deck)
    for _ in range(5):
        card = standard_deck.draw_card(replace=True)
    print(standard_deck) # Cards left should remain the same as they were replaced

    print("\n--- Creating a Deck with Jokers ---")
    joker_factory = JokerDeckFactory()
    joker_deck = joker_factory.create_deck()
    print(joker_deck)

    print("\n--- Drawing cards from Joker Deck (without replacement) ---")
    for _ in range(3):
        card = joker_deck.draw_card(replace=False)
    print(joker_deck)

    # Demonstrate that drawn cards are immutable
    dealt_card = joker_deck.draw_card(replace=True) # Draw one with replacement
    print(f"Dealt card for immutability check: {dealt_card}")
    try:
        dealt_card.value = "New Value"
    except AttributeError as e:
        print(f"Attempted to modify dealt card: {e}")
