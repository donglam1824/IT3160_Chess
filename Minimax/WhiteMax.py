from Base.ChessBoard import ChessBoard
from Minimax.MiniMaxClass import Minimax
from copy import deepcopy

class WhiteMax(Minimax):
    def __init__(self, max_depth):
        super().__init__(max_depth)

    def miniMax(self, best_value, piece_index, best_move , is_max, board = ChessBoard, alpha = float, beta = float):
        copy_board = deepcopy(board)
        return self.miniMaxActive(best_value, piece_index, best_move , is_max, self.max_depth, copy_board, alpha, beta)
    
    def miniMaxActive(self, best_value, piece_index, best_move , is_max, depth, board = ChessBoard, alpha = int, beta = int):
        #Khởi tạo
        if is_max: best_value = -float("Inf")
        else: best_value = float("Inf")
        #Kiểm tra kết thúc game hoặc đến đáy
        if(board.endGame()[0] == True or depth <= 0):
            return [board.evaluateBoard("White"), "",""]
        #Xem từng nước đi một
        if(is_max == True):
            for piece in board.player_white.chess_pieces:
                movable_tile = piece.displayMovableTile(board)
                p_index = board.player_white.chess_pieces.index(piece)
                for move in movable_tile:
                    self.simulatedMove(board, [piece, move])
                    board_value = self.miniMaxActive(best_value, piece_index, best_move, not is_max, 
                                               depth - 1, board, alpha, beta)[0]
                    if(best_value < board_value): 
                        best_value = board_value
                        piece_index = p_index
                        best_move = move
                        alpha = max(best_value, alpha)
                    self.revertPastMove(board)
                    if(beta <= alpha): break
                if(beta <= alpha): break
        else:
            for piece in board.player_black.chess_pieces:
                movable_tile = piece.displayMovableTile(board)
                p_index = board.player_black.chess_pieces.index(piece)
                for move in movable_tile:
                    self.simulatedMove(board, [piece, move])
                    board_value = self.miniMaxActive(best_value, piece_index ,best_move, not is_max, 
                                               depth - 1, board, alpha, beta)[0]
                    if(best_value > board_value and is_max == False): 
                        best_value = board_value
                        piece_index = p_index
                        best_move = move
                        beta = min(best_value, beta)
                    self.revertPastMove(board)
                    if(beta <= alpha): break
                if(beta <= alpha): break
        return [best_value, piece_index , best_move]
