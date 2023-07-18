import pygame
from Piece import *

WHITE = 0
BLACK = 1
PLAYER = 0
AI = 1

class Board:
    def __init__(self, white, black, size=800):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_pieces = []
        self.black_pieces = []
        self.size = size
        self.spacing = self.size/8
        self.white_AI = (white == AI)
        self.black_AI = (black == AI)
        self.turn = WHITE
    
    def change_turn(self):
        self.turn = WHITE if self.turn == BLACK else BLACK

    def create_piece(self, Piece_class, color, col, row):
        piece = Piece_class(color, col, row)
        self.add_piece(piece)
    
    def add_piece(self, piece):
        if piece.color:
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
        if col < 0 or col >= 8 or row < 0 or row >= 8:
            return False
        return self.board[row][col] is not None
    
    def get_piece(self, col, row):
        return self.board[row][col]

    def draw_board(self, screen):
        # find selected piece
        selected_piece = None
        for piece in self.black_pieces + self.white_pieces:
            if piece.selected:
                selected_piece = piece
                break
        # moves selected piece can make
        if selected_piece is not None:
            moves = selected_piece.get_legal_moves(self)
            valid_moves = selected_piece.validate_moves(self, moves)
        # draw chessboard
        for row in range(8):
            for col in range(8):
                if (row+col)%2 == 0:
                    c = [238,237,210]
                else:
                    c = [117,150,86]
                rect = [col*self.spacing, row*self.spacing, self.spacing, self.spacing]
                pygame.draw.rect(screen, c, rect)
                
                if selected_piece is not None:
                    # if selected piece can move, highlight possible moves
                    if (col, row) in valid_moves:
                        if self.has_piece(col,row):
                            pygame.draw.circle(screen,
                                        (100,100,100), 
                                        [(col+.5)*self.spacing, (row+.5)*self.spacing],
                                        self.spacing/2,
                                        width=int(self.spacing/20))
                        else:
                            pygame.draw.circle(screen,
                                        (100,100,100), 
                                        [(col+.5)*self.spacing, (row+.5)*self.spacing],
                                        self.spacing/8)
                # display pieces
                piece = self.board[row][col]
                if piece is not None:
                    if isinstance(piece, King):
                        if piece.is_in_checkmate(self):
                            c = [170,255,170]
                        elif piece.is_in_check(self):
                            c = [255,170,170]
                        rect = [col*self.spacing, row*self.spacing, self.spacing, self.spacing]
                        pygame.draw.rect(screen, c, rect)
                    piece.display(self, screen)
        # display selected piece on top
        if selected_piece is not None:
            row = selected_piece.row
            col = selected_piece.col
            if (row+col)%2 == 0:
                c = [247,246,134]
            else:
                c = [185,202,65]
            rect = [col*self.spacing, row*self.spacing, self.spacing, self.spacing]
            pygame.draw.rect(screen, c, rect)
            selected_piece.display(self, screen)
        pygame.display.flip()

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
            return False
        else:
            # selected > 1..... (SHOULD NOT RUN)
            print("ERROR: MORE THAN ONE SELECTED. DEBUG NECESSARY")
        if selected_piece.can_move_to_square(self, col, row):
            selected_piece.move(self, col, row)
            self.change_turn()
            selected_piece.selected = False
            return True
        selected_piece.selected = False
        return False
    
    def get_possible_moves(self):
        pieces = self.white_pieces if self.turn == WHITE else self.black_pieces
        valid_moves = []
        for piece in pieces:
            moves = piece.get_legal_moves(self)
            for move in piece.validate_moves(self, moves):
                valid_moves.append( (piece,move[0],move[1]) )
        return valid_moves
    
    def from_FEN(self, fen_str):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        fen_parts = fen_str.split(" ")

        # 1. Piece placement
        piece_placements = fen_parts[0]
        for row, row_placement in enumerate(piece_placements.split("/")):
            col = 0
            for piece_placement in row_placement:
                if piece_placement.isnumeric():
                    col += int(piece_placement)
                else:
                    color = BLACK if piece_placement.islower() else WHITE
                    piece_placement = piece_placement.lower()
                    match piece_placement:
                        case "r":
                            self.create_piece(Rook, color, col, row)
                        case "n":
                            self.create_piece(Knight, color, col, row)
                        case "b":
                            self.create_piece(Bishop, color, col, row)
                        case "k":
                            self.create_piece(King, color, col, row)
                        case "q":
                            self.create_piece(Queen, color, col, row)
                        case "p":
                            self.create_piece(Pawn, color, col, row)
                        case _:
                            raise ValueError
                    col += 1

        # 2. Active color (turn)
        turn = fen_parts[1]
        self.turn = WHITE if turn == 'w' else BLACK

        # 3. Castling rights
        castling_rights = fen_parts[2]
        white_king = [piece for piece in self.white_pieces if isinstance(piece, King)][0]
        black_king = [piece for piece in self.white_pieces if isinstance(piece, King)][0]
        white_rooks = [piece for piece in self.white_pieces if isinstance(piece, Rook)]
        black_rooks = [piece for piece in self.black_pieces if isinstance(piece, Rook)]
        
        if castling_rights == '-':
            white_king.has_moved = True
            black_king.has_moved = True
        else:
            if len(white_rooks) == 2:
                if 'K' in castling_rights and 'Q' not in castling_rights:
                    if white_rooks[0].col == 7 and white_rooks[0].row == 7:
                        white_rooks[1].has_moved = True
                    else:
                        white_rooks[0].has_moved = True
                elif 'Q' in castling_rights and 'K' not in castling_rights:
                    if white_rooks[0].col == 0 and white_rooks[0].row == 7:
                        white_rooks[1].has_moved = True
                    else:
                        white_rooks[0].has_moved = True
            
            if len(black_rooks) == 2:
                if 'k' in castling_rights and 'q' not in castling_rights:
                    if black_rooks[0].col == 7 and black_rooks[0].row == 0:
                        black_rooks[1].has_moved = True
                    else:
                        black_rooks[0].has_moved = True
                if 'q' in castling_rights and 'k' not in castling_rights:
                    if black_rooks[0].col == 0 and black_rooks[0].row == 0:
                        black_rooks[1].has_moved = True
                    else:
                        black_rooks[0].has_moved = True
        
        # 4. En passant targets
        en_passant_square = fen_parts[3]
        if en_passant_square != "-":
            file = en_passant_square[0]
            rank = int(en_passant_square[1])

            row = 8 - rank
            col = 'abcdefgh'.index(file)

            if row == 2:
                pawn = self.get_piece(col, row+1)
            elif row == 5:
                pawn = self.get_piece(col, row-1)
            pawn.en_passant = True
        
        # 5. Halfmove clock
        # TODO:

        # 6. Fullmove number
        # TODO: