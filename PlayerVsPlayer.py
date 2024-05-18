import pygame

from Base.ChessBoardClass import ChessBoard
from Controler.ChessInterface import Interface

board = ChessBoard()
interface = Interface(board)
run = True
king_is_checked = [False, ""]
game_ended = False
pygame.display.flip()
movable_tile = []
choosen_piece = ""

while run:
    interface.timer.tick(interface.fps)
    interface.draw_board()
    interface.draw_pieces()
    if(king_is_checked[0] == True): interface.draw_check(king_is_checked[1])
    interface.draw_captured()
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
                king_is_checked = board.kingIsChecked()
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
            if(interface.turn_step == 3 and click_coords in movable_tile):
                #Di chuyển quân cờ trên các ô màu đỏ
                choosen_piece.makeMove(click_coords ,board)
                movable_tile = []
                interface.turn_step = 0
                king_is_checked = board.kingIsChecked()
                continue
            if(interface.turn_step <= 3 and interface.turn_step > 1):
                #Turn của bên White đi
                choosen_piece = board.locatePiece(click_coords)
                if(choosen_piece in board.player_white.chess_pieces): 
                    choosen_piece = ""
                    continue
                #Tìm các nước đi
                try:
                    movable_tile = choosen_piece.displayMovableTile(board)
                except AttributeError: pass #Chọn ô ko có quân cờ
                interface.turn_step = 3
    interface.draw_valid(movable_tile, choosen_piece)
    pygame.display.update()
pygame.quit()