import random
from minimax import minimax_decision

BOARD_SIZE = 8
# Zonas especiales en formato (fila, columna) = (y, x)
SPECIAL_ZONES = [
    [(0,0), (1,0), (2,0), (0,1), (0,2)],  # superior izquierda
    [(0,7), (0,6), (0,5), (1,7), (2,7)],  # superior derecha
    [(7,0), (6,0), (5,0), (7,1), (7,2)],  # inferior izquierda
    [(7,7), (6,7), (5,7), (7,6), (7,5)]   # inferior derecha
]

class Game:
    def __init__(self, depth):
        #Se agrega el atributo SPECIAL_ZONES para ser usado en minimax.py
        self.SPECIAL_ZONES = SPECIAL_ZONES      
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.painted = {}
        self.depth = depth
        #self.turn = "green"
        self.turn = "red"
        self.scores = {"green": 0, "red": 0}
        self.green_pos = self.random_start()
        self.red_pos = self.random_start(exclude=[self.green_pos])
        self.cells_painted = {"green": 0, "red": 0}  # NUEVO: celdas pintadas


    def random_start(self, exclude=[]):
        while True:
            pos = (random.randint(0,7), random.randint(0,7))
            if not any(pos in zone for zone in SPECIAL_ZONES) and pos not in exclude:
                return pos

    def get_possible_moves(self, pos):
        moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
        result = []
        for dx, dy in moves:
            nx, ny = pos[0] + dx, pos[1] + dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                if (nx, ny) not in self.painted:
                    result.append((nx, ny))
        return result

    def paint_zone(self, player, pos):
        for zone in SPECIAL_ZONES:
            if pos in zone:
                self.painted[pos] = player
                counts = {"green": 0, "red": 0}
                for cell in zone:
                    if cell in self.painted:
                        counts[self.painted[cell]] += 1
                if counts[player] > len(zone) // 2:
                    self.scores[player] = sum(1 for z in SPECIAL_ZONES if self.majority_owner(z) == player)

    def majority_owner(self, zone):
        counts = {"green": 0, "red": 0}
        for cell in zone:
            if cell in self.painted:
                counts[self.painted[cell]] += 1
        if counts["green"] > len(zone) // 2:
            return "green"
        elif counts["red"] > len(zone) // 2:
            return "red"
        return None

    def apply_move(self, player, move):
        if player == "green":
            self.green_pos = move
        else:
            self.red_pos = move
        if move not in self.painted and any(move in zone for zone in SPECIAL_ZONES):
                self.painted[move] = player
                self.cells_painted[player] += 1 
        self.paint_zone(player, move)

    def game_over(self):
        all_painted = all(
            all(cell in self.painted for cell in zone)
            for zone in SPECIAL_ZONES
        )
        return all_painted

    def get_winner(self):
        if self.scores["green"] > self.scores["red"]:
            return "green"
        elif self.scores["green"] < self.scores["red"]:
            return "red"
        return "draw"

    def ai_turn(self):
        move = minimax_decision(self, self.depth)
        self.apply_move("green", move)
        self.turn = "red"