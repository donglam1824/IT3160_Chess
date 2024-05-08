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
        eaten_piece.is_dead = True
        if(eaten_piece.side == "White"): self.player_white.chess_pieces.remove(eaten_piece)
        elif(eaten_piece.side == "Black"): self.player_black.chess_pieces.remove(eaten_piece)

    def phongHau(self, piece):
        if(piece.side == "White"): self.player_white.phongHau(piece)
        elif(piece.side == "Black"): self.player_black.phongHau(piece)

    def evaluateBoard(self, side):
        "Giá trị của bàn cờ dựa theo bên chơi side"
        if(side == "White"): return self.player_white.evaluateBoard() - self.player_black.evaluateBoard()
        elif(side == "Black"): return self.player_black.evaluateBoard() - self.player_white.evaluateBoard()

    def endGame(self):
        "KT game kết thúc chưa, return [True/False, bên thắng]"
        #Đầu tiên KT vua còn nước đi nào nữa không, rồi KT vua có bị chiếu không
        #KT vua quân Trắng
        if(len(self.player_white.king.available_move) == 0):  
            #Xem vua có đang bị chiếu không
            king_position = self.player_white.king.position
            for piece in self.player_black.chess_pieces:
                movable_tile = piece.available_move
                try:
                    movable_tile.index(king_position)
                except ValueError:
                    #ValueError là quân vua không ở trong đường đi của piece
                    continue
                return [True, "Black"]
        #KT vua quân Đen
        if(len(self.player_black.king.available_move) == 0):  
            #Xem vua có đang bị chiếu không
            king_position = self.player_black.king.position
            for piece in self.player_white.chess_pieces:
                movable_tile = piece.available_move
                try:
                    movable_tile.index(king_position)
                except ValueError:
                    continue            
                return [True, "White"]
        return [False, ""]

