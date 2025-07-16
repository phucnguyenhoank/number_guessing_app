from .card import Card
import random

class Deck:
    def __init__(self, cards, shuffle_on_init=True):
        self._cards = list(cards)
        if shuffle_on_init:
            self.shuffle()

    def shuffle(self):
        random.shuffle(self._cards)

    def deal_card(self):
        if not self._cards:
            raise IndexError("Cannot deal card from an empty deck.")
        return self._cards.pop(0)

    def cards_left(self):
        return len(self._cards)

    def __repr__(self):
        return f"Deck with {self.cards_left()} cards remaining."

class DeckFactory:
    def create_deck(self):
        raise NotImplementedError("Subclasses must implement create_deck()")

class StandardDeckFactory(DeckFactory):
    def create_deck(self):
        cards = []
        suits = ['Spade', 'Club', 'Diamond', 'Heart']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        for suit in suits:
            for value in values:
                cards.append(Card(value, suit))
        return Deck(cards)

class JokerDeckFactory(DeckFactory):
    def create_deck(self):
        cards = StandardDeckFactory().create_deck()._cards.copy()
        cards.append(Card('Black Joker', None))
        cards.append(Card('Red Joker', None))
        return Deck(cards)