from game.data.cards import ActionType
from game.data.game_state import GameState
from agents.base_agent import Agent, Decision


class PlayerAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        """Prompts the user to choose an action"""
        while True:
            choice = input("Draw (0) or stay (1) > ")
            if choice == "0":
                return Decision.DRAW
            elif choice == "1":
                return Decision.STAY
            else:
                print("Invalid choice.")

    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        """Prompts the user to choose an action"""
        while True:
            print(f"Legal targets: {legal_targets}")
            choice = input("Choice > ")
            try:
                choice = int(choice)
            except ValueError:
                print("Please enter a number.")
                continue
            if choice in legal_targets:
                return choice
            print("Invalid choice.")