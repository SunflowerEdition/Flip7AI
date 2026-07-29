from Game.data.cards import CardId, CARD_METADATA, ActionType
from Game.data.game_state import GameState
from Game.data.player import AddCardResult
from agents.base_agent import Agent


def resolve_number_card(state: GameState, player_idx: int, card_id: CardId):
    player = state.players[player_idx]
    result = player.add_card(card_id)

    if result == AddCardResult.SECOND_CHANCE_USED:
        # If a second chance is used, both the second chance and card get discarded immediately
        state.discard_pile.append(card_id)
        state.discard_pile.append(CardId.SECOND_CHANCE)


def resolve_action_card(state: GameState, card_id: CardId, agent: Agent):
    action_type = CARD_METADATA[card_id].action
    legal_targets = state.legal_targets_for(action_type)

    target_idx = agent.choose_target(state, action_type, legal_targets)
    target = state.players[target_idx]

    if action_type == ActionType.FLIP_THREE:
        # Three cards get played on this player
    else:
        target.add_card(card_id)
