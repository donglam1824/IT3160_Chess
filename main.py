import pygame

from Controller.Controller import Controller
from Controller.Interface.OpenScreen import OpenScreen
import pygame

pygame.init()
def main():
    controller : Controller
    open_screen = OpenScreen()
    controller = open_screen.getChoosenMode()
    # Bắt đầu vòng lặp chính của trò chơi cờ
    while(controller.run == True):
        controller.onFrameUpdate()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and controller.game_ended[0] == False:
            #Xác định vị trí chuột trên bàn cờ
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = [y_coord, x_coord]
                controller.onClick(click_coords)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and controller.game_ended[0] == True:
               #Về màn hình chính, xóa hết các đối tượng và gọi lại main
                controller == None
                open_screen == None
                main()
                return

if __name__ == "__main__":
    main()
