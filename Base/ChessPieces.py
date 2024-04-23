from Base.ChessAtribute import ChessPiece
from copy import deepcopy

class Paw(ChessPiece):
    "Tốt"
    def __init__(self, position, side):
        super().__init__(position, 10, "Pawn", side)
        #KT di chuyển chưa
    def displayMovableTile(self, board):
        if(self.side == "White"): move_vector = 1
        elif(self.side == "Black"): move_vector = -1
        movable_tile = []
        if(self.has_moved == False):
            for i in [self.position[0] + move_vector*1, self.position[0] + move_vector*2]:
                if(board.board_display[i][self.position[1]] != "0"):
                    break
                movable_tile.append([i, self.position[1]]) 
        else: 
            movable_tile = self.updateMove_Singular([[move_vector, 0]], board)
        #Xem 2 bên chéo quân tốt có quân địch nào để ăn được không
        try:
            check_tile = [self.position[0] + move_vector, self.position[1] - 1]
            if(board.locatePiece(check_tile).side != self.side):
                movable_tile.append(check_tile)
        except AttributeError:
            pass
        #AttributeError khi trên tile kiểm tra không có quân cờ nào cả
        try: 
            check_tile = [self.position[0] + move_vector, self.position[1] + 1]
            if(board.locatePiece(check_tile).side != self.side):
                movable_tile.append(check_tile)
        except AttributeError:
            pass
        self.available_move = movable_tile
        self.gradePiece(5)
        return movable_tile
class Rock(ChessPiece):
    "Xe"
    def __init__(self, position, side):
        super().__init__(position, 100, "Rock", side)
        #KT di chuyển chưa để có nhập thành
        self.has_moved = False
    def displayMovableTile(self, board):
        "Tìm các nước có thể đi hiện tại"
        movable_tile = self.updateMove_Multiple([[1, 0], [0, 1], [-1, 0], [0, -1]], board)
        self.gradePiece(15)
        return movable_tile

class Knight(ChessPiece):
    "Mã"
    def __init__(self, position, side):
        super().__init__(position, 150, "Knight", side)
        #Khởi tạo bước đi đầu
    def displayMovableTile(self, board):
        movable_tile = self.updateMove_Singular([[2, 1], [-2, 1], [2, -1], [-2, -1], 
                                         [1, 2], [-1, 2], [1, -2], [-1, -2]], board)
        self.available_move = movable_tile
        self.gradePiece(30)
        return movable_tile
                                         


class Bishop(ChessPiece):
    "Tịnh"
    def __init__(self, position, side):
        super().__init__(position, 100, "Bishop", side)
    def displayMovableTile(self, board):
        "Tìm các nước có thể đi hiện tại"
        movable_tile = self.updateMove_Multiple([[1, 1], [-1, 1], [1, -1], [-1, -1]], board)
        self.gradePiece(15)
        return movable_tile

class Queen(ChessPiece):
    "Hậu"
    def __init__(self, position, side):
        super().__init__(position, 500, "Queen", side)
    def displayMovableTile(self, board):
        "Tìm các nước có thể đi hiện tại"
        movable_tile = self.updateMove_Multiple([[1, 0], [0, 1], [-1, 0], [0, -1], 
                                                 [1, 1], [-1, 1], [1, -1], [-1, -1]], board)
        self.gradePiece(15)
        return movable_tile

class King(ChessPiece):
    "Vua"
    def __init__(self, position, side):
        super().__init__(position, 10000, "King", side)
        #KT di chuyển chưa để có nhập thành
        self.has_moved = False
    def displayMovableTile(self, board):
        movable_tile = self.updateMove_Singular([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]], board)
        #KT xem các nước đi có khiến Vua bị quân cờ địch bắt không
        if(self.side == "White"): opponent_pieces = board.player_black.chess_pieces
        elif(self.side == "Black"): opponent_pieces = board.player_white.chess_pieces
        for piece in opponent_pieces:
            for move in movable_tile:
                if(piece.name == "King"): not_movable_tile = piece.updateMove_Singular([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]], board)
                else: not_movable_tile = piece.displayMovableTile(board)
                try:
                    not_movable_tile.index(move)
                except ValueError:
                    continue
                movable_tile.remove(move)
        self.available_move = movable_tile
        return movable_tile