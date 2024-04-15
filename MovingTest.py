from ChessBoardClass import ChessBoard

board = ChessBoard()

while(1):
    board.printBoard()
    print(board.evaluateBoard("White"))
    print(board.endGame())
    choosen_tile = [int(i) for i in input("Choose tile:").split()]
    choosen_piece = ""
    for piece in board.player_white.chess_pieces:
        if(choosen_tile == piece.position):
            choosen_piece = piece
            break
    if(choosen_piece == ""):
        for piece in board.player_black.chess_pieces:
            if(choosen_tile == piece.position):
                choosen_piece = piece
                break
    print(choosen_piece.name , choosen_piece.displayMovableTile(board))
    move = [int(i) for i in input("Make your move:").split()]
    choosen_piece.makeMove(move, board)