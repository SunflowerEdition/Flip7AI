from game.data.cards import ActionType
from game.data.game_state import GameState
from agents.base_agent import Agent, Decision


class NumPointsAgent(Agent):
    def __init__(self, num_points: int, name: str):
        super().__init__(name)
        self._num_points = num_points

    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        # Always hit if there's a second chance active
        player = state.players[player_idx]
        if player.second_chance:
            return Decision.DRAW

        # Count the number of NUMBER cards
        points = sum(card.value for card in player.number_cards)
        if points >= self._num_points:
            return Decision.STAY

        return Decision.DRAW

    def choose_target(self, state: GameState, player_idx: int, action_type: ActionType, legal_targets: list[int]) -> int:
        # Player second chance on yourself, or the player with the least overall points if you can't
        if action_type == ActionType.SECOND_CHANCE:
            if player_idx in legal_targets:
                return player_idx
            return min(legal_targets, key=lambda p_idx: state.players[p_idx].score)

        # Player flip three on yourself if you have 2 or fewer cards, otherwise on the player with the most round points
        elif action_type == ActionType.FLIP_THREE:
            if player_idx in legal_targets and len(state.players[player_idx].number_cards) <= 2:
                return player_idx
            targets = [p_idx for p_idx in legal_targets if p_idx != player_idx]
            return max(targets or legal_targets, key=lambda p_idx: state.players[p_idx].count_score())

        # Freeze the player with the most overall points (not including themselves)
        targets = [p_idx for p_idx in legal_targets if p_idx != player_idx]
        return max(targets or legal_targets, key=lambda p_idx: state.players[p_idx].score)
