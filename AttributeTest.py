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
board.player_black.paws[4].makeMove([3,3], board)
board.player_white.queen.makeMove([3,4], board)


board.printBoard()
print(board.gameOver())






