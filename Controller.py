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

        best_move = AI.find_best_move(self.board, depth)
        piece, col, row = best_move[0]
        if piece.can_move_to_square(self.board, col, row): # should always be true
            piece.move(self.board, col, row)
        self.board.draw_board(screen)
        pygame.display.flip()
        self.change_turn()
    
    def display_winner(self, color, method, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"{color} wins by {method}!", True, (255,255,255))
        textbox = text.get_rect(center=(self.board.size/2, self.board.size/2))
        text_background = pygame.Surface((textbox.width, textbox.height))
        text_background.fill((0, 0, 255)) 

        screen.blit(text_background, textbox)
        screen.blit(text, textbox)
        pygame.display.flip()
        pygame.time.wait(3000)

    def game_loop(self):
        screen = pygame.display.set_mode([self.board.size,self.board.size])
        white_king = [piece for piece in self.board.white_pieces if isinstance(piece, King)][0]
        black_king = [piece for piece in self.board.black_pieces if isinstance(piece, King)][0]

        while not white_king.is_in_checkmate(self.board):
            # White's turn
            if self.board.turn == WHITE:
                if self.board.white_AI:
                    self.ai_turn(WHITE, screen, depth=3)
                else:
                    self.player_turn(screen)
            # Black's turn
            elif not black_king.is_in_checkmate(self.board):
                if self.board.black_AI:
                    self.ai_turn(BLACK, screen, depth=3)
                else:
                    self.player_turn(screen)
            else:
                # Black is in checkmate, White WINS!
                self.display_winner("White", "checkmate", screen)
                return

        # White is in checkmate, Black WINS!
        self.display_winner("Black", "checkmate", screen)