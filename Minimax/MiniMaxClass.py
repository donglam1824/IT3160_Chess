from copy import copy, deepcopy

from MoveSimulate.MoveSimulator import MoveSimulator


class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.move_simulator = MoveSimulator(None)
    
    def updateDepth(self, new_depth):
        self.max_depth = new_depth
