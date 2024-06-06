from Base.ChessBoard import ChessBoard
import math

UCT_CONSTANT_OPENING= 200
UCT_CONSTANT_MIDDLE= 80
UCT_CONSTANT_ENDING = 40

class Node:
    "Thuộc tính của mỗi Node trong cây"
    def __init__(self, current_side, parent, moving_piece, old_position, new_position):
        self.current_side = current_side
        self.total = 0
        self.visited = 0
        self.parent = parent
        self.moving_piece = moving_piece #Ở dạng symbol (VD: "bp1", "wq")
        self.old_position = old_position
        self.new_position = new_position
        self.children = []
    def getUctValue(self, game_state):
        if(self.visited == 0): return float("Inf")
        else:
            if(game_state == "Opening"):
                c = UCT_CONSTANT_OPENING
            elif(game_state == "Middle"):
                c = UCT_CONSTANT_MIDDLE
            else:
                c = UCT_CONSTANT_ENDING
            #t/ni + c*sqrt(ln(N) / ni)
            #t: tổng giá trị các node con (total)
            #ni : số lần visit
            #N: sô lần visit của cha
            #c = UCT_constant
            return (self.total / self.visited) + c*math.sqrt(math.log(self.parent.visited) / self.visited)
    def makeMoveToNode(self, board : ChessBoard):
        "Di chuyển quân cờ trên bàn cờ theo thông tin của node này"
        piece = board.locatePiece(self.old_position)
        piece.makeMove(self.new_position, board)
    
    def updateState(self, value):
        self.visited += 1
        self.total += value

        
        