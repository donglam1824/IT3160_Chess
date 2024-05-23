import pygame

from Controller.Interface.OpenScreen import OpenScreen
import pygame

def main():
    pygame.init()
    controller = None
    open_screen = OpenScreen()
    controller = open_screen.getChoosenMode()
    # Bắt đầu vòng lặp chính của trò chơi cờ
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

if __name__ == "__main__":
    main()
