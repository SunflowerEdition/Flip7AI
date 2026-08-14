import random
from agents.num_cards_agent import NumCardsAgent
from agents.num_points_agent import NumPointsAgent
from game.logic.game_loop import play_game


def run_tournament():
    num_games = 1_000_000
    available_agents = [
        NumCardsAgent(3, "3 Cards Agent"),
        NumCardsAgent(4, "4 Cards Agent"),
        NumCardsAgent(5, "5 Cards Agent"),
        NumPointsAgent(16, "16 Points Agent"),
        NumPointsAgent(17, "17 Points Agent"),
        NumPointsAgent(18, "18 Points Agent"),
        NumPointsAgent(19, "19 Points Agent"),
        NumPointsAgent(20, "20 Points Agent"),
        NumPointsAgent(21, "21 Points Agent"),
        NumPointsAgent(22, "22 Points Agent"),
        NumPointsAgent(23, "23 Points Agent"),
        NumPointsAgent(24, "24 Points Agent"),
        NumPointsAgent(25, "25 Points Agent"),
        NumPointsAgent(26, "26 Points Agent"),
        NumPointsAgent(27, "27 Points Agent"),
        NumPointsAgent(28, "28 Points Agent"),
        NumPointsAgent(29, "29 Points Agent"),
        NumPointsAgent(30, "30 Points Agent"),
        NumPointsAgent(31, "31 Points Agent"),
        NumPointsAgent(32, "32 Points Agent"),
        NumPointsAgent(33, "33 Points Agent"),
    ]

    wins = {agent.name: 0 for agent in available_agents}
    appearances = {agent.name: 0 for agent in available_agents}

    rng = random.Random()

    for game_num in range(num_games):
        if game_num % 1000 == 0:
            print(f"Game {game_num}")
        agents = rng.sample(available_agents, 5)

        for agent in agents:
            appearances[agent.name] += 1

        final_state = play_game(agents, rng, renderer=None)
        winner_idx = max(range(len(final_state.players)), key=lambda i: final_state.players[i].score)
        wins[agents[winner_idx].name] += 1

    results = [(name, wins[name], appearances[name]) for name in wins]
    results.sort(key=lambda x: x[1], reverse=True)

    for name, win_count, appearance_count in results:
        win_rate = win_count / appearance_count * 100
        print(f"{name:<20} {win_count:>8} {win_rate:>6.2f}%")