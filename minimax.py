def minimax_decision(game, depth):
    best_value = float('-inf')
    best_move = None
    for move in game.get_possible_moves(game.green_pos):
        new_game = simulate_move(game, "green", move)
        value = min_value(new_game, depth - 1)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move

def min_value(game, depth):
    if depth == 0 or game.game_over():
        return evaluate(game)
    value = float('inf')
    for move in game.get_possible_moves(game.red_pos):
        new_game = simulate_move(game, "red", move)
        value = min(value, max_value(new_game, depth - 1))
    return value

def max_value(game, depth):
    if depth == 0 or game.game_over():
        return evaluate(game)
    value = float('-inf')
    for move in game.get_possible_moves(game.green_pos):
        new_game = simulate_move(game, "green", move)
        value = max(value, min_value(new_game, depth - 1))
    return value

def evaluate(game):
    return game.scores["green"] - game.scores["red"]

def simulate_move(game, player, move):
    import copy
    new_game = copy.deepcopy(game)
    new_game.apply_move(player, move)
    return new_game