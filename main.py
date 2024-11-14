# main.py
from game.ai_player import AIPlayer
from game.game import Game
from game.human_player import HumanPlayer
from ui.console_ui import display_message, get_user_input


def initialize_players():
    players = []
    human_player = None

    # Ask if the user wants to add a human player
    add_human = get_user_input("Do you want to add a human player? (yes/no): ").strip().lower()
    if add_human in ['yes', 'y']:
        if not any(isinstance(p, HumanPlayer) for p in players):
            name = get_user_input("Enter the name for the human player: ").strip()
            human_player = HumanPlayer(name)
            players.append(human_player)
        else:
            display_message("A human player has already been added. Only one human player is allowed.")

    # Ask for the number of AI players
    while True:
        try:
            num_ai = int(get_user_input("Enter the number of AI players: ").strip())
            if num_ai < 0:
                display_message("Number of AI players cannot be negative.")
                continue
            break
        except ValueError:
            display_message("Please enter a valid integer for the number of AI players.")

    for i in range(1, num_ai + 1):
        ai_name = f"AI Bot {i}"
        players.append(AIPlayer(ai_name))

    if not players:
        display_message("No players added. Exiting the game.")
        exit()

    return players

def main():
    display_message("Welcome to Gartic Phone Clone!")

    players = initialize_players()

    display_message(f"\nPlayers in the game:")
    for player in players:
        player_type = "Human" if isinstance(player, HumanPlayer) else "AI"
        display_message(f"- {player.name} ({player_type})")

    # Initialize and start the game
    game = Game(players)
    while True:
        try:
            rounds = int(get_user_input("\nEnter the number of rounds you want to play: ").strip())
            if rounds <= 0:
                display_message("Number of rounds must be positive.")
                continue
            break
        except ValueError:
            display_message("Please enter a valid integer for the number of rounds.")

    game.start(rounds=rounds)

    # Display game history
    game.display_history()

    display_message("\nGame Over!")

if __name__ == "__main__":
    main()
