import pygame
from game import Game
from ui import GameUI, show_menu

pygame.init()

def main():
    while True:
        depth = show_menu()
        game = Game(depth)
        ui = GameUI(game)
        should_restart = ui.run()
        if not should_restart:
            break  # salir del programa si no se desea reiniciar

if __name__ == "__main__":
    main()
