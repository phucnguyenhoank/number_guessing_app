# The Card class provided by the user
class Card:
    _VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
               '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'Black Joker': 14, 'Red Joker': 15}
    _SUITS = {'Spade': 1, 'Club': 2, 'Diamond': 3, 'Heart': 4}

    def __init__(self, value, suit=None):
        # Validate if the value is in _VALUES
        if value not in self._VALUES:
            raise ValueError(f"Invalid card value: {value}")
        # Validate if the suit is in _SUITS if provided
        if suit is not None and suit not in self._SUITS:
            raise ValueError(f"Invalid card suit: {suit}")

        self.value = value
        self.suit = suit

    def __lt__(self, other):
        # First, compare by value
        if self._VALUES[self.value] < self._VALUES[other.value]:
            return True
        # If values are equal, compare by suit (if both have suits)
        if self._VALUES[self.value] == self._VALUES[other.value] and self.suit is not None and other.suit is not None:
            return self._SUITS[self.suit] < self._SUITS[other.suit]
        # If values are equal but one or both don't have suits, or if self.value is not less than other.value
        return False

    def __gt__(self, other):
        # First, compare by value
        if self._VALUES[self.value] > self._VALUES[other.value]:
            return True
        # If values are equal, compare by suit (if both have suits)
        if self._VALUES[self.value] == self._VALUES[other.value] and self.suit is not None and other.suit is not None:
            return self._SUITS[self.suit] > self._SUITS[other.suit]
        # If values are equal but one or both don't have suits, or if self.value is not greater than other.value
        return False

    def __eq__(self, other):
        # Check for equality based on both value and suit
        # If one has a suit and the other doesn't, they are not equal
        if (self.suit is None and other.suit is not None) or \
           (self.suit is not None and other.suit is None):
            return False
        
        # If both have suits, compare both value and suit
        if self.suit is not None and other.suit is not None:
            return self._VALUES[self.value] == self._VALUES[other.value] and \
                   self._SUITS[self.suit] == self._SUITS[other.suit]
        
        # If neither has a suit (e.g., Jokers initialized without suit), compare only value
        return self._VALUES[self.value] == self._VALUES[other.value]

    def __repr__(self):
        # Representation includes suit if it exists
        if self.suit:
            return f"{self.value} of {self.suit}"
        # Otherwise, just the value (e.g., for Jokers)
        return f"{self.value}"