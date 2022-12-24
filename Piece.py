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
    
    def can_move_to_square(self, board, col, row):
        if not super().can_move_to_square(board, col, row):
            return False
        # set step/direction and home row for different colors
        step = -1 if self.color == WHITE else 1
        home_row = 6 if self.color == WHITE else 1
        # basic movement (1 step, 2 if on home row)
        if col == self.col and not board.has_piece(col, row):
            if row == self.row + step:
                return True
            elif self.row == home_row and row == self.row + 2*step and not board.has_piece(self.col,self.row+step):
                return True
        # capturing
        elif (col == self.col+1 or col == self.col-1) and row == self.row + step and board.has_piece(col, row):
            piece = board.get_piece(col, row)
            return self.color != piece.color
        # TO DO - en passant?
        # TO DO - don't forget pawn promotion
        return False

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
        self.has_moved = False
    
    def move(self, board, col, row):
        self.has_moved = True
        return super().move(board, col, row)

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
    
    def can_move_to_square(self, board, col, row):
        if not super().can_move_to_square(board, col, row):
            return False
        # test if square is one of 8 possible squares a knight can jump to manually
        return ((row == self.row + 2 and (col == self.col + 1 or col == self.col - 1)) or
            (row == self.row - 2 and (col == self.col + 1 or col == self.col - 1)) or
            (col == self.col + 2 and (row == self.row + 1 or row == self.row - 1)) or
            (col == self.col - 2 and (row == self.row + 1 or row == self.row - 1)))

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
    
    def can_move_to_square(self, board, col, row):
        if not super().can_move_to_square(board, col, row):
            return False
        # make sure it is a diagonal move i.e. movement in col = movement in row
        col_dist = abs(col - self.col)
        row_dist = abs(row - self.row)
        if row_dist != col_dist:
            return False

        col_step = 1 if col > self.col else -1
        row_step = 1 if row > self.row else -1
        for i in range(1, row_dist): 
            c = self.col + i*col_step
            r = self.row + i*row_step
            if board.has_piece(c, r):
                    return False
        
        return True

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
    
    def can_move_to_square(self, board, col, row):
        if not super().can_move_to_square(board, col, row):
            return False
        # if a bishop or a rook can move there, the queen can move there
        B = Bishop(self.color, self.col, self.row)
        R = Rook(self.color, self.col, self.row)
        return B.can_move_to_square(board, col, row) or R.can_move_to_square(board, col, row)

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
        self.has_moved = False
    
    def move(self, board, col, row):
        self.has_moved = True
        # if castling, also move the rook
        if col - self.col == 2:
            k_rook = board.get_piece(7, row)
            k_rook.move(board, col-1, row)
        elif self.col - col == 2:
            q_rook = board.get_piece(0, row)
            q_rook.move(board, col+1, row)
        return super().move(board, col, row)

    def can_move_to_square(self, board, col, row):
        if not super().can_move_to_square(board, col, row):
            return False
        # 1 step in any direction
        if abs(col-self.col) <= 1 and abs(row-self.row) <= 1:
            return True
        # TO-DO: castling
        if not self.has_moved and self.row == row:
            # kingside castling
            if col == self.col + 2:
                k_rook = board.get_piece(7, row)
                if k_rook.has_moved:
                    return False
                if board.has_piece(self.col+1, row) or board.has_piece(self.col+2, row):
                    return False
                else:
                    return True
            # queenside castling
            elif col == self.col - 2:
                q_rook = board.get_piece(0, row)
                if q_rook.has_moved:
                    return False
                if board.has_piece(self.col-1, row) or board.has_piece(self.col-2, row):
                    return False
                else:
                    return True
        return False