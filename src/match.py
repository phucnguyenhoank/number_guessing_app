from .deck import JokerDeckFactory
from .card import Card

class Match:
    def __init__(self, initial_reward=20, win_threshold=1000):
        self.deck = JokerDeckFactory().create_deck()
        self.initial_reward = initial_reward
        self.potential_reward = initial_reward
        self.win_threshold = win_threshold
        self.house_card = None
        self.player_card = None

    def reset_deck_if_needed(self):
        """Reset the deck if fewer than 2 cards remain."""
        if len(self.deck) < 2:
            self.deck = JokerDeckFactory().create_deck()

    def deal_cards(self):
        """Deal house and player cards, return the house card."""
        self.reset_deck_if_needed()
        self.house_card = self.deck.deal_card()
        self.player_card = self.deck.deal_card()
        return self.house_card

    def reveal_player_card(self):
        """Return the player's card."""
        return self.player_card

    def is_guess_correct(self, guess):
        """Check if the guess ('g' or 'l') is correct."""
        if guess == "g":
            return self.player_card > self.house_card
        elif guess == "l":
            return self.player_card < self.house_card
        return False

    def double_reward(self):
        """Double the potential reward for the next round."""
        self.potential_reward *= 2
    
    def remove_reward(self):
        """Set the potential reward to zero."""
        self.potential_reward = 0

    def get_reward(self):
        """Return the current potential reward."""
        return self.potential_reward

    def reset_reward(self):
        """Reset the potential reward to the initial value."""
        self.potential_reward = self.initial_reward