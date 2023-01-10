import pygame
from Piece import *
from Board import Board
from Controller import Controller

# constants to be assigned easily later
PLAYER = 0
AI = 1

# customizable settings
SIZE = 800
WHITE = PLAYER
BLACK = AI

pygame.init()
screen = pygame.display.set_mode([SIZE,SIZE])
if __name__ == "__main__":
    board = Board(WHITE, BLACK, size=SIZE)
    board.initialize_board()
    controller = Controller(board)
    controller.game_loop()