from copy import deepcopy
from Base.ChessBoard import ChessBoard
from Minimax.WhiteMax import WhiteMax
import time

from MoveSimulate.MoveSimulator import MoveSimulator

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
# board.player_white.bishop_1.makeMove([0, 0], board)
# board.player_white.queen.makeMove([0, 1], board)


# minimax_white.simulatedMove(board, [board.player_white.paws[1], [0,1]])
MoveSimulator.simulatedMove(board, [board.player_black.queen, [7, 4]])
board.printBoard()
MoveSimulator.simulatedMove(board, [board.player_white.paws[1], [5, 1]])
board.printBoard()
MoveSimulator.simulatedMove(board, [board.player_black.queen, [7, 3]])
board.printBoard()

MoveSimulator.revertPastMove(board)
board.printBoard()
MoveSimulator.revertPastMove(board)
board.printBoard()
MoveSimulator.revertPastMove(board)
board.printBoard()

pass

