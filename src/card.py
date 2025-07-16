
class Card:
    _VALUES = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
               '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13, 'Black Joker': 14, 'Red Joker': 14}

    def __init__(self, value, suit=None):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self._VALUES[self.value] < self._VALUES[other.value]

    def __gt__(self, other):
        return self._VALUES[self.value] > self._VALUES[other.value]

    def __eq__(self, other):
        return self._VALUES[self.value] == self._VALUES[other.value]

    def __repr__(self):
        if self.suit:
            return f"{self.value} of {self.suit}"
        return self.value