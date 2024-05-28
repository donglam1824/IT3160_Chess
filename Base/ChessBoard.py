from copy import deepcopy
from Base.Player import BlackPlayer, WhitePlayer

class ChessBoard:
    delete_counter = 0

    def __init__(self):
        self.player_white = WhitePlayer()
        self.player_black = BlackPlayer()
        self.board_display = [["br1", "bkn1", "bb1", "bq", "bK", "bb2", "bkn2", "br2"],
                            ["bp0", "bp1", "bp2", "bp3", "bp4", "bp5", "bp6", "bp7"],
                            ["0",   "0",   "0",   "0",   "0",   "0",   "0",   "0"],
                            ["0",   "0",   "0",   "0",   "0",   "0",   "0",   "0"],
                            ["0",   "0",   "0",   "0",   "0",   "0",   "0",   "0"],
                            ["0",   "0",   "0",   "0",   "0",   "0",   "0",   "0"],
                            ["wp0", "wp1", "wp2", "wp3", "wp4", "wp5", "wp6", "wp7"],
                            ["wr1", "wkn1", "wb1", "wq", "wK", "wb2", "wkn2", "wr2",]]
        #Make a new chess board
        self.player_black.initalizePieces(self)
        self.player_white.initalizePieces(self)
        self.black_king = self.player_black.king
        self.white_king = self.player_white.king
        self.captured_white_pieces = []
        self.captured_black_pieces = []
        self.last_captured_piece = None
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
        piece_symbol = self.board_display[position[0]][position[1]]
        if(piece_symbol == "0"): return ""
        if(piece_symbol[0] == 'b'): player = self.player_black
        else: player = self.player_white
        if(piece_symbol[1] == 'p'): return player.paws[int(piece_symbol[2])]
        elif(piece_symbol[1:] == "r1"): return player.rock_1
        elif(piece_symbol[1:] == "r2"): return player.rock_2
        elif(piece_symbol[1:] == "kn1"): return player.knight_1
        elif(piece_symbol[1:] == "kn2"): return player.knight_2
        elif(piece_symbol[1:] == "b1"): return player.bishop_1
        elif(piece_symbol[1:] == "b2"): return player.bishop_2
        elif(piece_symbol[1] == "q"): 
            if(len(piece_symbol) == 2): return player.queen
            else: return player.accended_paw[int(piece_symbol[2])]
        elif(piece_symbol[1:] == "K"): return player.king

    
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
        self.last_captured_piece = eaten_piece
        self.delete_counter += 1

    def pieceJustCaptured(self):
        """Checks if a piece was captured in the most recent move."""
        return self.last_captured_piece is not None
    
    def phongHau(self, piece):
        "Thực hiện phong Hậu"
        if(piece.side == "White"):
            self.board_display[piece.position[0]][piece.position[1]] = "wq" + str(len(self.player_white.accended_paw))
            self.player_white.phongHau(piece)
        elif(piece.side == "Black"): 
            self.board_display[piece.position[0]][piece.position[1]] = "bq" + str(len(self.player_black.accended_paw))
            self.player_black.phongHau(piece)

    def evaluateBoard(self, side):
        "Giá trị của bàn cờ dựa theo bên chơi side"
        if(side == "White"): return self.player_white.evaluateBoard() - self.player_black.evaluateBoard()
        elif(side == "Black"): return self.player_black.evaluateBoard() - self.player_white.evaluateBoard()

    def getCheckedKing(self):
        "KT xem vua có đang bị chiếu không, nếu có trả về bên bị chiếu"
        for piece in self.player_black.chess_pieces:
            if(piece.displayMovableTile(self).count(self.white_king.position) > 0):
                return [True, "White"]
        for piece in self.player_white.chess_pieces:
            if(piece.displayMovableTile(self).count(self.black_king.position) > 0):
                return [True, "Black"]
            
        return [False, ""]

    def endGame(self):
        "KT game kết thúc chưa, return [True/False, bên thắng]. Chỉ kiểm tra vua đã bị ăn chưa, dùng cho hàm Minimax"
        if(self.player_black.chess_pieces.count(self.black_king) == 0):
            return [True, "White"]
        elif(self.player_white.chess_pieces.count(self.white_king) == 0):
            return [True, "Black"]
        return [False, ""]
    
    def getPossibleMove(self):
        "KT các nước đi còn đi được của 2 bên, nếu hết nước đi thì game sẽ end"
        if(self.endGame()[0] == True): return self.endGame()
        white_possible_move = []
        black_possible_move = []
        current_checked_king = self.getCheckedKing()
        #Xét từng nước đi một, giống cách Minimax
        white_lose = True
        black_lose = True
        for piece in self.player_white.chess_pieces:
            movable_tile = piece.displayMovableTile(self)
            for move in movable_tile:
                copy_board = deepcopy(self)
                p_index = self.player_white.chess_pieces.index(piece)
                copy_piece = copy_board.player_white.chess_pieces[p_index]
                #Tạo copy của bàn cờ
                copy_piece.makeMove(move, copy_board)
                checked_king = copy_board.getCheckedKing()
                if(checked_king[0] == False or (checked_king == [True, "Black"] and current_checked_king != [True, "White"])):
                    white_possible_move.append([piece ,move])
                    white_lose = False

        for piece in self.player_black.chess_pieces:
            movable_tile = piece.displayMovableTile(self)
            for move in movable_tile:
                copy_board = deepcopy(self)
                p_index = self.player_black.chess_pieces.index(piece)
                #Tạo copy của bàn cờ
                copy_piece = copy_board.player_black.chess_pieces[p_index]
                copy_piece.makeMove(move, copy_board)
                checked_king = copy_board.getCheckedKing()
                if(checked_king[0] == False or (checked_king == [True, "White"]  and current_checked_king != [True, "Black"])):
                    black_possible_move.append([piece, move])
                    black_lose = False

        return [white_possible_move, black_possible_move]
        
        
            
                


