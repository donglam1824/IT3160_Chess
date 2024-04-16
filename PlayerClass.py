from ChessPieces import Paw, Rock, Knight, Bishop, Queen, King

class Player:
    "Biểu hiệu của 2 người chơi"
    def __init__(self, h, h_paw, side):
        self.paws = []
        self.side = side
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
        self.chess_pieces = self.paws
        self.chess_pieces.extend([self.rock_1, self.rock_2, self.bishop_1, self.bishop_2, self.knight_1, self.knight_2, self.queen, self.king])
    def evaluateBoard(self):
        value = 0
        for piece in self.chess_pieces:
            value += piece.piece_value
        return value
        
class BlackPlayer(Player):
    def __init__(self):
        super().__init__(7, 6, "Black")
        
class WhitePlayer(Player):
    def __init__(self):
        super().__init__(0, 1, "White")