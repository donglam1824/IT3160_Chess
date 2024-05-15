from Base.ChessBoardClass import ChessBoard
from Minimax.MiniMaxClass import Minimax
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
#print(board.player_black.paws[0].score_table)
#printMoves()
#printPieces()
print(board.player_white.paws[3].linked_pieces)
board.player_white.paws[3].makeMove([3,3], board)
board.player_black.knight_1.makeMove([5,2], board)
#board.printBoard()
#print(board.player_white.queen.available_move)
board.player_black.knight_1.makeMove([3,3], board)
print(board.player_black.knight_1.linked_pieces)
#board.printBoard()
print(board.player_white.queen.available_move)
#print(board.player_white.paws[3].linked_pieces)
#print(board.player_white.queen.linked_pieces)
#print(board.player_black.knight_1.linked_pieces)





