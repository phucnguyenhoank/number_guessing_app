from functools import total_ordering

@total_ordering
class Card:
    _VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
               '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'Black Joker': 14, 'Red Joker': 15}
    _SUITS = {'Spade': 1, 'Club': 2, 'Diamond': 3, 'Heart': 4}

    def __init__(self, value, suit=None):
        if value not in self._VALUES:
            raise ValueError(f"Invalid card value: {value}")
        if suit is not None and suit not in self._SUITS:
            raise ValueError(f"Invalid card suit: {suit}")
        self.value = value
        self.suit = suit

    def __eq__(self, other):
        if not isinstance(other, Card):
            return NotImplemented

        if (self.suit is None) != (other.suit is None):
            return False

        if self.suit is not None:
            return (self._VALUES[self.value] == self._VALUES[other.value] and
                    self._SUITS[self.suit] == self._SUITS[other.suit])
        return self._VALUES[self.value] == self._VALUES[other.value]

    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented

        if self._VALUES[self.value] != self._VALUES[other.value]:
            return self._VALUES[self.value] < self._VALUES[other.value]
        if self.suit is not None and other.suit is not None:
            return self._SUITS[self.suit] < self._SUITS[other.suit]
        return False

    def __repr__(self):
        return f"{self.value} of {self.suit}" if self.suit else f"{self.value}"
