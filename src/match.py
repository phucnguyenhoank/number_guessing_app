from .deck import JokerDeckFactory

class Match:
    def __init__(self):
        self.deck = JokerDeckFactory().create_deck()
        self.potential_reward = 20

    def play_match(self):
        while True:
            if len(self.deck) < 2:
                print("Not enough cards left in the deck! Auto restart the deck.")
                self.deck = JokerDeckFactory().create_deck()

            house_card = self.deck.deal_card()
            print(f"House's card: {house_card}")
            player_card = self.deck.deal_card()

            guess = input("Is your card greater or less than the House's card? (g/l): ").strip().lower()
            print(f"Your card: {player_card}")

            # If Player got right
            if (guess == "g" and player_card > house_card) or (guess == "l" and player_card < house_card):
                print("Correct guess!")
                if self.potential_reward >= 1000:
                    return self.potential_reward
                
                decision = input("Continue to get x2 reward in the next round? (y/stop): ").strip().lower()
                if decision == "stop":
                    return self.potential_reward
                else:
                    self.potential_reward *= 2
                    print(f"Reward doubled to {self.potential_reward} for the next round.")
            else:
                print("Wrong guess.")
                return 0