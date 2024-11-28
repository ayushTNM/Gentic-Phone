# main.py
from game.ai_player import AIPlayer
from game.game import Game
from game.human_player import HumanPlayer
from ui.console_ui import display_message, get_user_input


def initialize_players():
    players = []

    # Ask if the user wants to add a human player
    add_human = get_user_input("Do you want to add a human player? (yes/no): ").strip().lower()
    if add_human in ['yes', 'y']:
        name = get_user_input("Enter the name for the human player: ").strip()
        players.append(HumanPlayer(name))

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

    # Enforce minimum of 3 players
    if len(players) < 3:
        display_message("The game requires at least 3 players to avoid self-assignment.")
        while len(players) < 3:
            if len(players) == 2:
                # Prompt to add another AI player
                ai_name = f"AI Bot {len(players) + 1}"
                display_message(f"Adding another AI player: {ai_name}")
                players.append(AIPlayer(ai_name))
            elif len(players) == 1:
                # Prompt to add more AI players
                try:
                    additional_ai = int(get_user_input("Enter the number of additional AI players to reach 3: ").strip())
                    if additional_ai < 1:
                        display_message("Please add at least 1 AI player.")
                        continue
                    for i in range(1, additional_ai + 1):
                        ai_name = f"AI Bot {len(players) + 1}"
                        display_message(f"Adding AI player: {ai_name}")
                        players.append(AIPlayer(ai_name))
                    if len(players) < 3:
                        display_message("Still less than 3 players. Adding more AI players.")
                except ValueError:
                    display_message("Please enter a valid integer.")
    
    return players

def main():
    display_message("Welcome to Gartic Phone Clone!")

    players = initialize_players()

    display_message("\nPlayers in the game:")
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
