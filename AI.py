from Board import Board
from Piece import *
import copy

class AI:
    def __init__(self) -> None:
        pass

    def score(self, board: Board):
        total = 0
        scores = {
            "King": 0, # will always be in the array
            "Pawn": 1,
            "Bishop": 3,
            "Knight": 3,
            "Rook": 5,
            "Queen": 9
        }

        for piece in board.white_pieces + board.black_pieces:
            piece_type = piece.__class__.__name__
            mult = 1 if piece.color == WHITE else -1

            total += mult*scores[f"{piece_type}"]
            if (piece.row == 3 or piece.row == 4) and (piece.col == 3 or piece.col == 4):
                total += mult*2 # piece in center of board
            elif (piece.row >= 2 and piece.row <= 5) and (piece.col >= 2 and piece.col <= 5):
                total += mult # piece near center of board   
        
        return total
    
    def choose_best_move(self, board: Board):
        moves = board.get_possible_moves()
        best_move = (None, 0)
        for move in moves:
            test_board = copy.deepcopy(board)
            piece = test_board.get_piece(move[0].col, move[0].row)
            piece.move(test_board, move[1], move[2])
            score = self.score(test_board)
            if score > best_move[1]:
                best_move = (move, score)
        return best_move
