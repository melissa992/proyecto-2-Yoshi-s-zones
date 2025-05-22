import pygame
from game import Game
from ui import GameUI, show_menu

pygame.init()

def main():
    depth = show_menu()
    game = Game(depth)
    ui = GameUI(game)
    ui.run()

if __name__ == "__main__":
    main()
