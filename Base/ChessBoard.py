from copy import deepcopy, copy
import time
from Base.Player import BlackPlayer, WhitePlayer
from Base.PieceEvaluation import EvaluatePiece
from MoveSimulate.MoveSimulator import MoveSimulator

class ChessBoard:

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
        self.game_state = "Opening" #3 state: "Opening"; "Middle"; "Ending"
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
    
    def updateToMiddleState(self):
        self.game_state = "Middle"
        self.player_black.game_state = "Middle"
        self.player_white.game_state = "Middle"

    def updateToEndingState(self):
        self.game_state = "Ending"
        self.player_black.game_state = "Ending"
        self.player_white.game_state = "Ending"
        self.white_king.score_table = EvaluatePiece.king_white_late
        self.black_king.score_table = EvaluatePiece.king_black_late

    def locatePiece(self, position):
        "Xác định quân cờ trên 1 position, return object Quân cờ"
        piece_symbol = self.board_display[position[0]][position[1]]
        if(piece_symbol == "0"): return None
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

    
    def deletePiece(self, eaten_piece):
        "Xoá quân cờ bị ăn ra khỏi bàn cờ"
        if(self.game_state == "Opening"): self.updateToMiddleState() #Hết Opening sau khi ăn 1 quân
        if(eaten_piece.side == "White"): 
            self.captured_white_pieces.append(eaten_piece)
            self.player_white.chess_pieces.remove(eaten_piece)
        elif(eaten_piece.side == "Black"): 
            self.player_black.chess_pieces.remove(eaten_piece)
            self.captured_black_pieces.append(eaten_piece)
        self.last_captured_piece = eaten_piece
        if((self.player_black.queen in self.captured_black_pieces and self.player_white.queen in self.captured_white_pieces) 
        or len(self.getAllPieces()) <= 10):
            self.updateToEndingState() #Khi Hậu bị ăn hết hoặc còn 14 quân trên bàn đấu, chuyển về Ending
    
    def revivePiece(self, revived_piece, piece_index, piece_symbol):
        "Hồi sinh 1 quân cờ"
        try:
            if(revived_piece.side == "White"): 
                self.captured_white_pieces.remove(revived_piece)
                self.player_white.chess_pieces.insert(piece_index , revived_piece)
            elif(revived_piece.side == "Black"): 
                self.captured_black_pieces.remove(revived_piece)
                self.player_black.chess_pieces.insert(piece_index , revived_piece)
            self.board_display[revived_piece.position[0]][revived_piece.position[1]] = piece_symbol
            self.last_captured_piece = None
        except Exception:
            self.printBoard()
            print(piece_symbol, revived_piece.position, revived_piece)
            print("Black capture", self.captured_black_pieces)
            print("White capture",self.captured_white_pieces)

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
            if self.white_king.position in piece.displayMovableTile(self):
                return [True, "White"]
        for piece in self.player_white.chess_pieces:
            if self.black_king.position in piece.displayMovableTile(self):
                return [True, "Black"]
            
        return [False, ""]

    def endGame(self):
        "KT game kết thúc chưa, return [True/False, bên thắng]. Chỉ kiểm tra vua đã bị ăn chưa, dùng cho hàm Minimax"
        if(self.player_black.chess_pieces.count(self.black_king) == 0):
            return [True, "White"]
        elif(self.player_white.chess_pieces.count(self.white_king) == 0):
            return [True, "Black"]
        return [False, ""]
    
    def getPossibleMoveWhite(self):
        "KT các nước đi còn đi được của 2 bên, nếu hết nước đi thì game sẽ end"
        if(self.endGame() == [True, "Black"]): return []
        white_possible_move = []
        current_checked_king = self.getCheckedKing()
        move_simulator = MoveSimulator(self)
        #Xét từng nước đi một, giống cách Minimax
        for piece in self.player_white.chess_pieces:
            movable_tile = piece.displayMovableTile(self)
            for move in movable_tile:
                move_simulator.simulatedMove([piece, move])
                checked_king = self.getCheckedKing()
                if(checked_king[0] == False or (checked_king == [True, "Black"] and current_checked_king != [True, "White"])):
                    white_possible_move.append([piece ,move])
                move_simulator.revertPastMove(self)
        return white_possible_move
    
    def getPossibleMoveBlack(self):
        "KT các nước đi còn đi được của 2 bên, nếu hết nước đi thì game sẽ end"
        if(self.endGame() == [True, "White"]): return []
        black_possible_move = []
        current_checked_king = self.getCheckedKing()
        move_simulator = MoveSimulator(self)
        #Xét từng nước đi một, giống cách Minimax
        for piece in self.player_black.chess_pieces:
            movable_tile = piece.displayMovableTile(self)
            for move in movable_tile:
                move_simulator.simulatedMove([piece, move])
                checked_king = self.getCheckedKing()
                if(checked_king[0] == False or (checked_king == [True, "White"]  and current_checked_king != [True, "Black"])):
                    black_possible_move.append([piece, move])
                move_simulator.revertPastMove(self)
        return black_possible_move
    

    def displayToChessBoard(board_display, white_castle, black_castle):
        "Chuyển từ bàn cờ vẽ 2D thành object bàn cờ, ..._castle = [Trái, Phải]: 2 bên có thể nhập thành không"
        new_board = ChessBoard()
        new_board.board_display = board_display
        piece_stack = new_board.getAllPieces()
        for i in range(0, 8):
            for j in range(0, 8):
                if(board_display[i][j] != "0"):
                    piece = new_board.locatePiece([i, j])
                    piece.position = [i, j]
                    if(piece.name == "Pawn" and piece.position[0] != piece.start_position):
                        piece.has_moved = True
                    piece_stack.remove(piece) #Xếp dần quân cờ vào bàn cờ trống

        if(white_castle[0] == False):
            new_board.player_white.rock_1.has_moved = True
        elif(white_castle[1] == False):
            new_board.player_white.rock_2.has_moved = True

        if(black_castle[0] == False):
            new_board.player_black.rock_1.has_moved = True
        elif(black_castle[1] == False):
            new_board.player_black.rock_2.has_moved = True
        
        #Xóa các quân đã bị ăn
        for piece in piece_stack:
            new_board.deletePiece(piece)
        
        return new_board
        
            
                


