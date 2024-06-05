from copy import copy, deepcopy
from Base.ChessBoard import ChessBoard
from Minimax.PastMove import PastMove

class Minimax:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.past_move_stack = []
    
    def updateDepth(self, new_depth):
        self.max_depth = new_depth

    # def miniMax(self, best_value, piece_index, best_move , is_max, board = ChessBoard, alpha = float, beta = float):
    #     copy_board = deepcopy(board)
    #     return self.miniMaxer.miniMax(best_value, piece_index, best_move , is_max, self.max_depth, copy_board, alpha, beta)
    
    def simulatedMove(self, board : ChessBoard , move):
        "Giả 1 nước đi để nhìn trước thế cờ"
        #move = [piece, move_posiiton]
        piece = move[0]
        old_position = copy(piece.position)
        move_position = move[1]
        board_display = board.board_display
        if(piece.side == "White"): 
            player = board.player_white
            opposite_player = board.player_black
        else: 
            player = board.player_black
            opposite_player = board.player_white

        if(piece.name == "King"): # Kiểm tra có phải nhập thành không
            castle_check = move_position[1] - piece.position[1]
            if(castle_check == 2): is_castle_move = [True, "Right"]
            elif(castle_check == -2): is_castle_move = [True, "Left"]
            else: is_castle_move = [False, ""]
        else: is_castle_move = [False, ""]
        
        if(piece.name == "Pawn"): # Kiểm tra có phải phong hậu không
            is_pawn_assended_move = [(move_position[0] == piece.final_position), player.paws.index(piece)]
        else: is_pawn_assended_move = [False, -1]

        eaten_piece = board.locatePiece(move_position)
        if(eaten_piece != None):
            eaten_piece_index = opposite_player.chess_pieces.index(eaten_piece)
        else: 
            eaten_piece_index = -1
        eaten_piece_symbol = board.board_display[move_position[0]][move_position[1]]

        piece.makeMove(move_position, board)
        past_move = PastMove(piece, old_position, move_position, is_castle_move, 
                             is_pawn_assended_move, eaten_piece, eaten_piece_index, eaten_piece_symbol)
        self.past_move_stack.append(past_move)
    
    def revertPastMove(self, board : ChessBoard, reverted_move : PastMove = None):
        reverted_move = self.past_move_stack.pop()
        piece = reverted_move.piece

        if(piece.side == "White"): player = board.player_white
        else: player = board.player_black

        if(piece.name == "King"): piece.returnToPosition(reverted_move.old_position, board)
        else: piece.makeMove(reverted_move.old_position, board)

        if(reverted_move.eaten_piece["piece"] != None):
            eaten_piece = reverted_move.eaten_piece
            board.revivePiece(eaten_piece["piece"], eaten_piece["index"], eaten_piece["symbol"])

        if(reverted_move.is_castle_move[0] == True): #Nếu là nhập thành, trả xe về chỗ cũ
            if(reverted_move.is_castle_move[1] == "Left"): 
                old_position = [reverted_move.move_position[0], reverted_move.move_position[1] - 2]
                player.rock_1.makeMove(old_position, board)
            else:
                old_position = [reverted_move.move_position[0], reverted_move.move_position[1] + 1]
                player.rock_2.makeMove(old_position, board)

        if(reverted_move.is_pawn_assended_move[0] == True): #Nếu là phong hậu, xóa quân hậu mới đi, đưa tốt về
            player.chess_pieces.insert(reverted_move.is_pawn_assended_move[1], piece)
            assended_pawn = board.locatePiece(reverted_move.old_position)
            if(player.side == "White"): piece_symbol = "wp"
            else: piece_symbol = "bp"
            board.board_display[reverted_move.old_position[0]][reverted_move.old_position[1]] =  piece_symbol + str(reverted_move.is_pawn_assended_move[1])
            player.chess_pieces.remove(assended_pawn)
            player.accended_paw.remove(assended_pawn)
