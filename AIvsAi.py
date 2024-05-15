import time
import pygame

from Minimax.MiniMaxClass import Minimax
from Base.ChessBoardClass import ChessBoard
from Base.ChessInterface import Interface

current_board = ChessBoard()
minimax_white = Minimax("White")
minimax_black = Minimax("Black")
interface = Interface(current_board)
run = True
pygame.display.flip()
movable_tile = []
choosen_piece = ""
start = False

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
            start = True
        if(current_board.endGame()[0] == False and start == True):
            #tic = time.perf_counter()
            if(interface.turn_step <= 1):
                best = minimax_white.miniMax(0, "", "", True, 3, current_board, -float("Inf"), float("Inf"))
                current_board.player_white.chess_pieces[best[1]].makeMove(best[2], current_board)
                interface.turn_step = 2
                print("White point:" , current_board.evaluateBoard("White"), "turn: White")
            elif(interface.turn_step > 1 and interface.turn_step <= 3):
                best = minimax_black.miniMax(0, "", "", True, 3, current_board, -float("Inf"), float("Inf"))
                current_board.player_black.chess_pieces[best[1]].makeMove(best[2], current_board)
                interface.turn_step = 0
                print("White point:" , current_board.evaluateBoard("White"), "turn: Black")
            #print(time.perf_counter() - tic, "second")
    
    #interface.draw_valid(movable_tile, choosen_piece)
    pygame.display.update()
pygame.quit()
