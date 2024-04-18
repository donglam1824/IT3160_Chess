import pygame

from MiniMaxClass import Minimax
from ChessBoardClass import ChessBoard
from ChessInterface import Interface

current_board = ChessBoard()
minimax_white = Minimax("White")
minimax_black = Minimax("Black")
interface = Interface(current_board)
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
    if(current_board.endGame()[0] == False):
        if(interface.turn_step <= 1):
            best = minimax_white.miniMax(0, "", "", True, 1, current_board, -float("Inf"), float("Inf"))
            current_board.player_white.chess_pieces[best[1]].makeMove(best[2], current_board)
            interface.turn_step = 2
        elif(interface.turn_step > 1 and interface.turn_step <= 3):
            best = minimax_black.miniMax(0, "", "", True, 3, current_board, -float("Inf"), float("Inf"))
            current_board.player_black.chess_pieces[best[1]].makeMove(best[2], current_board)
            interface.turn_step = 0
    else:
        interface.draw_game_over(current_board.endGame()[1])
    
    #interface.draw_valid(movable_tile, choosen_piece)
    pygame.display.update()
pygame.quit()
