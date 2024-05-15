import time
from Base.ChessBoardClass import ChessBoard
from Minimax.MiniMaxClass import Minimax

board = ChessBoard()
minimax_black = Minimax("Black")
board.player_black.paws[3].makeMove([5, 3], board)
board.player_black.paws[4].makeMove([5, 4], board)
board.player_white.bishop_2.makeMove([4, 1], board)
board.printBoard()
print(board.player_black.king.displayMovableTile(board))
print(board.endGame())
tic = time.perf_counter()
best = minimax_black.miniMax(0, "", "", True, 3, board, -float("Inf"), float("Inf"))
print(time.perf_counter()-tic)
print(best[0], board.player_black.chess_pieces[best[1]].name, best[2])