from copy import copy, deepcopy
from Base.ChessBoard import ChessBoard
from MoveSimulate.PastMove import PastMove

class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.past_move_stack = []
    
    def updateDepth(self, new_depth):
        self.max_depth = new_depth
