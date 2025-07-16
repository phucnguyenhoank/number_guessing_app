from .deck import Deck, JokerDeckFactory

class Match:
    def __init__(self):
        self.deck = JokerDeckFactory().create_deck()
        self.potential_reward = 20

    def play_match(self):
        while True:
            if self.deck.cards_left() < 2:
                print("Not enough cards left in the deck!")
                return 0

            house_card = self.deck.deal_card()
            print(f"House's card: {house_card}")
            player_card = self.deck.deal_card()

            guess = input("Is your card greater or less than the House's card? (greater/less): ").strip().lower()
            print(f"Your card: {player_card}")

            if (guess == "greater" and player_card > house_card) or (guess == "less" and player_card < house_card):
                print("Correct guess!")
                decision = input("Do you want to continue or stop? (continue/stop): ").strip().lower()
                if decision == "stop":
                    return self.potential_reward
                else:
                    self.potential_reward *= 2
                    print(f"Reward doubled to {self.potential_reward} for the next round.")
            else:
                print("Wrong guess or cards are equal. You lose this match.")
                return 0