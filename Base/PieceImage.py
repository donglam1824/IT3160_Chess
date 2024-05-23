import pygame

image_folder = 'Resource/Chess_Image/'
class PieceImage:
    #quân đen
    black_queen = pygame.image.load(image_folder + 'black_queen.png')
    black_queen = pygame.transform.scale(black_queen, (80, 80))
    black_queen_small = pygame.transform.scale(black_queen, (45, 45))

    black_king = pygame.image.load(image_folder + 'black_king.png')
    black_king = pygame.transform.scale(black_king, (80, 80))
    black_king_small = pygame.transform.scale(black_king, (45, 45))

    black_rook = pygame.image.load(image_folder + 'black_rock.png')
    black_rook = pygame.transform.scale(black_rook, (80, 80))
    black_rook_small = pygame.transform.scale(black_rook, (45, 45))

    black_bishop = pygame.image.load(image_folder + 'black_bishop.png')
    black_bishop = pygame.transform.scale(black_bishop, (80, 80))
    black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))

    black_knight = pygame.image.load(image_folder + 'black_knight.png')
    black_knight = pygame.transform.scale(black_knight, (80, 80))
    black_knight_small = pygame.transform.scale(black_knight, (45, 45))

    black_pawn = pygame.image.load(image_folder + 'black_pawn.png')
    black_pawn = pygame.transform.scale(black_pawn, (65, 65))
    black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))


    #quân trắng
    white_queen = pygame.image.load(image_folder + 'white_queen.png')
    white_queen = pygame.transform.scale(white_queen, (80, 80))
    white_queen_small = pygame.transform.scale(white_queen, (45, 45))

    white_king = pygame.image.load(image_folder + 'white_king.png')
    white_king = pygame.transform.scale(white_king, (80, 80))
    white_king_small = pygame.transform.scale(white_king, (45, 45))

    white_rook = pygame.image.load(image_folder + 'white_rock.png')
    white_rook = pygame.transform.scale(white_rook, (80, 80))
    white_rook_small = pygame.transform.scale(white_rook, (45, 45))

    white_bishop = pygame.image.load(image_folder + 'white_bishop.png')
    white_bishop = pygame.transform.scale(white_bishop, (80, 80))
    white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))

    white_knight = pygame.image.load(image_folder + 'white_knight.png')
    white_knight = pygame.transform.scale(white_knight, (80, 80))
    white_knight_small = pygame.transform.scale(white_knight, (45, 45))

    white_pawn = pygame.image.load(image_folder + 'white_pawn.png')
    white_pawn = pygame.transform.scale(white_pawn, (65, 65))
    white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))

    white_images = []
    small_white_images = []

    black_images = []
    small_black_images = []

    piece_list = ["Pawn", "Queen", "King", "Knight", "Rock", "Bishop"]
    def __init__(self):
        self.white_images = [self.white_pawn, self.white_queen, self.white_king, 
                        self.white_knight, self.white_rook, self.white_bishop]
        
        self.small_white_images = [self.white_pawn_small, self.white_queen_small, self.white_king_small, 
                              self.white_knight_small, self.white_rook_small, self.white_bishop_small]
        
        self.black_images = [self.black_pawn, self.black_queen, self.black_king,
                    self.black_knight, self.black_rook, self.black_bishop]
        
        self.small_black_images = [self.black_pawn_small, self.black_queen_small, self.black_king_small, 
                              self.black_knight_small, self.black_rook_small, self.black_bishop_small]