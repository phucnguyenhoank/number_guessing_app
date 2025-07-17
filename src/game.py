from .match import Match

class Game:
    def __init__(self, starting_points=60, match_cost=25, win_threshold=1000, lose_threshold=30):
        self.points = starting_points
        self.match_cost = match_cost
        self.win_threshold = win_threshold
        self.lose_threshold = lose_threshold

    def can_play_match(self):
        """Check if there are enough points to play a match."""
        return self.points >= self.lose_threshold

    def pay_for_match(self):
        """Deduct the match cost from points if possible."""
        if self.points >= self.match_cost:
            self.points -= self.match_cost
            return True
        return False

    def add_reward(self, reward):
        """Add the match reward to total points."""
        self.points += reward

    def check_win(self):
        """Check if the win threshold is reached."""
        return self.points >= self.win_threshold

    def get_points(self):
        """Return the current points."""
        return self.points