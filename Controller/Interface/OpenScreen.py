import pygame
from Controller.Interface.SoundGame import SoundManager
from Controller.Controller import Controller

pygame.init()

image_folder = "Controller/Interface/image/"

icon = pygame.image.load(image_folder + "icon.jpg")
sound_manager = SoundManager()
sound_manager.playBackGroundMusic(-1)
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))  # Kích thước cửa sổ menu
original_background_image = pygame.image.load(image_folder + "Menu.jpg").convert()
background_image = pygame.transform.scale(original_background_image, (screen_width, screen_height))
font = pygame.font.SysFont(None, 30)
button_color = (255, 255, 255)  # Màu trắng
button_hover_color = (191, 191, 191)  # Màu xám sáng
button_border_color = (0, 0, 0)  # Màu đen
text_color = (0, 0, 0)  # Màu đen
border_width = 2
corner_radius = 10

class OpenScreen:

    # Các nút chọn chế độ chơi
    buttons = [
    {"text": "Player vs Player", "rect": pygame.Rect(400, 200, 200, 50), "AI": (False, False)},
    {"text": "Player vs Bot", "rect": pygame.Rect(400, 320, 200, 50), "AI": (False, True)},
    {"text": "Bot vs Player", "rect": pygame.Rect(400, 440, 200, 50), "AI": (True, False)},
    {"text": "Bot vs Bot", "rect": pygame.Rect(400, 560, 200, 50), "AI": (True, True)}]

    def __init__(self):
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Chọn Chế Độ Chơi")
        self.controller = None
        self.displayingScreen()
    
    def displayingScreen(self):
        running = True
        pygame.display.flip()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            # Tạo Controller với chế độ chơi đã chọn
                            self.controller = Controller(button["AI"][0], button["AI"][1])
                            running = False  # Thoát khỏi vòng lặp menu
                            break  # Thoát khỏi vòng lặp duyệt nút
            
            if (self.controller == None):
                screen.blit(background_image, (0, 0))
                
            for button in self.buttons:
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

            pygame.display.update()

    def getChoosenMode(self):
        return self.controller
        


        