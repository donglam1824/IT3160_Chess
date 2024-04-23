from Base.ChessBoardClass import ChessBoard
from MiniMaxClass import Minimax
import time

def printMoves():
    print("Black")
    for piece in board.player_black.chess_pieces:
        print(piece.name, piece.position , piece.available_move)
    print("White")
    for piece in board.player_white.chess_pieces:
        print(piece.name, piece.position, piece.available_move)

def printPieces():
    print("Black")
    for piece in board.player_black.chess_pieces:
        print(piece.name, piece.position ,piece.linked_pieces)
    print("White")
    for piece in board.player_white.chess_pieces:
        print(piece.name, piece.position, piece.linked_pieces)

def printValue():
    print("Black")
    for piece in board.player_black.chess_pieces:
        print(piece.name, piece.position ,piece.value)
    print("White")
    for piece in board.player_white.chess_pieces:
        print(piece.name, piece.position, piece.value)

board = ChessBoard()
board.player_black.knight_1.makeMove([5, 2], board)
board.printBoard()
#printMoves()
#printPieces()
printValue()