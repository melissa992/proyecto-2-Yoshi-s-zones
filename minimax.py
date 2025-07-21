def minimax_decision(game, depth):
    best_value = float('-inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    for move in game.get_possible_moves(game.green_pos):
        new_game = simulate_move(game, "green", move)
        value = min_value(new_game, depth - 1, alpha, beta)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)

    return best_move

def min_value(game, depth, alpha, beta):
    if depth == 0 or game.game_over():
        return evaluate(game)

    value = float('inf')
    for move in game.get_possible_moves(game.red_pos):
        new_game = simulate_move(game, "red", move)
        value = min(value, max_value(new_game, depth - 1, alpha, beta))
        if value <= alpha:
            return value  # poda
        beta = min(beta, value)

    return value

def max_value(game, depth, alpha, beta):
    if depth == 0 or game.game_over():
        return evaluate(game)

    value = float('-inf')
    for move in game.get_possible_moves(game.green_pos):
        new_game = simulate_move(game, "green", move)
        value = max(value, min_value(new_game, depth - 1, alpha, beta))
        if value >= beta:
            return value  # poda
        alpha = max(alpha, value)

    return value

def evaluate(game):
    green_zones = game.scores["green"]
    red_zones = game.scores["red"]
    green_cells = game.cells_painted["green"]
    red_cells = game.cells_painted["red"]

    green_moves = len(game.get_possible_moves(game.green_pos))
    red_moves = len(game.get_possible_moves(game.red_pos))

    # Calcula el potencial inmediato para el control de zonas
    green_potential_zones = 0
    red_potential_zones = 0

    # Itera sobre cada zona especial para calcular su 'potencial'
    # Accede a las zonas especiales a través de la instancia del juego (game.SPECIAL_ZONES)
    # o directamente si la importaste como constante global.
    for zone in game.SPECIAL_ZONES:
        owner = game.majority_owner(zone)
        if owner == "green":
            green_potential_zones += 1 # Si ya la controla, cuenta como un potencial completo
        elif owner == "red":
            red_potential_zones += 1 # Si el oponente la controla, cuenta como potencial para él
        else: # Zona está siendo disputada o no tiene dueño mayoritario
            counts = {"green": 0, "red": 0}
            for cell in zone:
                if cell in game.painted:
                    counts[game.painted[cell]] += 1
            
            # **CAMBIO: Valorar la cercanía al control de zona**
            # Si el verde necesita 1 celda más para controlar (y el rojo no tiene la mayoría)
            if counts["green"] + 1 > len(zone) // 2 and counts["red"] <= len(zone) // 2:
                green_potential_zones += 0.5 # Bonificación por estar "a un paso" de controlar

            # Si el rojo necesita 1 celda más para controlar (y el verde no tiene la mayoría)
            if counts["red"] + 1 > len(zone) // 2 and counts["green"] <= len(zone) // 2:
                red_potential_zones += 0.5 # Penalización por permitir que el rojo esté "a un paso"

    return (
        # **CAMBIO: Aumento del peso de control de zonas completas**
        15 * (green_zones - red_zones) +      
        # **CAMBIO: Aumento significativo del peso de celdas pintadas individualmente**
        5 * (green_cells - red_cells) +       
        # **CAMBIO: Incorporación del potencial de zona**
        3 * (green_potential_zones - red_potential_zones) + 
        # Mantener peso para la movilidad
        1 * (green_moves - red_moves)         
    )

def simulate_move(game, player, move):
    import copy
    new_game = copy.deepcopy(game)
    new_game.apply_move(player, move)
    return new_game