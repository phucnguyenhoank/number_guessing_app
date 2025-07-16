from functools import total_ordering

@total_ordering
class Card:
    # Define orderings as class attributes (these are constant)
    SUIT_ORDER = {'Spade': 1, 'Club': 2, 'Diamond': 3, 'Heart': 4}
    VALUE_ORDER = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9, '10': 10,
        'J': 11, 'Q': 12, 'K': 13,
        'Black Joker': 14, 'Red Joker': 15
    }

    def __init__(self, value, suit):
        """
        Initializes a new Card object.
        value: 'A', '2', ..., 'K', 'Black Joker', or 'Red Joker'
        suit: one of 'Heart', 'Diamond', 'Club', 'Spade', or None for Jokers
        """
        # Validate inputs first
        if value not in Card.VALUE_ORDER:
            raise ValueError(f"Invalid card value: '{value}'")

        if value in ['Black Joker', 'Red Joker']:
            if suit is not None:
                raise ValueError("Jokers cannot have a suit.")
        elif suit not in Card.SUIT_ORDER:
            raise ValueError(f"Invalid suit: '{suit}' for value '{value}'")

        # Store the values in "private" attributes (using single underscore convention)
        # These attributes will hold the actual data.
        self._value = value
        self._suit = suit

    @property
    def value(self):
        """
        Allows reading the card's value.
        There is no @value.setter, so 'value' cannot be modified after creation.
        """
        return self._value

    @property
    def suit(self):
        """
        Allows reading the card's suit.
        There is no @suit.setter, so 'suit' cannot be modified after creation.
        """
        return self._suit

    def __repr__(self):
        """
        Returns a string representation of the card for debugging and display.
        """
        if self.suit:
            return f"{self.value} of {self.suit}"
        return f"{self.value}"

    def _rank(self):
        """
        Returns a tuple (value_rank, suit_rank) used for comparison logic.
        This method is internal to the class's comparison logic.
        """
        val_rank = Card.VALUE_ORDER[self.value]
        # Get suit rank, default to 0 for Jokers (which have no suit)
        suit_rank = Card.SUIT_ORDER.get(self.suit, 0)
        return (val_rank, suit_rank)

    def __eq__(self, other):
        """
        Defines equality (==) comparison between two Card objects.
        """
        if not isinstance(other, Card):
            # If 'other' is not a Card, comparison is not implemented
            return NotImplemented
        return self._rank() == other._rank()

    def __lt__(self, other):
        """
        Defines less than (<) comparison between two Card objects.
        """
        if not isinstance(other, Card):
            # If 'other' is not a Card, comparison is not implemented
            return NotImplemented
        return self._rank() < other._rank()
