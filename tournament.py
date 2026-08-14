import random

from agents.ev_agent import EVAgent
from agents.num_cards_agent import NumCardsAgent
from agents.num_points_agent import NumPointsAgent
from agents.prob_threshold_agent import ProbThresholdAgent
from agents.random_agent import RandomAgent
from game.logic.game_loop import play_game


def run_tournament():
    num_games = 1_000_000
    '''available_agents = [
        ProbThresholdAgent(threshold=0.05, name="Prob Threshold Agent 0.05"),
        ProbThresholdAgent(threshold=0.10, name="Prob Threshold Agent 0.10"),
        ProbThresholdAgent(threshold=0.15, name="Prob Threshold Agent 0.15"),
        ProbThresholdAgent(threshold=0.20, name="Prob Threshold Agent 0.20"),
        ProbThresholdAgent(threshold=0.25, name="Prob Threshold Agent 0.25"),
        ProbThresholdAgent(threshold=0.30, name="Prob Threshold Agent 0.30"),
        ProbThresholdAgent(threshold=0.35, name="Prob Threshold Agent 0.35"),
        ProbThresholdAgent(threshold=0.40, name="Prob Threshold Agent 0.40"),
        ProbThresholdAgent(threshold=0.45, name="Prob Threshold Agent 0.45"),
        ProbThresholdAgent(threshold=0.50, name="Prob Threshold Agent 0.50"),
        ProbThresholdAgent(threshold=0.55, name="Prob Threshold Agent 0.55"),
        ProbThresholdAgent(threshold=0.60, name="Prob Threshold Agent 0.60"),
        ProbThresholdAgent(threshold=0.65, name="Prob Threshold Agent 0.65"),
        ProbThresholdAgent(threshold=0.70, name="Prob Threshold Agent 0.70"),
        ProbThresholdAgent(threshold=0.75, name="Prob Threshold Agent 0.75"),
        ProbThresholdAgent(threshold=0.80, name="Prob Threshold Agent 0.80"),
        ProbThresholdAgent(threshold=0.85, name="Prob Threshold Agent 0.85"),
        ProbThresholdAgent(threshold=0.90, name="Prob Threshold Agent 0.90"),
        ProbThresholdAgent(threshold=0.95, name="Prob Threshold Agent 0.95"),
        ProbThresholdAgent(threshold=0.100, name="Prob Threshold Agent 1.00"),

    ]'''
    available_agents = [
        EVAgent("EV Agent"),
        RandomAgent(rng=random.Random(), name="Random Agent"),
        NumCardsAgent(4, "4 Cards Agent"),
        ProbThresholdAgent(0.25, "0.25 Prob Agent"),
        NumPointsAgent(30, "30 Points Agent"),
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
        print(f"{name:<20}  ({win_count:>8} / {appearance_count} ) {win_rate:>6.2f}%")