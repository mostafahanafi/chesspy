from Board import Board
from Piece import *
import copy

class AI:
    def __init__(self, color) -> None:
        self.color = color

    def score_board(self, board: Board):
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
    
    def score_move(self, board, move):
        piece, col, row = move
        test_board = copy.deepcopy(board)
        test_piece = test_board.get_piece(piece.col, piece.row)
        test_piece.move(test_board, col, row)
        score = self.score_board(test_board)
        return score

    def choose_best_move(self, board: Board):
        moves = board.get_possible_moves()
        best_move = (moves[0], self.score_move(board, moves[0]))
        for move in moves:
            score = self.score_move(board, move)
            if self.color == WHITE:
                if score > best_move[1]:
                    best_move = (move, score)
            else:
                if score < best_move[1]:
                    best_move = (move, score)
        return best_move
