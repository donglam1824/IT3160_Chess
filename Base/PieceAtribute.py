from copy import copy, deepcopy
from Base.PieceEvaluation import EvaluatePiece
class ChessPiece:
    "Các thược tính cơ bản của quân cờ"
    move_count = 0
    def __init__(self, position, piece_value, name, side):
#        self.occupied_tile.append(position)
        self.position = position
        self.value = piece_value
        self.base_value = piece_value
        self.name = name
        self.has_moved = False
        self.side = side
        self.piece_symbol = ""
        self.score_table = EvaluatePiece.initailizeScore(name, side) # Điểm theo vị trí của bàn cờ
    
    def makeMove(self, new_position, board):
        if(board.board_display[new_position[0]][new_position[1]] != "0"):     
            board.deletePiece(board.locatePiece(new_position))
        board.board_display[new_position[0]][new_position[1]] = board.board_display[self.position[0]][self.position[1]]
        board.board_display[self.position[0]][self.position[1]] = "0"
        self.position = new_position
        self.has_moved = True

    def gradePiece(self):
        self.value = self.base_value + self.score_table[self.position[0]][self.position[1]]
        
    def isInTheBoard(position):
        "KT xem nước đi còn trong bàn cờ không"
        if(position[0] < 0 or position[1] < 0): return False
        if(position[0] > 7 or position[1] > 7): return False
        return True
    
    def updateMove_Multiple(self, move_vectors, board):
        "Trả về các ô đi được của quân cờ đi được nhiều ô (Xe, Tịnh, Hậu)"
        movable_tile = []     
        for vector in move_vectors:
            check_tile = copy(self.position)
            check_tile[0] += vector[0]
            check_tile[1] += vector[1]
            try:
                while(board.board_display[check_tile[0]][check_tile[1]] == "0" and ChessPiece.isInTheBoard(check_tile)):
                    movable_tile.append(copy(check_tile))
                    check_tile[0] += vector[0]
                    check_tile[1] += vector[1]
                #Thêm tile có quân cờ địch ăn được
                if(ChessPiece.isInTheBoard(check_tile)):
                    try:
                        block_piece = board.locatePiece(check_tile)
                        if(block_piece.side != self.side):
                            movable_tile.append(copy(check_tile))
                    except AttributeError:
                        print("Error NoneType", block_piece ,board.player_white.accended_paw)
                        board.printBoard()
                        exit(1)
            except IndexError:
                #Ra khỏi bàn cờ
                continue
        self.gradePiece()
        return movable_tile
    
    def updateMove_Singular(self, move_vectors, board):
        "Trả về các ô đi được của quân cờ đi được 1 ô ô (Tốt, Mã, Vua)"
        movable_tile = []
        for vector in move_vectors:
            check_tile = copy(self.position)
            check_tile[0] += vector[0]
            check_tile[1] += vector[1]
            if(ChessPiece.isInTheBoard(check_tile)):
                if(board.board_display[check_tile[0]][check_tile[1]] == "0"):
                    movable_tile.append(copy(check_tile))
                    #Thêm tile có quân cờ địch ăn được (Trừ khi là Tốt)
                else:
                    #Tìm quân cờ nằm trên đường đi của nhau
                    block_piece = board.locatePiece(check_tile)
                    if(block_piece.side != self.side and len(move_vectors) > 1):
                        movable_tile.append(copy(check_tile))
        self.gradePiece()
        return movable_tile

        