from Base.ChessPieces import Paw, Rock, Knight, Bishop, Queen, King

class Player:
    "Biểu hiệu của 2 người chơi"
    def __init__(self, h, h_paw, side):
        self.paws = []
        self.side = side
        self.accended_paw = [] #Dành cho Tốt đươch tăng cấp
        for i in range(0, 8):
            paw_piece = Paw([h_paw, i], side)
            self.paws.append(paw_piece)
        self.rock_1 = Rock([h, 0], side)
        self.rock_2 = Rock([h, 7], side)
        self.knight_1 = Knight([h, 1], side)
        self.knight_2 = Knight([h, 6], side)
        self.bishop_1 = Bishop([h, 2], side)
        self.bishop_2 = Bishop([h, 5], side)
        self.queen = Queen([h, 3], side)
        self.king = King([h, 4], side)
        self.chess_pieces = []
        self.chess_pieces.extend(self.paws)
        self.chess_pieces.extend([self.rock_1, self.rock_2, self.bishop_1, self.bishop_2, 
                                  self.knight_1, self.knight_2, self.queen, self.king])
        self.game_state = "Opening"
    def initalizePieces(self, board):
        for piece in self.chess_pieces:
            piece.displayMovableTile(board)
            piece.gradePiece()
        self.king.rock_1 = self.rock_1
        self.king.rock_2 = self.rock_2

    def phongHau(self, piece = Paw):
        "Tiến hành phong hậu cho tốt"
        new_queen = Queen(piece.position, piece.side)
        self.chess_pieces.remove(piece)
        self.chess_pieces.append(new_queen)
        self.accended_paw.append(new_queen)
    def evaluateBoard(self):
        value = 0
        for piece in self.chess_pieces:
            value += piece.value
        if(self.bishop_1 in self.chess_pieces and self.bishop_2 in self.chess_pieces):
            value += 5 #Bonus khi có cả 2 Bishop
        if(self.knight_1 in self.chess_pieces and self.knight_2 in self.chess_pieces):
            value += 3 #Bonus khi còn cả 2 Mã
        if(len(self.paws) == 8): 
            value -= 3 #Penalty khi có quá nhiều Pawn
        elif(len(self.paws) == 7):
            value -= 1
        elif(len(self.paws) <= 1):
            value -= 3
        elif(len(self.paws) == 0):
            value -= 10 #Penalty khi có quá ít Pawn
        if(self.game_state == "Opening" and self.queen.has_moved == True):
            value -= 2 #Penalty khi đi Hậu quá sớm

        return value
    def getOppositeSide(side):
        if(side == "White"): return "Black"
        else: return "White"
        
class BlackPlayer(Player):
    def __init__(self):
        super().__init__(0, 1, "Black")
        
class WhitePlayer(Player):
    def __init__(self):
        super().__init__(7, 6, "White")