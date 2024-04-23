import pygame, time

from Base.ChessBoardClass import ChessBoard
from Base.ChessInterface import Interface
from MiniMaxClass import Minimax

board = ChessBoard()
interface = Interface(board)
minimax_black = Minimax("Black")
run = True
pygame.display.flip()
movable_tile = []
choosen_piece = ""

while run:
    interface.timer.tick(interface.fps)
    interface.draw_board()
    interface.draw_pieces()
    #interface.draw_check()
    if interface.counter < 30:
        interface.counter += 1
    else:
        interface.counter = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Xác định vị trí chuột trên bàn cờ
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = [y_coord, x_coord]
            if(interface.turn_step == 1 and click_coords in movable_tile):
                #Di chuyển quân cờ trên các ô màu đỏ
                choosen_piece.makeMove(click_coords ,board)
                movable_tile = []
                interface.turn_step = 2
                continue
            if(interface.turn_step <= 1):
                #Turn của bên White đi
                choosen_piece = board.locatePiece(click_coords)
                if(choosen_piece in board.player_black.chess_pieces): 
                    choosen_piece = ""
                    continue
                #Tìm các nước đi
                try:
                    movable_tile = choosen_piece.displayMovableTile(board)
                except AttributeError: pass #Chọn ô ko có quân cờ
                interface.turn_step = 1
        if(interface.turn_step > 1 and interface.turn_step <= 3):
                tic = time.perf_counter()
                best = minimax_black.miniMax(0, "", "", True, 3, board, -float("Inf"), float("Inf"))
                print(time.perf_counter() - tic, "seconds")
                board.player_black.chess_pieces[best[1]].makeMove(best[2], board)
                interface.turn_step = 0
    interface.draw_valid(movable_tile, choosen_piece)
    pygame.display.update()
pygame.quit()