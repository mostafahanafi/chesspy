from Board import Board
from Piece import *
import copy
import random

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

    def minimax(self, board, depth):
        if board.turn == WHITE:
            best_move = (None, float("-inf"))
            for move in board.get_possible_moves():
                score = self.minimax_move(board, move, depth)
                if score > best_move[1]:
                    best_move = (move, score)
            return best_move
        else:
            best_move = (None, float("inf"))
            for move in board.get_possible_moves():
                score = self.minimax_move(board, move, depth)
                if score < best_move[1]:
                    best_move = (move, score)
            return best_move

    def minimax_move(self, board, move, depth):
        test_board = copy.deepcopy(board)
        test_piece = test_board.get_piece(move[0].col, move[0].row)
        test_piece.move(test_board, move[1], move[2])
        test_board.change_turn()
        depth -= 1

        if depth == 0:
            return self.score_board(test_board)
        else:
            next_moves = test_board.get_possible_moves()
            if test_board.turn == WHITE:
                return max(self.minimax_move(test_board, next_move, depth) \
                    for next_move in next_moves)
            else:
                return min(self.minimax_move(test_board, next_move, depth) \
                    for next_move in next_moves)

class RandomAI(AI):
    def minimax(self, board, depth):
        return (random.choice(board.get_possible_moves()), random.random())