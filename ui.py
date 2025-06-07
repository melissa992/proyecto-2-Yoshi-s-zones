import pygame

CELL_SIZE = 80
WIDTH = HEIGHT = CELL_SIZE * 8
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
YELLOW = (255, 255, 0)

# Zonas especiales en formato (fila, columna) = (y, x)
SPECIAL_ZONES = [
    [(0,0), (1,0), (2,0), (0,1), (0,2)],  # superior izquierda
    [(0,7), (0,6), (0,5), (1,7), (2,7)],  # superior derecha
    [(7,0), (6,0), (5,0), (7,1), (7,2)],  # inferior izquierda
    [(7,7), (6,7), (5,7), (7,6), (7,5)]   # inferior derecha
]

class GameUI:
    def __init__(self, game):
        #Imagenes de los jugadores
        self.green_img = pygame.image.load("imagenes/green_yoshi.png").convert_alpha()
        self.red_img = pygame.image.load("imagenes/red_yoshi.png").convert_alpha()
        self.green_img = pygame.transform.scale(self.green_img, (CELL_SIZE, CELL_SIZE))
        self.red_img = pygame.transform.scale(self.red_img, (CELL_SIZE, CELL_SIZE))

        self.game = game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 40))
        pygame.display.set_caption("Yoshi's Zones")
        self.clock = pygame.time.Clock()

    def draw_board(self):
        #Pintar fondo del tablero
        self.screen.fill(WHITE)

        for x in range(8):
            for y in range(8):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = GRAY if (x + y) % 2 == 0 else WHITE
                pygame.draw.rect(self.screen, color, rect)

                # Dibujar borde negro en zonas especiales
                for zone in SPECIAL_ZONES:
                    if (y, x) in zone:
                        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)
                        break

                # Pintar celdas pintadas si las hay
                if (x, y) in self.game.painted:
                    color = GREEN if self.game.painted[(x, y)] == "green" else RED
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)

        # Dibujar piezas de los jugadores
            #gx, gy = self.game.green_pos
            #pygame.draw.circle(self.screen, GREEN, (gx*CELL_SIZE + 40, gy*CELL_SIZE + 40), 20)
            #rx, ry = self.game.red_pos
            #pygame.draw.circle(self.screen, RED, (rx*CELL_SIZE + 40, ry*CELL_SIZE + 40), 20)

        #Dibujar imágenes de los jugadores
        gx, gy = self.game.green_pos
        rx, ry = self.game.red_pos
        self.screen.blit(self.green_img, (gx * CELL_SIZE, gy * CELL_SIZE))
        self.screen.blit(self.red_img, (rx * CELL_SIZE, ry * CELL_SIZE))

        font = pygame.font.SysFont(None, 24)
        score_text = (
        f"Zonas Green: {self.game.scores['green']} | Zonas Red: {self.game.scores['red']} | "
        f"Celdas Green: {self.game.cells_painted['green']} | Celdas Red: {self.game.cells_painted['red']}"
       )
        text = font.render(score_text, True, (0, 0, 0))
        self.screen.blit(text, (10, HEIGHT + 10))

    def run(self):
        running = True
        while running:
            self.clock.tick(30)
            if self.game.turn == "green" and not self.game.game_over():
                self.game.ai_turn()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and self.game.turn == "red":
                    x, y = pygame.mouse.get_pos()
                    gx, gy = x // CELL_SIZE, y // CELL_SIZE
                    if (gx, gy) in self.game.get_possible_moves(self.game.red_pos):
                        self.game.apply_move("red", (gx, gy))
                        self.game.turn = "green"

            self.draw_board()
            if self.game.game_over():
                winner = self.game.get_winner()
                font = pygame.font.SysFont(None, 48)
                msg = f"¡Gana {winner}!" if winner != "draw" else "¡Empate!"
                text = font.render(msg, True, (0, 0, 0))
                self.screen.blit(text, (200, HEIGHT // 2))
            pygame.display.flip()
        pygame.quit()

def show_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Selecciona Dificultad")
    font = pygame.font.SysFont(None, 36)
    options = [("Principiante", 2), ("Amateur", 4), ("Experto", 6)]
    buttons = []
    
    #Cargar imagen de fondo
    bg = pygame.image.load("imagenes/fondo_menu.jpg").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    for i, (label, _) in enumerate(options):
        rect = pygame.Rect(WIDTH//4, 100 + i*100, WIDTH//2, 50)
        buttons.append((rect, label))

    while True:
        #screen.fill(WHITE)
        screen.blit(bg, (0, 0))  # Dibuja el fondo
        for i, (rect, label) in enumerate(buttons):
            pygame.draw.rect(screen, GRAY, rect)
            text = font.render(label, True, (0, 0, 0))
            screen.blit(text, (rect.x + 20, rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for i, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(mx, my):
                        return options[i][1]

        pygame.display.flip()
