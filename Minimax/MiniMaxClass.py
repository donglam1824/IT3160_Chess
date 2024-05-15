from copy import deepcopy
from Base.ChessBoardClass import ChessBoard
from Minimax.BlackMax import BlackMax
from Minimax.WhiteMax import WhiteMax


class Minimax:
    def __init__(self, maxing_player):
        if(maxing_player == "White"): self.miniMaxer = WhiteMax()
        else: self.miniMaxer = BlackMax()
    def miniMax(self, best_value, piece_index, best_move , is_max, depth, board = ChessBoard, alpha = float, beta = float):
        return self.miniMaxer.miniMax(best_value, piece_index, best_move , is_max, depth, board, alpha, beta)
        
