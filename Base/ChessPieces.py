from Base.PieceAtribute import ChessPiece
from copy import deepcopy

class Paw(ChessPiece):
    "Tốt"
    def __init__(self, position, side):
        super().__init__(position, 10, "Pawn", side)
        if(side == "White"): self.start_position = 6
        else: self.start_position = 1
        #KT di chuyển chưa
    def displayMovableTile(self, board):
        if(self.side == "White"): move_vector = -1
        elif(self.side == "Black"): move_vector = 1
        movable_tile = []
        if(self.has_moved == False):
            for pos in [self.position[0] + move_vector*1, self.position[0] + move_vector*2]:
                if(board.board_display[pos][self.position[1]] != "0"):
                    break
                movable_tile.append([pos, self.position[1]]) 
        else: 
            movable_tile = self.updateMove_Singular([[move_vector, 0]], board)
        #Xem 2 bên chéo quân tốt có quân địch nào để ăn được không
        for i in [-1, 1]:
            check_tile = [self.position[0] + move_vector, self.position[1] + i]
            if(check_tile[1] < 0 or check_tile[1] > 7): continue #Không được kiểm tra ngoài bàn cờ
            if(board.board_display[check_tile[0]][check_tile[1]] != "0"):
                close_piece = board.locatePiece(check_tile)
                if(close_piece.side != self.side):
                    movable_tile.append(check_tile)
        self.gradePiece()
        return movable_tile
    def makeMove(self, new_position, board):
        super().makeMove(new_position, board)
        #Kiểm tra xem phong hậu được không
        if(self.side == "White"): final_position = 0
        elif(self.side == "Black"): final_position = 7
        if(new_position[0] == final_position):
            board.phongHau(self)
            
class Rock(ChessPiece):
    "Xe"
    def __init__(self, position, side):
        super().__init__(position, 50, "Rock", side)
        #KT di chuyển chưa để có nhập thành
        self.has_moved = False
    def displayMovableTile(self, board):
        "Tìm các nước có thể đi hiện tại"
        movable_tile = self.updateMove_Multiple([[1, 0], [0, 1], [-1, 0], [0, -1]], board)
        return movable_tile

class Knight(ChessPiece):
    "Mã"
    def __init__(self, position, side):
        super().__init__(position, 32, "Knight", side)
        #Khởi tạo bước đi đầu
    def displayMovableTile(self, board):
        movable_tile = self.updateMove_Singular([[2, 1], [-2, 1], [2, -1], [-2, -1], 
                                         [1, 2], [-1, 2], [1, -2], [-1, -2]], board)
        return movable_tile
                                         

class Bishop(ChessPiece):
    "Tịnh"
    def __init__(self, position, side):
        super().__init__(position, 33, "Bishop", side)
    def displayMovableTile(self, board):
        "Tìm các nước có thể đi hiện tại"
        movable_tile = self.updateMove_Multiple([[1, 1], [-1, 1], [1, -1], [-1, -1]], board)
        return movable_tile

class Queen(ChessPiece):
    "Hậu"
    def __init__(self, position, side):
        super().__init__(position, 90, "Queen", side)
    def displayMovableTile(self, board):
        "Tìm các nước có thể đi hiện tại"
        movable_tile = self.updateMove_Multiple([[1, 0], [0, 1], [-1, 0], [0, -1], 
                                                 [1, 1], [-1, 1], [1, -1], [-1, -1]], board)
        return movable_tile

class King(ChessPiece):
    "Vua"
    def __init__(self, position, side):
        super().__init__(position, 2000, "King", side)
        self.rock_1 = ""
        self.rock_2 = ""
        #KT di chuyển chưa để có nhập thành
        self.has_moved = False

    def makeMove(self, new_position, board):
        castle_check = new_position[1] - self.position[1]
        if(abs(castle_check) == 2):
            #Thực hiện nhập thành
            if(castle_check < 0): self.rock_1.makeMove([new_position[0], new_position[1] + 1], board)
            else: self.rock_2.makeMove([new_position[0], new_position[1] - 1], board)
        super().makeMove(new_position, board)

    def displayMovableTile(self, board):
        movable_tile = self.updateMove_Singular([[1, 0], [0, 1], [-1, 0], [0, -1], 
                                                 [1, 1], [-1, 1], [1, -1], [-1, -1]], board)
        #KT nhập thành
        if(self.has_moved == False):
            if(self.side == "White"): player = board.player_white
            else: player = board.player_black
            #KT Xe bên trái
            if(player.rock_1.has_moved == False and len(self.updateMove_Multiple([[0, -1]], board)) == 3):
                movable_tile.append([self.position[0], self.position[1] -2])
            #KT Xe bên phải
            if(player.rock_1.has_moved == False and len(self.updateMove_Multiple([[0, 1]], board)) == 2):
                movable_tile.append([self.position[0], self.position[1] +2])
        return movable_tile