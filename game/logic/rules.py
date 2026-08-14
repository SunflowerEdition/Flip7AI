from game.data.cards import CardId, CARD_METADATA, ActionType, CardCategory
from game.data.game_state import GameState
from game.data.player import AddCardResult
from game.logic.deck import draw_card
from agents.base_agent import Agent
from typing import NamedTuple
import random

from game.render.pygame_renderer import CardRenderer


class Event(NamedTuple):
    player_idx: int
    card_id: CardId


def resolve_drawn_card(
        state: GameState,
        player_idx: int,
        card_id: CardId,
        agents: list[Agent],
        rng: random.Random,
        renderer: CardRenderer | None = None
) -> None:
    """Resolve the specified card. Called recursively if Flip Three is played.

    Number cards, modifier, freeze, and second chance cards are resolved immediately.
    Flip Three cards have special rules:
        1) The targeted player flips three cards in a row, and plays them immediately
        2) Stop drawing immediately if the target player flips 7, busts, or gets frozen.
        3) Additional Flip Three or Freeze cards are delayed until AFTER all three cards
            are drawn, provided the target player is still active.
        4) In the event the target player is no longer active, all extra cards waiting to
            be played are discarded.

    :param state: The state of the game
    :param player_idx: The index of the player playing the card
    :param card_id: The ID of the card being played
    :param agents: List of agents playing the game.
    :param rng: The random number generator
    :param renderer: The game renderer.
    """
    event_queue: list[Event] = []

    # If Number or modifier card, resolve immediately
    if CARD_METADATA[card_id].category in [CardCategory.NUMBER, CardCategory.MODIFIER]:
        result = state.players[player_idx].add_card(card_id)
        if result == AddCardResult.SECOND_CHANCE_USED:
            # If a second chance is used (on Number) both the second chance and card get discard immediately
            state.discard_pile.append(card_id)
            state.discard_pile.append(CardId.SECOND_CHANCE)
            if renderer is not None:
                renderer.render(state, message=f"Second chance and {card_id._name_} discarded.")
        return

    # Otherwise it's an action card and handle accordingly
    action_type = CARD_METADATA[card_id].action
    targets = state.legal_targets_for(action_type)

    # If there are no targets available, the card is discarded
    if not targets:
        state.discard_pile.append(card_id)
        if renderer is not None:
            renderer.render(state, message=f"No legal targets, {card_id._name_} discarded.")
        return

    # Select the target using the associated agent
    target_idx = agents[player_idx].choose_target(state, player_idx, action_type, targets)
    target_player = state.players[target_idx]

    if action_type in (ActionType.FREEZE, ActionType.SECOND_CHANCE):
        target_player.add_card(card_id)
        if renderer is not None:
            renderer.render(state, message=f"Player {target_idx} gains {action_type._name_}.")
    else: # Flip Three
        for _ in range(3):
            # If player is no longer active or flipped seven, stop drawing cards
            if not target_player.is_active():
                break

            # Resolve card right away unless Freeze or Flip Three
            drawn_card_id = draw_card(state, rng)
            if renderer is not None:
                renderer.render(state, drawn_card=True, player_idx=target_idx, card_id=drawn_card_id,
                                message=f"Player {target_idx} drew {drawn_card_id._name_} (FLIP THREE)")
            if drawn_card_id in [CardId.FREEZE, CardId.FLIP_THREE]:
                event_queue.append(Event(player_idx=target_idx, card_id=drawn_card_id))
            else:
                resolve_drawn_card(state, target_idx, drawn_card_id, agents, rng)

        # Resolve the event queue cards (while player is active)
        while len(event_queue) > 0:
            if not target_player.is_active():
                break
            event_player_idx, event_card_id = event_queue.pop(0)
            resolve_drawn_card(state, event_player_idx, event_card_id, agents, rng)

        # Discard any cards still leftover in the event queue
        while len(event_queue) > 0:
            _, drawn_card_id = event_queue.pop()
            state.discard_pile.append(drawn_card_id)

        # Discard used flip three
        state.discard_pile.append(card_id)

def end_round(state: GameState) -> None:
    """End the round of the game.

    This function starts by counting the scores of each player, then cleaning
    up the cards by adding the cards from the players hands to the discard pile,
    and finally resetting the game for the next round.

    :param state: The state of the game.
    """
    # Count all scores
    for player in state.players:
        if player.busted:
            continue
        player.score += player.count_score()

    # Card clean-up
    for player in state.players:
        for card_id in player.number_cards:
            state.discard_pile.append(card_id)
        for card_id in player.modifier_cards:
            state.discard_pile.append(card_id)
        if player.frozen:
            state.discard_pile.append(CardId.FREEZE)
        if player.second_chance:
            state.discard_pile.append(CardId.SECOND_CHANCE)
        player.reset_round()
