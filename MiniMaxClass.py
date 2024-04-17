from copy import deepcopy
from ChessBoardClass import ChessBoard

class Minimax:
    def __init__(self, maxing_player):
        self.maxing_player = maxing_player
    def miniMax(self, best_value, piece_index, best_move , is_max, depth, board = ChessBoard, alpha = int, beta = int):
        #Khởi tạo
        if is_max: best_value = -float("Inf")
        else: best_value = float("Inf")
        #Kiểm tra kết thúc game hoặc đến đáy
        if(board.endGame()[0] == True or depth <= 0):
            return [board.evaluateBoard(self.maxing_player), ["",""]]
        #Xem từng nước đi một
        if((is_max == True and self.maxing_player == "White") or (is_max == False and self.maxing_player == "Black")):
            for piece in board.player_white.chess_pieces:
                movable_tile = piece.displayMovableTile(board)
                for move in movable_tile:
                    copy_board = deepcopy(board)
                    p_index = board.player_white.chess_pieces.index(piece)
                    copy_piece = copy_board.player_white.chess_pieces[p_index]
                    #Tạo copy của bàn cờ
                    copy_piece.makeMove(move, copy_board)
                    #Đệ quy, tìm nhánh dưới
                    board_value = self.miniMax(best_value, piece_index, best_move, not is_max, depth - 1, copy_board, alpha, beta)[0]
                    if(best_value < board_value and is_max == True): 
                        best_value = board_value
                        piece_index = p_index
                        best_move = move
                        alpha = max(best_value, alpha)
                    if(best_value > board_value and is_max == False): 
                        best_value = board_value
                        piece_index = p_index
                        best_move = move
                        beta = min(best_value, beta)
                    if(beta <= alpha): break
                if(beta <= alpha): break
        elif((is_max == True and self.maxing_player == "Black") or (is_max == False and self.maxing_player == "White")):
            for piece in board.player_black.chess_pieces:
                for move in piece.displayMovableTile(board):
                    copy_board = deepcopy(board)
                    p_index = board.player_black.chess_pieces.index(piece)
                    copy_piece = copy_board.player_black.chess_pieces[p_index]
                    copy_piece.makeMove(move, copy_board)
                    board_value = self.miniMax(best_value, piece_index ,best_move, not is_max, depth - 1, copy_board, alpha, beta)[0]
                    if(best_value < board_value and is_max == True): 
                        best_value = board_value
                        piece_index = p_index
                        best_move = move
                        alpha = max(best_value, alpha)
                    if(best_value > board_value and is_max == False): 
                        best_value = board_value
                        piece_index = p_index
                        best_move = move
                        beta = min(best_value, beta)
                    if(beta <= alpha): break
                if(beta <= alpha): break
        return [best_value, piece_index , best_move]
