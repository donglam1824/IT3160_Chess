import pygame
from ChessBoardClass import ChessBoard
from PiecePicture import PieceImage

class Interface:
    "Vẽ dao diện cho game"
    WIDTH = 1000    #kich thuoc man hinh
    HEIGHT = 800
    fps = 60
    selection = 100
    captured_white_pieces = []
    captured_black_pieces = []
    
    def __init__(self, board = ChessBoard):
        pygame.init()
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.screen.fill('gray')
        pygame.display.set_caption('Bài tập lớn: Cờ vua')
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.medium_font = pygame.font.Font('freesansbold.ttf', 40)
        self.big_font = pygame.font.Font('freesansbold.ttf', 50)
        self.timer = pygame.time.Clock()
        self.board = board
        self.counter = 0
        self.turn_step = 0
        """Trạng thái bàn cờ theo các giá trị: 
        0: Bên White, chưa chọn quân
        1: Bên White, chuẩn bị đi
        2: Bên Black, chưa chọn quân
        3: Bên Black, chuẩn bị đi
        """

    def draw_board(self):
        "Vẽ bàn cờ"
        LIGHT_SQUARE_COLOR = (209, 139, 71)  # Màu ô vuông
        DARK_SQUARE_COLOR = (255, 206, 158)
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(self.screen, LIGHT_SQUARE_COLOR, [col * 100, row * 100, 100, 100])
                else:
                    pygame.draw.rect(self.screen, DARK_SQUARE_COLOR, [col * 100, row * 100, 100, 100])

        pygame.draw.rect(self.screen, 'gray', [0, 800, self.WIDTH, 100])
        pygame.draw.rect(self.screen, 'gold', [0, 800, self.WIDTH, 100], 5)
        pygame.draw.rect(self.screen, 'gold', [800, 0, 200, self.HEIGHT], 5)

        status_text = ['Trắng đang chọn quân', 'Trắng đang chọn nước đi',
                        'Đen đang chọn quân', 'Đen đang chọn nước đi']
        #hiện text tương ứng với trạng thái 
        self.screen.blit(self.big_font.render(status_text[self.turn_step], True, 'black'), (20, 820))
            
        for i in range(9):
                pygame.draw.line(self.screen, 'black', (0, 100 * i), (800, 100 * i), 2)
                pygame.draw.line(self.screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        self.screen.blit(self.medium_font.render('FORFEIT', True, 'black'), (810, 830))

    def draw_pieces(self):
        "Vẽ quân cờ"
        white_pieces = self.board.player_white.chess_pieces
        image = PieceImage()
        for i in range(len(white_pieces)):
            piece = white_pieces[i]
            index = image.piece_list.index(piece.name)
            if piece.name == "Pawn":
                self.screen.blit(image.white_pawn, (piece.position[1] * 100 + 22, piece.position[0] * 100 + 30))
            else:
                self.screen.blit(image.white_images[index], (piece.position[1] * 100 + 10, piece.position[0] * 100 + 10))
                    

        black_pieces = self.board.player_black.chess_pieces
        for i in range(len(black_pieces)):
            piece = black_pieces[i]
            index = image.piece_list.index(piece.name)
            if piece.name == "Pawn":
                self.screen.blit(image.black_pawn, 
                    (piece.position[1] * 100 + 22, piece.position[0] * 100 + 30))
            else:
                self.screen.blit(image.black_images[index], 
                    (piece.position[1] * 100 + 10, piece.position[0] * 100 + 10))
                    
    
    # vẽ nước hợp lệ trên bàn cờ và quân cờ đang được chọn
    def draw_valid(self, moves ,choosen_piece):
        if type(choosen_piece) is not str:
            if self.turn_step < 2:
                color = 'red'
                pygame.draw.rect(self.screen, 'red', 
                                [choosen_piece.position[1] * 100 + 1, choosen_piece.position[0] * 100 + 1, 100, 100], 2)
            else:
                color = 'blue'
                pygame.draw.rect(self.screen, 'blue', 
                        [choosen_piece.position[1] * 100 + 1, choosen_piece.position[0] * 100 + 1, 100, 100], 2)
            for mv in moves:
                pygame.draw.circle(self.screen, color, (mv[1] * 100 + 50, mv[0] * 100 + 50), 5)

    # vẽ quân bắt được ở cạnh bàn cờ
    def draw_captured(self):
        image = PieceImage()
        for i in range(len(self.captured_white_pieces)):
            captured_piece = self.captured_white_pieces[i]
            index = image.piece_list.index(captured_piece)
            self.screen.blit(image.small_black_images[index], (825, 5 + 50 * i))
        for i in range(len(self.captured_black_pieces)):
            captured_piece = self.captured_black_pieces[i]
            index = image.piece_list.index(captured_piece)
            image.screen.blit(image.small_white_images[index], (925, 5 + 50 * i))


    # ô vua nhấp nháy nếu bị chiếu
    def draw_check(self):
        image = PieceImage()
        if self.turn_step < 2:
            king_location = self.board.player_white.king.position
        else:
            king_location = self.board.player_black.king.position
        if(self.counter < 15):
            pygame.draw.rect(self.screen, 'dark red', [king_location[1] * 100 + 1,
                        king_location[0] * 100 + 1, 100, 100], 5)


    def draw_game_over(self, winner):
        pygame.draw.rect(self.screen, 'black', [200, 200, 400, 70])
        self.screen.blit(self.font.render(f'{winner} giành chiến thắng!', True, 'white'), (210, 210))
        self.screen.blit(self.font.render(f'Press ENTER to Restart!',True, 'white'), (210, 240))
        


        
