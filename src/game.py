from .match import Match

class Game:
    def __init__(self):
        self.points = 60

    def play_game(self):
        while True:
            print(f"\nCurrent points: {self.points}")
            if self.points < 25:
                print("Not enough points to play a match.")
                if self.points < 30:
                    print("You lose the game!")
                else:
                    print("Game ended without win or loss.")
                break

            self.points -= 25
            print("You paid 25 points to start a match.")
            match = Match()
            reward = match.play_match()
            self.points += reward
            print(f"Match ended. Reward: {reward}. Total points: {self.points}")

            if self.points >= 1000:
                print("Congratulations! You win the game!")
                break
            elif self.points < 30:
                print("Sorry, you lose the game!")
                break