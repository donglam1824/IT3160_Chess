from copy import deepcopy
from Base.ChessBoard import ChessBoard
from Minimax.BlackMax import BlackMax
from Minimax.WhiteMax import WhiteMax


class Minimax:
    def __init__(self, maxing_player, max_depth):
        if(maxing_player == "White"): self.miniMaxer = WhiteMax()
        else: self.miniMaxer = BlackMax()
        self.max_depth = max_depth
    
    def updateDepth(self, new_depth):
        self.max_depth = new_depth
    def miniMax(self, best_value, piece_index, best_move , is_max, board = ChessBoard, alpha = float, beta = float):
        return self.miniMaxer.miniMax(best_value, piece_index, best_move , is_max, self.max_depth, board, alpha, beta)
        
