from Base.PlayerClass import BlackPlayer, WhitePlayer

class ChessBoard:
    def __init__(self):
        self.player_white = WhitePlayer()
        self.player_black = BlackPlayer()
        self.board_display = []
        #Make a new chess board
        for i in range(0, 8):
            self.board_display.append([])
            for j in range(0, 8):
                self.board_display[i].append("0")
        for piece in self.player_black.chess_pieces:
            name = piece.getPieceName("Black")
            self.board_display[piece.position[0]][piece.position[1]] = name
        for piece in self.player_white.chess_pieces:
            name = piece.getPieceName("White")
            self.board_display[piece.position[0]][piece.position[1]] = name
        self.player_black.initalizePieces(self)
        self.player_white.initalizePieces(self)
        self.black_king = self.player_black.king
        self.white_king = self.player_white.king
        self.captured_white_pieces = []
        self.captured_black_pieces = []
    def printBoard(self):
        "Vẽ cờ trên màn console"
        print("|")
        for i in range(0, 8):
            print("__", end = " ")
            line = self.board_display[i]
            print("{:3} {:3} {:3} {:3} {:3} {:3} {:3} {:3}".format(*line), end = " ")
            print("__")
        print("|")
        
    def getAllPieces(self):
        "Trả về mọi quân cờ còn trên bàn cờ"
        chess_pieces = []
        chess_pieces.extend(self.player_black.chess_pieces)
        chess_pieces.extend(self.player_white.chess_pieces)

        return chess_pieces
    def locatePiece(self, position):
        "Xác định quân cờ trên 1 position, return object Quân cờ"
        chess_pieces = self.getAllPieces()
        for piece in chess_pieces:
            if(piece.position == position):
                return piece
        return "No piece in this position"
    
    def deletePiece(self, position):
        "Xoá quân cờ bị ăn ra khỏi bàn cờ"
        eaten_piece = self.locatePiece(position)
        eaten_piece.isEaten(self)
        if(eaten_piece.side == "White"): 
            self.captured_white_pieces.append(eaten_piece)
            self.player_white.chess_pieces.remove(eaten_piece)
        elif(eaten_piece.side == "Black"): 
            self.player_black.chess_pieces.remove(eaten_piece)
            self.captured_black_pieces.append(eaten_piece)

    def phongHau(self, piece):
        if(piece.side == "White"): self.player_white.phongHau(piece)
        elif(piece.side == "Black"): self.player_black.phongHau(piece)

    def evaluateBoard(self, side):
        "Giá trị của bàn cờ dựa theo bên chơi side"
        if(side == "White"): return self.player_white.evaluateBoard() - self.player_black.evaluateBoard()
        elif(side == "Black"): return self.player_black.evaluateBoard() - self.player_white.evaluateBoard()

    def endGame(self):
        "KT game kết thúc chưa, return [True/False, bên thắng]"
        if(self.player_black.chess_pieces.count(self.black_king) == 0):
            return [True, "White"]
        elif(self.player_white.chess_pieces.count(self.white_king) == 0):
            return [True, "Black"]
        return [False, ""]

