import random

from agents.random_agent import RandomAgent
from game.data.player import Player
from game.logic.game_loop import play_game, determine_winner
from tests.conftest import AlwaysStayAgent, create_test_state, NUM_CARDS_IN_FULL_DECK


def test_game_cutoff():
    agents = [AlwaysStayAgent(name="Always Stay Agent") for _ in range(5)]
    state = play_game(agents, random.Random(), max_rounds=5)
    assert (state.round_number == 6)

def test_determine_winner_one_winner():
    players = [Player() for _ in range(5)]
    players[0].score = 240
    players[1].score = 239
    players[2].score = 264
    players[3].score = 176
    players[4].score = 45
    game_state = create_test_state(draw_pile=[], players=players)
    assert (determine_winner(game_state, 200) == 2)

def test_determine_winner_no_one_over_threshold():
    players = [Player() for _ in range(5)]
    players[0].score = 240
    players[1].score = 239
    players[2].score = 264
    players[3].score = 176
    players[4].score = 45
    game_state = create_test_state(draw_pile=[], players=players)
    assert (determine_winner(game_state, 300) is None)

def test_determine_winner_tied_game():
    players = [Player() for _ in range(5)]
    players[0].score = 240
    players[1].score = 264
    players[2].score = 264
    players[3].score = 176
    players[4].score = 45
    game_state = create_test_state(draw_pile=[], players=players)
    assert (determine_winner(game_state, 200) is None)

def test_game_consistency():
    agents = [RandomAgent(random.Random(), "Random Agent") for _ in range(5)]
    for _ in range(100_000):
        game_state = play_game(agents, random.Random())
        cards_in_draw = len(game_state.draw_pile)
        cards_in_discard = len(game_state.discard_pile)
        assert (cards_in_discard + cards_in_draw == NUM_CARDS_IN_FULL_DECK)
