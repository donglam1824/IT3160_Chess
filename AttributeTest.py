from copy import deepcopy
from Base.ChessBoard import ChessBoard
from Minimax.WhiteMax import WhiteMax
import time

# new_board =  ChessBoard.displayToChessBoard([['br1', 'bkn1', 'bb1', 'bq', 'bK', 'bb2', 'bkn2', 'br2'], 
#                                 ['bp0', 'bp1', 'bp2', 'bp3', '0', '0', 'bp6', 'bp7'], 
#                                 ['0', '0', '0', '0', '0', 'bp5', '0', '0'], 
#                                 ['0', '0', '0', '0', '0', '0', '0', '0'], 
#                                 ['0', '0', '0', 'wkn1', '0', '0', '0', '0'], 
#                                 ['0', '0', '0', '0', '0', '0', '0', 'wp7'], 
#                                 ['wp0', 'wp1', 'wp2', '0', 'wp4', 'wp5', 'wp6', '0'], 
#                                 ['wr1', '0', 'wb1', '0', 'wK', 'wb2', 'wkn2', 'wr2']]
#                                 , [True, True], [True, True])

board = ChessBoard()
minimax_white = WhiteMax(3)
board.player_white.bishop_1.makeMove([0, 0], board)
board.player_white.queen.makeMove([0, 1], board)


start_time = time.perf_counter()
copy_board = deepcopy(board)
copy_board.player_white.paws[1].makeMove([1, 1], copy_board)
print(time.perf_counter() - start_time)

start_time = time.perf_counter()
# minimax_white.simulatedMove(board, [board.player_white.paws[1], [0,1]])
minimax_white.simulatedMove(board, [board.white_king, [7,2]])

board.printBoard()

minimax_white.revertPastMove(board)
print(time.perf_counter() - start_time)

board.printBoard()


