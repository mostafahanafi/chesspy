import pygame
from Piece import *

WHITE = 0
BLACK = 1

class Board:
    def __init__(self, size=800):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_pieces = []
        self.black_pieces = []
        self.size = size
        self.spacing = self.size/8
        self.turn = WHITE
    
    def create_piece(self, Piece_class, color, col, row):
        piece = Piece_class(color, col, row)
        if color:
            self.black_pieces.append(piece)
        else:
            self.white_pieces.append(piece)
        self.board[piece.row][piece.col] = piece

    def initialize_board(self):
        for i in range(8):
            self.create_piece(Pawn,0,i,6)
            self.create_piece(Pawn,1,i,1)
        self.create_piece(Rook,0,0,7)
        self.create_piece(Rook,0,7,7)
        self.create_piece(Rook,1,0,0)
        self.create_piece(Rook,1,7,0)
        self.create_piece(Knight,0,1,7)
        self.create_piece(Knight,0,6,7)
        self.create_piece(Knight,1,1,0)
        self.create_piece(Knight,1,6,0)
        self.create_piece(Bishop,0,2,7)
        self.create_piece(Bishop,0,5,7)
        self.create_piece(Bishop,1,2,0)
        self.create_piece(Bishop,1,5,0)
        self.create_piece(Queen,0,3,7)
        self.create_piece(Queen,1,3,0)
        self.create_piece(King,0,4,7)
        self.create_piece(King,1,4,0)

    def has_piece(self, col, row):
        return self.board[row][col] is not None
    
    def get_piece(self, col, row):
        return self.board[row][col]

    def draw_board(self, screen):
        for row in range(8):
            for col in range(8):
                if (row+col)%2 == 0:
                    c = [227,193,111]
                else:
                    c = [184,139,74]
                rect = [col*self.spacing, row*self.spacing, self.spacing, self.spacing]
                pygame.draw.rect(screen, c, rect)
        selected_piece = None
        for row in range(8):
            for col in range(8):
                if self.has_piece(col, row):
                    piece = self.get_piece(col, row)
                    if piece.selected:
                        selected_piece = piece
                    else:
                        piece.display(self, screen)
        if selected_piece is not None:
            selected_piece.display(self, screen)
    
    def mouse_clicked(self, pos):
        col, row = int(pos[0]/self.spacing), int(pos[1]/self.spacing)
        if self.has_piece(col, row):
            piece = self.get_piece(col, row)
            if self.turn == piece.color:
                piece.selected = True
    
    def mouse_released(self, pos):
        col, row = int(pos[0]/self.spacing), int(pos[1]/self.spacing)
        selected_piece = [p for row in self.board for p in row if p is not None and p.selected]
        if len(selected_piece) == 1:
            selected_piece = selected_piece[0]
        elif len(selected_piece) == 0:
            return
        else:
            # selected > 1..... (SHOULD NOT RUN)
            print("ERROR: MORE THAN ONE SELECTED. DEBUG NECESSARY")
        if selected_piece.can_move_to_square(self, col, row):
            selected_piece.move(self, col, row)
            self.turn = WHITE if self.turn == BLACK else BLACK
        selected_piece.selected = False