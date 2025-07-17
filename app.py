from src.game import Game
from src.match import Match

STARTING_POINTS = 60
MATCH_COST = 25
WIN_THRESHOLD = 1000
LOSE_THRESHOLD = 30

game = Game(STARTING_POINTS, MATCH_COST, WIN_THRESHOLD, LOSE_THRESHOLD)

print(f"START THE GAME WITH {game.points} POINTS")
while game.can_play_match():
    game.pay_for_match()
    print(f"Paid {game.match_cost} points. Current points: {game.points}")

    # Start playing a Match
    match = Match()
    while True:
        # Deal cards and get the match result
        house_card = match.deal_cards()
        print(f"House's card: {house_card}")
        guess = input("Greater or less? (g/l): ").strip().lower()
        player_card = match.reveal_player_card()
        print(f"Your card: {player_card}")
        if match.is_guess_correct(guess):
            print("Correct!")

            # Automatically end the match if the player reaches win_threshold
            if match.get_reward() >= match.win_threshold:
                break

            decision = input(f"Continue? (y/stop): ").strip().lower()
            if decision == "stop":
                break
            match.double_reward()
            print(f"Reward doubled to {match.get_reward()}")
        else:
            print("Wrong!")
            match.remove_reward()
            break
    
    game.add_reward(match.get_reward())
    print(f"Match reward: {match.get_reward()}. Total points: {game.points}")
    if game.check_win():
        print("You win!")
        break
if not game.can_play_match():
    print(f"Not enough {game.lose_threshold} points (having {game.points} now) to continue!")
print(f"Final score: {game.points}")