import pygame

from Minimax.MiniMaxClass import Minimax
from Base.ChessBoard import ChessBoard
from Controller.Interface import Interface
from Controller.Controller import Controller

controller = Controller()
pygame.display.flip()

while(controller.run == True):
    controller.onFrameUpdate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #Xác định vị trí chuột trên bàn cờ
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = [y_coord, x_coord]
            controller.onClick(click_coords)
    
    pygame.display.update()

