from copy import deepcopy
import ChessPieces


class ChessPiece:
    "Các thuộc tính cơ bản của quân cờ"
    def __init__(self, position, piece_value, name, side):
#        self.occupied_tile.append(position)
        self.position = position
        self.is_dead = False
        self.piece_value = piece_value
        self.name = name
        self.has_moved = False
        self.side = side
    def getPieceName(self, side):
        "Tìm ký hiệu của quân cờ trên bàn cơ <Không cần thiết khi có dao diện>"
        if(side == "White"): name = "w"
        else: name = "b"
        if(self.name == "Pawn"): name = name + "p"
        elif(self.name == "Rock"): name = name + "r"
        elif(self.name == "Knight"): name = name + "kn"
        elif(self.name == "Bishop"): name = name + "b"
        elif(self.name == "Queen"): name = name + "q"
        elif(self.name == "King"): name = name + "K"
        return name
    def makeMove(self, new_position, board):
        if(board.board_display[new_position[0]][new_position[1]] != "0"):
            board.deletePiece(new_position)
        board.board_display[new_position[0]][new_position[1]] = board.board_display[self.position[0]][self.position[1]]
        board.board_display[self.position[0]][self.position[1]] = "0"
        self.position = new_position
        self.has_moved = True
    def isEaten(self, board):
        self.is_dead = True
    def isInTheBoard(position):
        "KT xem nước đi còn trong bàn cờ không"
        if(position[0] < 0 or position[1] < 0): return False
        if(position[0] > 7 or position[1] > 7): return False
        return True
    def updateMove_Multiple(self, move_vectors, board):
        "Trả về các ô đi được của quân cờ đi được nhiều ô (Xe, Tịnh, Hậu)"
        movable_tile = []     
        for vector in move_vectors:
            check_tile = deepcopy(self.position)
            check_tile[0] += vector[0]
            check_tile[1] += vector[1]
            try:
                while(board.board_display[check_tile[0]][check_tile[1]] == "0" and ChessPiece.isInTheBoard(check_tile)):
                    movable_tile.append(deepcopy(check_tile))
                    check_tile[0] += vector[0]
                    check_tile[1] += vector[1]
                #Thêm tile có quân cờ địch ăn được
                if(ChessPiece.isInTheBoard(check_tile)):
                    if(board.locatePiece(check_tile).side != self.side):
                        movable_tile.append(deepcopy(check_tile))
            except IndexError:
                #Ra khỏi bàn cờ
                continue
        return movable_tile
    def updateMove_Singular(self, move_vectors, board):
        movable_tile = []
        for vector in move_vectors:
            check_tile = deepcopy(self.position)
            check_tile[0] += vector[0]
            check_tile[1] += vector[1]
            if(ChessPiece.isInTheBoard(check_tile)):
                if(board.board_display[check_tile[0]][check_tile[1]] == "0"):
                    movable_tile.append(deepcopy(check_tile))
                    #Thêm tile có quân cờ địch ăn được (Trừ khi là Tốt)
                elif(board.locatePiece(check_tile).side != self.side and len(move_vectors) > 1):
                    movable_tile.append(deepcopy(check_tile))
        return movable_tile

        