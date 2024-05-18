from Base.ChessBoardClass import ChessBoard
from Minimax.MiniMaxClass import Minimax
import time


def printValue():
    print("Black")
    for piece in board.player_black.chess_pieces:
        print(piece.name, piece.position ,piece.value)
    print("White")
    for piece in board.player_white.chess_pieces:
        print(piece.name, piece.position, piece.value)

board = ChessBoard()
board.player_black.paws[0].makeMove([3, 0], board)
board.player_white.paws[3].makeMove([3, 3], board)
board.player_black.queen.makeMove([3, 1], board)


board.printBoard()
print(board.player_black.queen.displayMovableTile(board))
print(board.kingIsChecked())






