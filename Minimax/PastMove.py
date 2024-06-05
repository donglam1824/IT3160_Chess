from Base.ChessBoard import ChessBoard

class PastMove:
    def __init__(self, piece, old_position, move_position, is_castle_move
                 , is_pawn_assended_move, eaten_piece, index, symbol):
        self.piece = piece
        self.old_position = old_position
        self.move_position = move_position
        self.is_castle_move = is_castle_move #[True/False, if True = Lelf/Right]
        self.is_pawn_assended_move = is_pawn_assended_move #True/False
        self.eaten_piece = {"piece" : eaten_piece, "index" : index, "symbol" : symbol}