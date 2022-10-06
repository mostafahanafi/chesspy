import sys
import pygame
from Piece import *
from Board import Board
pygame.init()

SIZE = 600
screen = pygame.display.set_mode([SIZE,SIZE])

board = Board(size=SIZE)
board.initialize_board()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            board.mouse_clicked(pos)
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            board.mouse_released(pos)
    board.draw_board(screen)
    pygame.display.flip()