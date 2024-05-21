import pygame

from Base.ChessBoardClass import ChessBoard
from Controler.ChessInterface import Interface
from Minimax.MiniMaxClass import Minimax
from Controler.Controller import Controller  # Nhập lớp Controller của bạn

def main():
    pygame.init()

    screen = pygame.display.set_mode((400, 360))  # Kích thước cửa sổ menu
    pygame.display.set_caption("Chọn Chế Độ Chơi Cờ")

    font = pygame.font.SysFont(None, 30)

    # Các nút chọn chế độ chơi
    buttons = [
        {"text": "Player vs Player", "rect": pygame.Rect(100, 50, 200, 50), "AI": (False, False)},
        {"text": "Player vs Bot", "rect": pygame.Rect(100, 120, 200, 50), "AI": (False, True)},
        {"text": "Bot vs Player", "rect": pygame.Rect(100, 190, 200, 50), "AI": (True, False)},
        {"text": "Bot vs Bot", "rect": pygame.Rect(100, 260, 200, 50), "AI": (True, True)}
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

        for button in buttons:
            pygame.draw.rect(screen, (0, 0, 255), button["rect"])  # Vẽ nút màu xanh
            text_surface = font.render(button["text"], True, (255, 255, 255))  # Màu chữ trắng
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
