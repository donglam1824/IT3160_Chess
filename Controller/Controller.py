from copy import deepcopy
from Base.ChessBoard import ChessBoard
from Controller.Interface import Interface
from Minimax.MiniMaxClass import Minimax
from soundgame import SoundManager
import pygame


class Controller:
    sound_manager = SoundManager()
    minimax_black = Minimax("Black", 3)
    minimax_white = Minimax("White", 2)
    def __init__(self, enable_white_AI: bool, enable_black_AI: bool):
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound('Chess_Image/chess_move.mp3')
        self.capture_sound = pygame.mixer.Sound('Chess_Image/chess_capture.mp3')
        self.check_sound = pygame.mixer.Sound('Chess_Image/check.mp3')
        self.white_AI = False
        self.black_AI = False
        self.possible_move = [[], []]
        self.makeNewGame(enable_white_AI, enable_black_AI, 3, 3)
        self.movable_tile = []
        self.choosen_piece = ""
        self.king_is_checked = [False, ""]
        self.turn_step = 0
    
    def makeNewGame(self, enable_white_AI : bool, enable_black_AI: bool, 
                    max_depth_white : int, max_depth_black : int):
        "Tạo game mới, có thể lựa chọn AI cho 2 bên"
        self.board = ChessBoard()
        self.interface = Interface(self.board)
        self.run = True
        self.king_is_checked = [False, ""]
        self.game_ended = self.board.gameCondition()
        self.possible_move = [self.game_ended[1], self.game_ended[2]]

        if(enable_white_AI == True): 
            self.white_AI = True
            self.minimax_white.updateDepth(max_depth_black)
        if(enable_black_AI == True): 
            self.black_AI = True
            self.minimax_black.updateDepth(max_depth_black)


    def onFrameUpdate(self):
        self.interface.timer.tick(self.interface.fps)
        self.interface.draw_board()
        self.interface.draw_pieces()
        self.interface.draw_valid(self.movable_tile, self.choosen_piece, self.turn_step)
        if(self.king_is_checked[0] == True): self.interface.draw_check(self.king_is_checked[1])
        if(self.game_ended[0] == True): self.interface.draw_game_over(self.game_ended[1])

        self.aiMakeMove()
        self.interface.draw_captured()
        if self.interface.counter < 30:
            self.interface.counter += 1
        else:
            self.interface.counter = 0
    
    def onClick(self, click_coords):
        "Khi người chơi click chuột chọn nước đi"
        if(self.white_AI == False):
            #Luợt của bên White
            if(self.turn_step == 1 and click_coords in self.movable_tile):
                #Di chuyển quân cờ trên các ô màu đỏ
                self.choosen_piece.makeMove(click_coords ,self.board)
                self.turn_step = 2
                self.onMove()
                self.sound_manager.play_move_sound ()
                return
            if(self.turn_step <= 1):
                #Turn của bên White đi
                self.choosen_piece = self.board.locatePiece(click_coords)
                if(self.choosen_piece in self.board.player_black.chess_pieces): 
                    self.choosen_piece = ""
                    return
                #Tìm các nước đi
                try:
                    self.movable_tile = self.choosen_piece.displayMovableTile(self.board)
                except AttributeError: pass #Chọn ô ko có quân cờ
                self.turn_step = 1
                movable_tile = deepcopy(self.movable_tile)
                for move in movable_tile:
                    if(self.possible_move[0].count([self.choosen_piece ,move]) <= 0):
                        self.movable_tile.remove(move)
        if(self.black_AI == False):
            #Lượt của bên Black
            if(self.turn_step == 3 and click_coords in self.movable_tile):
                #Di chuyển quân cờ trên các ô màu đỏ
                self.choosen_piece.makeMove(click_coords ,self.board)
                self.turn_step = 0
                self.onMove()
                self.sound_manager.play_move_sound ()
                return
            if(self.turn_step <= 3 and self.turn_step > 1):
                #Turn của bên White đi
                self.choosen_piece = self.board.locatePiece(click_coords)
                if(self.choosen_piece in self.board.player_white.chess_pieces): 
                    self.choosen_piece = ""
                    return
                #Tìm các nước đi
                try:
                    self.movable_tile = self.choosen_piece.displayMovableTile(self.board)
                except AttributeError: pass #Chọn ô ko có quân cờ
                self.turn_step = 3
                movable_tile = deepcopy(self.movable_tile)
                for move in movable_tile:
                    if(self.possible_move[1].count([self.choosen_piece ,move]) <= 0):
                        self.movable_tile.remove(move)
        

    def aiMakeMove(self):
        if(self.turn_step <= 1 and self.white_AI == True):
            best = self.minimax_white.miniMax(0, "", "", True, self.board, -float("Inf"), float("Inf"))
            self.board.player_white.chess_pieces[best[1]].makeMove(best[2], self.board)
            self.turn_step = 2
            self.onMove()
            self.sound_manager.play_move_sound ()
            return
        if(self.turn_step > 1 and self.turn_step <= 3 and self.black_AI == True):
            best = self.minimax_black.miniMax(0, "", "", True, self.board, -float("Inf"), float("Inf"))
            self.board.player_black.chess_pieces[best[1]].makeMove(best[2], self.board)
            self.turn_step = 0
            self.onMove()
            self.sound_manager.play_move_sound ()
            return
    
    def onMove(self):
        "Khi người chơi thực hiện di chuyển"
        self.movable_tile = []
        self.king_is_checked = self.board.kingIsChecked()
        self.game_ended = self.board.gameCondition()
        if(self.game_ended[0] == False): 
            self.possible_move = [self.game_ended[1], self.game_ended[2]]
        if self.board.pieceJustCaptured():  # Kiểm tra trực tiếp, không cần qua biến tạm
            self.capture_sound.play()
            self.board.last_captured_piece = None  # Reset last_captured_piece
        elif self.king_is_checked[0]:
            self.check_sound.play()
        else:
            self.move_sound.play()