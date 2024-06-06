from Base.ChessBoard import ChessBoard
from MonteCarlo.MonteCarloUser import MonteCarloUser


board = ChessBoard()
monte_carlo_user = MonteCarloUser()

moving_piece = board.player_white.paws[2]
monte_carlo_user.moveToNode(moving_piece.position, [5, 2])
moving_piece.makeMove([5, 2], board)

move = monte_carlo_user.findBestMove()
moving_piece = board.locatePiece(move[0])
moving_piece.makeMove(move[1], board)
board.printBoard()