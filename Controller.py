import pygame
import sys
from Board import BLACK, WHITE
from AI import *

class Controller:
    def __init__(self, board) -> None:
        self.board = board
        if self.board.white_AI:
            self.white_AI = AI(WHITE)
        if self.board.black_AI:
            self.black_AI = AI(BLACK)
    
    def change_turn(self):
        self.board.change_turn()

    def player_turn(self, screen):
        move_made = False
        while not move_made:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.board.mouse_clicked(pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    move_made = self.board.mouse_released(pos)
            self.board.draw_board(screen)
            pygame.display.flip()
    
    def ai_turn(self, color, screen, depth=1):
        self.board.draw_board(screen)
        pygame.display.flip()
        if color == WHITE:
            AI = self.white_AI
        else:
            AI = self.black_AI
        
        best_move = AI.minimax(self.board, depth)
        piece, col, row = best_move[0]
        if piece.can_move_to_square(self.board, col, row): # should be true
            piece.move(self.board, col, row)
        print(best_move[1]) # score
        self.board.draw_board(screen)
        pygame.display.flip()
        self.change_turn()
    
    def game_loop(self):
        screen = pygame.display.set_mode([self.board.size,self.board.size])
        while True:
            if self.board.white_AI:
                self.ai_turn(WHITE, screen, depth=3)
            else:
                self.player_turn(screen)
            if self.board.black_AI:
                self.ai_turn(BLACK, screen, depth=3)
            else:
                self.player_turn(screen)