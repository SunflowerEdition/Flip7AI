import random
from game.data.game_state import GameState
from game.data.player import Player
from game.logic.deck import create_deck, count_unseen_cards, draw_card
from game.logic.rules import resolve_drawn_card, end_round
from agents.base_agent import Agent, Decision


def play_game(agents: list[Agent], rng: random.Random, target_score: int = 200, max_rounds: int = 1000) -> GameState:
    """Play a full game to the target score.

    :param agents: List of agents playing the game.
    :param rng: The random number generator.
    :param target_score: The target score to play to (200 per the game rules).
    :param max_rounds: The maximum number of rounds to play (prevents soft-locks).
    :return: The final state of the game.
    """
    state = new_game_state(len(agents), rng)

    while determine_winner(state, target_score) is None:
        if state.round_number > max_rounds:
            break

        play_round(state, agents, rng)
        state.round_number += 1
        state.update_starting_player_idx()

    return state


def play_round(state: GameState, agents: list[Agent], rng: random.Random) -> None:
    """Play a single round of the game.

    A round is finished when all players are frozen/bust, or until one player Flips 7.

    :param state: The current game state.
    :param agents: List of agents playing the game.
    :param rng: The random number generator.
    """
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


def new_game_state(num_players: int, rng: random.Random) -> GameState:
    """Creates a new game state.

    :param num_players: The number of players playing in the game.
    :param rng: The random number generator.
    :return: The newly created game state.
    """
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
    """Determines the winner of the game if there is one.

    If there is a tie, there is no winner yet. So, None is returned.

    :param state: The current game state.
    :param target_score: The target score to win.
    :return: The index of the winner, or None if there is no winner (tie included).
    """
    qualifying = [i for i, p in enumerate(state.players) if p.score >= target_score]
    if not qualifying:
        return None
    max_score = max(state.players[i].score for i in qualifying)
    tied_for_max = [i for i in qualifying if state.players[i].score == max_score]
    return tied_for_max[0] if len(tied_for_max) == 1 else None
