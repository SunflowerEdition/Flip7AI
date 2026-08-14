import random

from game.data.cards import ActionType, CardId, CARD_METADATA, CardCategory
from game.data.game_state import GameState
from agents.base_agent import Agent, Decision


class ProbThresholdAgent(Agent):
    def __init__(self, threshold: float, name: str):
        super().__init__(name)
        self._threshold = threshold

    def choose_action(self, state: GameState, player_idx: int) -> Decision:
        """Stays whenever the probability of busting on the next draw exceeds
        `threshold`; otherwise draws. Ignores everything except bust risk —
        doesn't weigh potential point gain, action-card effects, or flip-7 upside.
        """
        if state.players[player_idx].second_chance:
            return Decision.DRAW

        unseen_cards = state.unseen_cards
        total_unseen = int(unseen_cards.sum())
        if total_unseen == 0:
            raise RuntimeError("THIS SHOULD NEVER HAPPEN!")

        bust_prob = 0.0
        for card_id in state.players[player_idx].number_cards:
            unseen_count = unseen_cards[card_id]
            prob = unseen_count / total_unseen
            bust_prob += prob

        if bust_prob < self._threshold:
            return Decision.DRAW
        return Decision.STAY


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