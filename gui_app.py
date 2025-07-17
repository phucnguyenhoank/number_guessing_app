import tkinter as tk
from src.game import Game
from src.match import Match

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more detailed info
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("number_guessing_game.log"),  # Logs to a file
        logging.StreamHandler()               # Also prints to console
    ]
)
logger = logging.getLogger(__name__)


class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Card Game")
        self.STARTING_POINTS = 60
        self.MATCH_COST = 25
        self.WIN_THRESHOLD = 50
        self.LOSE_THRESHOLD = 30

        self.game = Game(self.STARTING_POINTS, self.MATCH_COST, self.WIN_THRESHOLD, self.LOSE_THRESHOLD)
        self.match = None

        # GUI elements
        self.points_label = tk.Label(root, text=f"Points: {self.game.get_points()}")
        self.points_label.pack()

        self.status_label = tk.Label(root, text="Click 'Start Match' to begin!")
        self.status_label.pack()

        self.card_label = tk.Label(root, text="")
        self.card_label.pack()

        self.start_button = tk.Button(root, text="Start Match", command=self.start_match)
        self.start_button.pack()

        self.guess_frame = tk.Frame(root)
        self.guess_greater = tk.Button(self.guess_frame, text="Greater (g)", command=lambda: self.make_guess("g"))
        self.guess_greater.pack(side=tk.LEFT)
        self.guess_less = tk.Button(self.guess_frame, text="Less (l)", command=lambda: self.make_guess("l"))
        self.guess_less.pack(side=tk.LEFT)

        self.decision_frame = tk.Frame(root)
        self.continue_button = tk.Button(self.decision_frame, text="Continue (y)", command=lambda: self.continue_match())
        self.continue_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.decision_frame, text="Stop", command=self.stop_match)
        self.stop_button.pack(side=tk.LEFT)

        # Initially hide guess and decision buttons
        self.guess_frame.pack_forget()
        self.decision_frame.pack_forget()

    def update_points(self):
        """Update the points display."""
        self.points_label.config(text=f"Points: {self.game.get_points()}")

    def start_match(self):
        """Start a new match if possible."""
        logger.info("Attempting to start a new match.")
        if not self.game.can_play_match():
            logger.warning("Not enough points to play a new match.")
            self.status_label.config(text=f"Not enough points to play (need at least {self.game.lose_threshold})!")
            return
        if not self.game.pay_for_match():
            logger.error("Payment for match failed unexpectedly.")
            self.status_label.config(text="Error paying for match!")
            return

        self.match = Match()
        house_card = self.match.deal_cards()
        logger.info(f"House card dealt: {house_card}")
        self.update_points()
        self.status_label.config(text="Guess if your card is greater or less.")
        self.card_label.config(text=f"House's Card: {house_card}")
        self.start_button.pack_forget()
        self.guess_frame.pack()
        self.decision_frame.pack_forget()

    def make_guess(self, guess):
        """Process the user's guess."""
        player_card = self.match.reveal_player_card()
        logger.info(f"Player guessed '{guess}'")
        logger.info(f"House card: {self.match.house_card}, Player card: {player_card}")
        self.card_label.config(text=f"House's Card: {self.match.house_card}\nYour Card: {player_card}")
        if self.match.is_guess_correct(guess):
            logger.info("Guess is correct.")
            if self.match.get_reward() >= self.match.win_threshold:
                self.status_label.config(text=f"Correct! Reward reached {self.match.get_reward()}!")
                self.end_match(self.match.get_reward())
            else:
                logger.info("Guess is wrong.")
                self.status_label.config(text="Correct guess! Continue to double reward?")
                self.guess_frame.pack_forget()
                self.decision_frame.pack()
        else:
            self.status_label.config(text="Wrong guess! Match ended.")
            self.end_match(0)

    def continue_match(self):
        """Continue the match by doubling the reward."""
        self.match.double_reward()
        logger.info(f"Reward doubled to {self.match.get_reward()}")
        house_card = self.match.deal_cards()
        self.status_label.config(text=f"Reward doubled to {self.match.get_reward()}. Guess again.")
        self.card_label.config(text=f"House's Card: {house_card}")
        self.decision_frame.pack_forget()
        self.guess_frame.pack()

    def stop_match(self):
        """Stop the match and take the current reward."""
        logger.info(f"Player stopped match with reward {self.match.get_reward()}")
        self.status_label.config(text=f"Match stopped with reward {self.match.get_reward()}.")
        self.end_match(self.match.get_reward())

    def end_match(self, reward):
        """End the match, update points, and check win/lose conditions."""
        self.game.add_reward(reward)
        self.update_points()
        self.guess_frame.pack_forget()
        self.decision_frame.pack_forget()
        self.start_button.pack()

        if self.game.check_win():
            self.status_label.config(text="Congratulations! You win the game!")
            self.start_button.config(state=tk.DISABLED)
        elif not self.game.can_play_match():
            self.status_label.config(text="Game over: Not enough points to continue.")
            self.start_button.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Click 'Start Match' for a new match.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApp(root)
    root.mainloop()