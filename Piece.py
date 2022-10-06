# Color: 0 = White, 1 = Black
import pygame

WHITE = 0
BLACK = 1

class Piece:
    def __init__(self, color, col, row):
        self.color = color
        self.img = ""
        self.col = col
        self.row = row
        self.selected = False
    
    def move(self, board, col, row):
        if board.has_piece(col, row):
            piece = board.get_piece(col, row)
            piece.delete(board)
        board.board[self.row][self.col] = None
        self.col = col
        self.row = row
        board.board[row][col] = self
    
    def delete(self, board):
        if self.color == WHITE:
            board.white_pieces.remove(self)
        else:
            board.black_pieces.remove(self)
        board.board[self.row][self.col] = None

    def display(self, board, screen):
        spacing = int(board.size / 8)
        img = pygame.image.load(self.img)
        img = pygame.transform.scale(img, [spacing, spacing])
        img_rect = img.get_rect()
        if self.selected:
            mouse_pos = pygame.mouse.get_pos()
            img_rect.x = mouse_pos[0] - int(spacing/2)
            img_rect.y = mouse_pos[1] - int(spacing/2)
        else:
            img_rect.x = spacing * self.col
            img_rect.y = spacing * self.row
        screen.blit(img, img_rect)

    # TO DO - false if in check, either still in check or puts into check
    def can_move_to_square(self, board, col, row):
        # if somehow out of bounds, return False
        if row < 0 or row >= 8 or col < 0 or col >= 8:
            return False
        # if same square, return False
        if row == self.row and col == self.col:
            return False
        # if occupied by another piece of the same color, return False
        if board.has_piece(col, row):
            piece = board.get_piece(col, row)
            if self.color == piece.color:
                return False
        # otherwise, return True
        return True

class Pawn(Piece):
    def __init__(self, color, col, row):
        self.color = color
        if self.color == BLACK:
            self.img = "data/Bpawn.png"
        else:
            self.img = "data/Wpawn.png"
        self.col = col
        self.row = row
        self.selected = False

class Rook(Piece):
    def __init__(self, color, col, row):
        self.color = color
        if self.color == BLACK:
            self.img = "data/Brook.png"
        else:
            self.img = "data/Wrook.png"
        self.col = col
        self.row = row
        self.selected = False
    
    def can_move_to_square(self, board, col, row):
        if not super().can_move_to_square(board, col, row):
            return False
        if self.col != col and self.row != row:
            return False
        # moving along same column
        if self.col == col:
            step = 1 if row > self.row else -1
            for n in range(self.row+step, row, step):
                if board.has_piece(col, n):
                    return False
        # moving along same row
        if self.row == row:
            step = 1 if col > self.col else -1
            for n in range(self.col+step, col, step):
                if board.has_piece(n, row):
                    return False
        return True

class Knight(Piece):
    def __init__(self, color, col, row):
        self.color = color
        if self.color == BLACK:
            self.img = "data/Bknight.png"
        else:
            self.img = "data/Wknight.png"
        self.col = col
        self.row = row
        self.selected = False

class Bishop(Piece):
    def __init__(self, color, col, row):
        self.color = color
        if self.color == BLACK:
            self.img = "data/Bbishop.png"
        else:
            self.img = "data/Wbishop.png"
        self.col = col
        self.row = row
        self.selected = False

class Queen(Piece):
    def __init__(self, color, col, row):
        self.color = color
        if self.color == BLACK:
            self.img = "data/Bqueen.png"
        else:
            self.img = "data/Wqueen.png"
        self.col = col
        self.row = row
        self.selected = False

class King(Piece):
    def __init__(self, color, col, row):
        self.color = color
        if self.color == BLACK:
            self.img = "data/Bking.png"
        else:
            self.img = "data/Wking.png"
        self.col = col
        self.row = row
        self.selected = False