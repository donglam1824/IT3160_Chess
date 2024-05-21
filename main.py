import pygame

from Base.ChessBoardClass import ChessBoard
from Controler.ChessInterface import Interface
from Minimax.MiniMaxClass import Minimax
from Controler.Controller import Controller  # Nhập lớp Controller của bạn

def main():
    pygame.init()
    icon = pygame.image.load("Chess_Image\icon.jpg")
    pygame.display.set_icon(icon)

    screen_width, screen_height = 1000, 800
    screen = pygame.display.set_mode((screen_width, screen_height))  # Kích thước cửa sổ menu
    pygame.display.set_caption("Chọn Chế Độ Chơi")
    original_background_image = pygame.image.load(r"Chess_Image\Menu.jpg").convert()
    background_image = pygame.transform.scale(original_background_image, (screen_width, screen_height))
    font = pygame.font.SysFont(None, 30)
    button_color = (165, 42, 42)  # Màu nâu đỏ
    button_hover_color = (139, 0, 0)  # Màu nâu đậm
    button_border_color = (0, 0, 0)  # Màu đen
    text_color = (255, 255, 255)  # Màu trắng
    border_width = 2
    corner_radius = 10

    # Các nút chọn chế độ chơi
    buttons = [
        {"text": "Player vs Player", "rect": pygame.Rect(400, 200, 200, 50), "AI": (False, False)},
        {"text": "Player vs Bot", "rect": pygame.Rect(400, 320, 200, 50), "AI": (False, True)},
        {"text": "Bot vs Player", "rect": pygame.Rect(400, 440, 200, 50), "AI": (True, False)},
        {"text": "Bot vs Bot", "rect": pygame.Rect(400, 560, 200, 50), "AI": (True, True)}
    ]

    running = True
    controller = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        # Tạo Controller với chế độ chơi đã chọn
                        controller = Controller(button["AI"][0], button["AI"][1])
                        running = False  # Thoát khỏi vòng lặp menu
                        break  # Thoát khỏi vòng lặp duyệt nút
        
        if (controller == None):
            screen.blit(background_image, (0, 0))


        for button in buttons:
        # Hiệu ứng hover
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, button_hover_color, button["rect"], border_radius=corner_radius)
            else:
                pygame.draw.rect(screen, button_color, button["rect"], border_radius=corner_radius)

            # Viền nút
            pygame.draw.rect(screen, button_border_color, button["rect"], border_width, border_radius=corner_radius)
            # Chữ trên nút
            text_surface = font.render(button["text"], True, text_color)  # Màu chữ trắng
            text_rect = text_surface.get_rect(center=button["rect"].center)
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

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
