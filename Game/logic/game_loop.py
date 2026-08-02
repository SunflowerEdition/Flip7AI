import random

from Game.data.game_state import GameState
from Game.data.player import Player
from Game.logic.deck import create_deck, count_unseen_cards, draw_card
from Game.logic.rules import resolve_drawn_card, end_round
from agents.base_agent import Agent, Decision


def new_game_state(num_players: int, rng: random.Random) -> GameState:
    draw_pile = create_deck()
    rng.shuffle(draw_pile)
    players = [Player() for _ in range(num_players)]
    starting_player_idx = rng.randrange(num_players)
    state = GameState(
        draw_pile=draw_pile,
        discard_pile=[],
        players=players,
        current_player_idx=starting_player_idx,
        starting_player_idx=starting_player_idx,
        round_number=1,
    )
    state.unseen_cards = count_unseen_cards(draw_pile)
    return state

def determine_winner(state: GameState, target_score: int) -> int | None:
    qualifying = [i for i, p in enumerate(state.players) if p.score >= target_score]
    if not qualifying:
        return None
    max_score = max(state.players[i].score for i in qualifying)
    tied_for_max = [i for i in qualifying if state.players[i].score == max_score]
    return tied_for_max[0] if len(tied_for_max) == 1 else None

def play_round(state: GameState, agents: list[Agent], rng: random.Random) -> None:
    round_active = True
    while round_active:
        current_player = state.players[state.current_player_idx]

        # Each player gets one starting card (even if they got one from a flip three previously)
        if not current_player.dealt_first_card:
            current_player.dealt_first_card = True
            decision = Decision.DRAW
        else:
            decision = agents[state.current_player_idx].choose_action(state)

        if decision == Decision.STAY:
            state.players[state.current_player_idx].stayed = True
        else:
            drawn_card_id = draw_card(state, rng)
            resolve_drawn_card(state, state.current_player_idx, drawn_card_id, agents, rng)
            if state.anyone_flipped_seven():
                break
        round_active = state.update_active_player_idx()

    end_round(state)


def play_game(agents: list[Agent], rng: random.Random, target_score: int = 200, max_rounds: int = 1000) -> GameState:
    state = new_game_state(len(agents), rng)

    #while not is_game_over(state, target_score):
    while determine_winner(state, target_score) is None:
        if state.round_number > max_rounds:
            return state # Players are probably spamming stay

        play_round(state, agents, rng)
        state.round_number += 1
        state.update_starting_player_idx()

    return state
