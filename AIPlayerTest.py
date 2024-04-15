from MiniMax import Minimax
from ChessBoardClass import ChessBoard

current_board = ChessBoard()
minimax_white = Minimax("White")
minimax_black = Minimax("Black")
turn = "White"
while(current_board.endGame()[0] == False):
    current_board.printBoard()
    if(turn == "White"):
        best = minimax_white.miniMax(0, "", "", True, 3, current_board, -float("Inf"), float("Inf"))
        current_board.player_white.chess_pieces[best[1]].makeMove(best[2], current_board)
        turn = "Black"
    elif(turn == "Black"):
        best = minimax_black.miniMax(0, "", "", True, 2, current_board, -float("Inf"), float("Inf"))
        current_board.player_black.chess_pieces[best[1]].makeMove(best[2], current_board)
        turn = "White"
current_board.printBoard()
winner = current_board.endGame()[1]
print(winner, "is the winner")
