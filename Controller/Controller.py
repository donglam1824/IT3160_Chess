from copy import copy, deepcopy
import random
from Base.ChessBoard import ChessBoard
from Controller.Interface.GameInterface import GameInterface
from Minimax.WhiteMax import WhiteMax
from Minimax.BlackMax import BlackMax
from MonteCarlo.MonteCarloUser import MonteCarloUser
from Controller.Interface.SoundGame import SoundManager

import pygame



class Controller:
    sound_manager = SoundManager()
    minimax_black = BlackMax(3)
    minimax_white = WhiteMax(2)
    def __init__(self, enable_white_AI: bool, enable_black_AI: bool, enable_MCTS_white : bool, enable_MCTS_black : bool):
        pygame.mixer.init()
        self.white_AI = False
        self.black_AI = False
        self.enable_MCTS_white = enable_MCTS_white
        self.enable_MCTS_black = enable_MCTS_black
        self.possible_move_white = []
        self.possible_move_black = []
        self.previous_move = {"old position" : [], "new position" : []}
        self.makeNewGame(enable_white_AI, enable_black_AI, 3, 4)
        self.monte_carlo_user = MonteCarloUser()
        self.movable_tile = []
        self.choosen_piece = None
        self.king_is_checked = [False, ""]
        self.turn_step = 0
        self.move_count = 0 # For the fifty-move rules
    
    def makeNewGame(self, enable_white_AI : bool, enable_black_AI: bool,
                    max_depth_white : int, max_depth_black : int):
        "Tạo game mới, có thể lựa chọn AI cho 2 bên"
        self.board = ChessBoard()
        self.interface = GameInterface(self.board)
        self.run = True
        self.king_is_checked = [False, ""]
        self.game_ended = [False, ""]
        self.possible_move_white = self.board.getPossibleMoveWhite()
        self.possible_move_black = self.board.getPossibleMoveBlack()
        self.turn_step = 0
        if(enable_white_AI == True): 
            self.white_AI = True
            self.minimax_white.updateDepth(max_depth_white)
        if(enable_black_AI == True): 
            self.black_AI = True
            self.minimax_black.updateDepth(max_depth_black)


    def onFrameUpdate(self):
        self.interface.timer.tick(self.interface.fps)
        self.interface.draw_board()
        self.interface.draw_pieces()
        self.interface.draw_valid(self.movable_tile, self.choosen_piece, self.turn_step)
        self.interface.draw_captured()
        if(self.king_is_checked[0] == True): self.interface.draw_check(self.king_is_checked[1])
        if(self.game_ended[0] == True): self.interface.draw_game_over(self.game_ended[1])
        pygame.display.update()
        
        if(self.game_ended[0] == False): self.aiMakeMove()
        if self.interface.counter < 30:
            self.interface.counter += 1
        else:
            self.interface.counter = 0
        pygame.display.update()
    def onClick(self, click_coords):
        "Khi người chơi click chuột chọn nước đi"
        if(click_coords[0] not in range(0, 8) or click_coords[1] not in range(0, 8)):
            return
        if(self.white_AI == False):
            #Luợt của bên White
            if(self.turn_step == 1 and (click_coords in self.movable_tile) and self.choosen_piece != None):
                #Di chuyển quân cờ trên các ô màu đỏ
                self.previous_move["old position"] = self.choosen_piece.position
                self.choosen_piece.makeMove(click_coords ,self.board)
                self.turn_step = 2
                self.onMove()
                return
            if(self.turn_step <= 1):
                #Turn của bên White đi
                self.choosen_piece = self.board.locatePiece(click_coords)
                if(self.choosen_piece in self.board.player_black.chess_pieces or self.choosen_piece == None): 
                    self.choosen_piece = None
                    return
                #Tìm các nước đi
                self.movable_tile = self.choosen_piece.displayMovableTile(self.board)
                self.turn_step = 1
                movable_tile = copy(self.movable_tile)
                for move in movable_tile:
                    if([self.choosen_piece ,move] not in self.possible_move_white):
                        self.movable_tile.remove(move)
        if(self.black_AI == False):
            #Lượt của bên Black
            if(self.turn_step == 3 and (click_coords in self.movable_tile) and self.choosen_piece != None):
                #Di chuyển quân cờ trên các ô màu đỏ
                self.previous_move["old position"] = self.choosen_piece.position
                self.choosen_piece.makeMove(click_coords ,self.board)
                self.turn_step = 0
                self.onMove()
                return
            if(self.turn_step <= 3 and self.turn_step > 1):
                #Turn của bên Black đi
                self.choosen_piece = self.board.locatePiece(click_coords)
                if(self.choosen_piece in self.board.player_white.chess_pieces or self.choosen_piece == None): 
                    self.choosen_piece = None
                    return
                #Tìm các nước đi
                self.movable_tile = self.choosen_piece.displayMovableTile(self.board)
                self.turn_step = 3
                movable_tile = copy(self.movable_tile)
                for move in movable_tile:
                    if([self.choosen_piece ,move] not in self.possible_move_black):
                        self.movable_tile.remove(move)
        

    def aiMakeMove(self):
        "AI thực hiện nước đi"
        #Minimax tìm nước đi
        if(self.turn_step <= 1 and self.white_AI == True and self.enable_MCTS_white == False):
            try:
                best = self.minimax_white.miniMax(0, "", "", True, self.board, -float("Inf"), float("Inf"))
                self.choosen_piece = self.board.player_white.chess_pieces[best[1]]
                self.previous_move["old position"] = self.choosen_piece.position
                self.choosen_piece.makeMove(best[2], self.board)
                self.turn_step = 2
                self.onMove()
                return
            except Exception:
                #Error in finding move, make a random move instead
                print("Error in finding move, make a random move instead")
                choosen_move = random.choice(self.possible_move_white)
                self.choosen_piece == choosen_move[0]
                self.previous_move["old position"] = self.choosen_piece.position
                self.makeMove(choosen_move[1], self.board)
                self.turn_step = 2
                self.onMove()
                return
        if(self.turn_step > 1 and self.turn_step <= 3 and self.black_AI == True and self.enable_MCTS_black == False):
            try:
                best = self.minimax_black.miniMax(0, "", "", True, self.board, -float("Inf"), float("Inf"))
                self.choosen_piece = self.board.player_black.chess_pieces[best[1]]
                self.previous_move["old position"] = self.choosen_piece.position
                self.choosen_piece.makeMove(best[2], self.board)
                self.turn_step = 0
                self.onMove()
                return
            except Exception:
                #Error in finding move, make a random move instead
                print("Error in finding move, make a random move instead")
                choosen_move = random.choice(self.possible_move_white)
                self.choosen_piece == choosen_move[0]
                self.previous_move["old position"] = self.choosen_piece.position
                self.makeMove(choosen_move[1], self.board)
                self.turn_step = 0
                self.onMove()
                return
        #Monte Carlo tìm nước đi
        if(self.turn_step <= 1 and self.white_AI == True and self.enable_MCTS_white == True):
            best = self.monte_carlo_user.findBestMove()
            self.choosen_piece = self.board.locatePiece(best[0])
            self.previous_move["old position"] = best[0]
            self.choosen_piece.makeMove(best[1], self.board)
            self.turn_step = 2
            self.onMove()
            return
        if(self.turn_step > 1 and self.turn_step <= 3 and self.black_AI == True and self.enable_MCTS_black == True):
            best = self.monte_carlo_user.findBestMove()
            self.choosen_piece = self.board.locatePiece(best[0])
            self.previous_move["old position"] = best[0]
            self.choosen_piece.makeMove(best[1], self.board)
            self.turn_step = 0
            self.onMove()
            return
    
    def onMove(self):
        "Event xảy ra khi một nước đi được thực hiện"
        self.movable_tile = []
        self.previous_move["new position"] = self.choosen_piece.position
        if(self.monte_carlo_user.current_node != None):
            self.monte_carlo_user.moveToNode(self.previous_move["old position"], self.previous_move["new position"]) # Update trạng thái monte carlo
        self.king_is_checked = self.board.getCheckedKing()
        self.possible_move_white = self.board.getPossibleMoveWhite()
        self.possible_move_black = self.board.getPossibleMoveBlack()
        self.sound_manager.playMoveSound()
        self.move_count += 1

        if self.board.pieceJustCaptured():  # Kiểm tra trực tiếp, không cần qua biến tạm
            self.sound_manager.capture_sound.play()
            self.board.last_captured_piece = None  # Reset last_captured_piece
        elif self.king_is_checked[0]:
            self.sound_manager.check_sound.play()
        else:
            self.sound_manager.move_sound.play()

        if(self.king_is_checked[0] == True or self.board.endGame()[0] == True):
            if(len(self.possible_move_white) == 0): self.game_ended = [True, "White"]
            elif(len(self.possible_move_black) == 0): self.game_ended = [True, "Black"]
        elif(len(self.possible_move_white) == 0 or len(self.possible_move_black) == 0):
            self.game_ended = [True, "Draw"]
