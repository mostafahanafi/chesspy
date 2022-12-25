import sys
import pygame
from Piece import *
from Board import Board
from Controller import Controller

pygame.init()

SIZE = 800
screen = pygame.display.set_mode([SIZE,SIZE])

if __name__ == "__main__":
    board = Board(size=SIZE)
    board.initialize_board()
    controller = Controller(board)
    controller.game_loop()