from Base.ChessBoard import ChessBoard
import math

UCT_CONSTANT= 14.1

class Node:
    "Thuộc tính của mỗi Node trong cây"
    def __init__(self, board : ChessBoard, current_side, parent, previous_move, white_castle, black_castle):
        self.board = board
        self.current_side = current_side
        self.total = 0
        self.visited = 0
        self.parent = parent
        self.previous_move = previous_move
        self.castle_state = {"White" : white_castle, "Black" : black_castle}
        self.children = []
    def getNodeData(self):
        return (str(self.board.board_display), self.current_side, self.total, self.visited)
    def getUctValue(self):
        if(self.visited == 0): return float("Inf")
        else:
            #t/ni + c*sqrt(ln(N) / ni)
            #t: tổng giá trị các node con (total)
            #ni : số lần visit
            #N: sô lần visit của cha
            #c = UCT_constant
            return (self.total / self.visited) + UCT_CONSTANT*math.sqrt(math.log(self.parent.visited) / self.visited)
    def updateState(self, value):
        self.visited += 1
        self.total += value
        