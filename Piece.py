# Color: 0 = White, 1 = Black
import pygame
import copy

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

    def can_move_to_square(self, board, col, row):
        return (col,row) in self.validate_moves(board, self.get_legal_moves(board))
    
    def validate_moves(self, board, moves):
        # check that moves do not put (or keep) king in check
        for move in moves.copy():
            next_board = copy.deepcopy(board)
            next_pieces = next_board.white_pieces if self.color == WHITE else next_board.black_pieces
            next_piece = next_board.get_piece(self.col, self.row)
            next_piece.move(next_board, move[0], move[1])
            for k in next_pieces:
                if isinstance(k, King) and k.is_in_check(next_board):
                    moves.remove(move)
        return moves

    def get_legal_moves(self, board):
        return []

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
        self.en_passant = False
    
    def move(self, board, col, row):
        # if you've reached end of board, auto promote to queen
        end_of_board = 0 if self.color == WHITE else 7
        if row == end_of_board:
            queen = Queen(self.color, self.col, self.row)
            self.delete(board)
            board.add_piece(queen)
            return queen.move(board, col, row)
        else:
            self.en_passant = abs(row - self.row) == 2
            # if taking pawn en passant, make sure to capture it
            if (col == self.col+1 or col == self.col - 1):
                if board.has_piece(col, self.row):
                    piece = board.get_piece(col, self.row)
                    if isinstance(piece, Pawn) and piece.en_passant:
                        piece.delete(board)
            return super().move(board, col, row)
    
    def get_legal_moves(self, board):
        moves = []
        step = -1 if self.color == WHITE else 1
        home_row = 6 if self.color == WHITE else 1
        # one step forward
        if not board.has_piece(self.col, self.row+step):
            moves.append( (self.col, self.row+step) )
        # if hasn't moved, two steps forward
            if self.row == home_row and not board.has_piece(self.col, self.row+2*step):
                moves.append( (self.col, self.row+2*step) )
        # if opponent piece diagonal to it, diagonal move
        if board.has_piece(self.col-1, self.row+step):
            piece = board.get_piece(self.col-1, self.row+step)
            if self.color != piece.color:
                moves.append( (self.col-1, self.row+step) )
        if board.has_piece(self.col+1, self.row+step):
            piece = board.get_piece(self.col+1, self.row+step)
            if self.color != piece.color:
                moves.append( (self.col+1, self.row+step) )
        # if en passant pawn adjacent, diagonal move
        if board.has_piece(self.col-1, self.row+step):
            piece = board.has_piece(self.col-1, self.row+step)
            if isinstance(piece, Pawn) and piece.en_passant:
                moves.append( (self.col-1, self.row+step) )
        if board.has_piece(self.col+1, self.row+step):
            piece = board.has_piece(self.col+1, self.row+step)
            if isinstance(piece, Pawn) and piece.en_passant:
                moves.append( (self.col+1, self.row+step) )
        # return move list
        return moves


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

    def get_legal_moves(self, board):
        moves = []
        # check left until hitting end of board or piece
        c = self.col-1
        while c >= 0:
            if board.has_piece(c, self.row):
                piece = board.get_piece(c, self.row)
                if piece.color != self.color:
                    moves.append( (c, self.row) )
                break
            else:
                moves.append( (c, self.row) )
                c -= 1
        # check right
        c = self.col+1
        while c < 8:
            if board.has_piece(c, self.row):
                piece = board.get_piece(c, self.row)
                if piece.color != self.color:
                    moves.append( (c, self.row) )
                break
            else:
                moves.append( (c, self.row) )
                c += 1
        # check up
        r = self.row-1
        while r >= 0:
            if board.has_piece(self.col, r):
                piece = board.get_piece(self.col, r)
                if piece.color != self.color:
                    moves.append( (self.col, r) )
                break
            else:
                moves.append( (self.col, r) )
                r -= 1
        # check down
        r = self.row+1
        while r < 8:
            if board.has_piece(self.col, r):
                piece = board.get_piece(self.col, r)
                if piece.color != self.color:
                    moves.append( (self.col, r) )
                break
            else:
                moves.append( (self.col, r) )
                r += 1
        # return move list
        return moves


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
    
    def get_legal_moves(self, board):
        moves = []
        moves.append( (self.col+1, self.row+2) )
        moves.append( (self.col-1, self.row+2) )
        moves.append( (self.col+1, self.row-2) )
        moves.append( (self.col-1, self.row-2) )
        moves.append( (self.col+2, self.row+1) )
        moves.append( (self.col+2, self.row-1) )
        moves.append( (self.col-2, self.row+1) )
        moves.append( (self.col-2, self.row-1) )
        for move in moves.copy():
            if move[0] < 0 or move[0] >= 8 or move[1] < 0 or move[1] >= 8:
                moves.remove(move)
            elif board.has_piece(move[0], move[1]):
                piece = board.get_piece(move[0], move[1])
                if piece.color == self.color:
                    moves.remove(move)
        return moves


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
    
    def get_legal_moves(self, board):
        moves = []
        # check up&left diagonal until hitting end of board or piece
        c = self.col-1
        r = self.row-1
        while c >= 0 and r >= 0:
            if board.has_piece(c, r):
                piece = board.get_piece(c, r)
                if piece.color != self.color:
                    moves.append( (c, r) )
                break
            else:
                moves.append( (c, r) )
                c -= 1
                r -= 1
        # check down&right
        c = self.col+1
        r = self.row+1
        while c < 8 and r < 8:
            if board.has_piece(c, r):
                piece = board.get_piece(c, r)
                if piece.color != self.color:
                    moves.append( (c, r) )
                break
            else:
                moves.append( (c, r) )
                c += 1
                r += 1
        # check up&right
        c = self.col+1
        r = self.row-1
        while r >= 0 and c < 8:
            if board.has_piece(c, r):
                piece = board.get_piece(c, r)
                if piece.color != self.color:
                    moves.append( (c, r) )
                break
            else:
                moves.append( (c, r) )
                c += 1
                r -= 1
        # check down&left
        c = self.col-1
        r = self.row+1
        while r < 8 and c >= 0:
            if board.has_piece(c, r):
                piece = board.get_piece(c, r)
                if piece.color != self.color:
                    moves.append( (c, r) )
                break
            else:
                moves.append( (c, r) )
                c -= 1
                r += 1
        # return move list
        return moves


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

    def get_legal_moves(self, board):
        B_moves = Bishop(self.color, self.col, self.row).get_legal_moves(board)
        R_moves = Rook(self.color, self.col, self.row).get_legal_moves(board)
        return B_moves + R_moves


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
        if col - self.col == 2 and row == self.row:
            k_rook = board.get_piece(7, row)
            k_rook.move(board, col-1, row)
        elif self.col - col == 2 and row == self.row:
            print(self.col, self.row, col, row)
            q_rook = board.get_piece(0, row)
            q_rook.move(board, col+1, row)
        return super().move(board, col, row)
    
    def get_legal_moves(self, board):
        moves = []
        # 1 move around the king
        for c in [self.col-1,self.col,self.col+1]:
            for r in [self.row-1,self.row,self.row+1]:
                moves.append( (c,r) )
        moves.remove( (self.col, self.row) )
        for move in moves.copy():
            if move[0] < 0 or move[0] >= 8 or move[1] < 0 or move[1] >= 8:
                moves.remove(move)
            elif board.has_piece(move[0], move[1]):
                piece = board.get_piece(move[0], move[1])
                if piece.color == self.color:
                    moves.remove(move)
        # castling
        if not self.has_moved:
            # kingside castling
            if board.has_piece(7, self.row):
                k_rook = board.get_piece(7, self.row)
                if isinstance(k_rook, Rook):
                    k_rook = board.get_piece(7, self.row)
                    if not k_rook.has_moved:
                        if not (board.has_piece(self.col+1, self.row) or board.has_piece(self.col+2, self.row)):
                            moves.append( (self.col+2, self.row) )
            # queenside castling
            if board.has_piece(0, self.row):
                q_rook = board.get_piece(0, self.row)
                if isinstance(q_rook, Rook):
                    q_rook = board.get_piece(0, self.row)
                    if not q_rook.has_moved:
                        if not (board.has_piece(self.col-1, self.row) or 
                        board.has_piece(self.col-2, self.row) or
                        board.has_piece(self.col-3, self.row)):
                            moves.append( (self.col-2, self.row) )
        return moves

    def is_in_check(self, board):
        pieces = board.white_pieces if self.color == BLACK else board.black_pieces
        for piece in pieces:
            moves = piece.get_legal_moves(board)
            if (self.col, self.row) in moves:
                return True
        return False
    
    def is_in_checkmate(self, board):
        if not self.is_in_check(board):
            return False
        pieces = board.white_pieces if self.color == WHITE else board.black_pieces
        for piece in pieces:
            moves = piece.get_legal_moves(board)
            if len(moves) > 0:
                return False
        return True