
def play_game(engine: GameEngine, policies: Sequence[Policy], seed: int | None = None):
    state = engine.reset(seed=seed)

    while not engine.is_game_over():
        actor_idx = engine.acting_player(state)
        legal = engine.legal_actions(state)

        if legal:
            action = policies[actor_idx](state, actor_idx, legal)
        else:
            action = None # auto-resolved phase
        state = engine.step(state, action)

    return build_result(state)