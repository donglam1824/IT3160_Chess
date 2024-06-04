from Base.ChessBoard import ChessBoard
from Minimax.MiniMaxClass import Minimax
import time

new_board =  ChessBoard.displayToChessBoard([['br1', 'bkn1', 'bb1', 'wq0', 'bK', 'bb2', 'bkn2', 'br2'], 
                                ['bp0', 'bp1', 'bp2', 'bp3', '0', '0', 'bp6', 'bp7'], 
                                ['0', '0', '0', '0', '0', 'bp5', '0', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', '0'], 
                                ['0', '0', '0', 'wkn1', '0', '0', '0', '0'], 
                                ['0', '0', '0', '0', '0', '0', '0', 'wp7'], 
                                ['wp0', 'wp1', 'wp2', '0', 'wp4', 'wp5', 'wp6', '0'], 
                                ['wr1', '0', 'wb1', '0', 'wK', 'wb2', 'wkn2', 'wr2']]
                                , [True, True], [True, True])




new_board.printBoard()

