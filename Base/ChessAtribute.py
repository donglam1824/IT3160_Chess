from copy import deepcopy
from Base.PieceEvaluation import EvaluatePiece

class ChessPiece:
    "Các thược tính cơ bản của quân cờ"
    def __init__(self, position, piece_value, name, side):
#        self.occupied_tile.append(position)
        self.position = position
        self.is_dead = False
        self.value = piece_value
        self.base_value = piece_value
        self.name = name
        self.has_moved = False
        self.side = side
        self.available_move = []
        self.linked_pieces = [] #Các quân cờ sẽ được update khi quân cờ này di chuyển
        self.score_table = EvaluatePiece.initailizeScore(name, side) # Điểm theo vị trí của bàn cờ
    def getPieceName(self, side):
        "Tìm ký hiệu của quân cờ trên bàn cơ <Không cần thiết khi có dao diện>"
        if(side == "White"): name = "w"
        else: name = "b"
        if(self.name == "Pawn"): name = name + "p"
        elif(self.name == "Rock"): name = name + "r"
        elif(self.name == "Knight"): name = name + "kn"
        elif(self.name == "Bishop"): name = name + "b"
        elif(self.name == "Queen"): name = name + "q"
        elif(self.name == "King"): name = name + "K"
        return name
    def makeMove(self, new_position, board):
        if(board.board_display[new_position[0]][new_position[1]] != "0"):
            board.deletePiece(new_position)
        board.board_display[new_position[0]][new_position[1]] = board.board_display[self.position[0]][self.position[1]]
        board.board_display[self.position[0]][self.position[1]] = "0"
        self.position = new_position
        self.has_moved = True
        self.displayMovableTile(board)
        #Update nhưng quân cờ mà trùng đường đi với vị trí cũ và mới của quân này
        linked_pieces = self.linked_pieces
        self.linked_piece = []
        for piece in linked_pieces:
            piece.displayMovableTile(board)
        chess_pieces = board.getAllPieces()
        for piece in chess_pieces:
            try:
                piece.available_move.index(new_position)
            except ValueError:
                continue
            piece.displayMovableTile(board)
    def isEaten(self, board):
        self.is_dead = True
    def gradePiece(self):
        self.value = self.base_value + self.score_table[self.position[0]][self.position[1]]
    def isInTheBoard(position):
        "KT xem nước đi còn trong bàn cờ không"
        if(position[0] < 0 or position[1] < 0): return False
        if(position[0] > 7 or position[1] > 7): return False
        return True
    def updateMove_Multiple(self, move_vectors, board):
        "Trả về các ô đi được của quân cờ đi được nhiều ô (Xe, Tịnh, Hậu)"
        movable_tile = []     
        for vector in move_vectors:
            check_tile = deepcopy(self.position)
            check_tile[0] += vector[0]
            check_tile[1] += vector[1]
            try:
                while(board.board_display[check_tile[0]][check_tile[1]] == "0" and ChessPiece.isInTheBoard(check_tile)):
                    movable_tile.append(deepcopy(check_tile))
                    check_tile[0] += vector[0]
                    check_tile[1] += vector[1]
                #Thêm tile có quân cờ địch ăn được
                if(ChessPiece.isInTheBoard(check_tile)):
                    block_piece = board.locatePiece(check_tile)
                    try: 
                        block_piece.linked_pieces.index(self)
                    except ValueError:
                        block_piece.linked_pieces.append(self)
                    if(block_piece.side != self.side):
                        movable_tile.append(deepcopy(check_tile))
            except IndexError:
                #Ra khỏi bàn cờ
                continue
        self.available_move = movable_tile
        self.gradePiece()
        return movable_tile
    def updateMove_Singular(self, move_vectors, board):
        "Trả về các ô đi được của quân cờ đi được 1 ô ô (Tốt, Mã, Vua)"
        movable_tile = []
        for vector in move_vectors:
            check_tile = deepcopy(self.position)
            check_tile[0] += vector[0]
            check_tile[1] += vector[1]
            if(ChessPiece.isInTheBoard(check_tile)):
                if(board.board_display[check_tile[0]][check_tile[1]] == "0"):
                    movable_tile.append(deepcopy(check_tile))
                    #Thêm tile có quân cờ địch ăn được (Trừ khi là Tốt)
                else:
                    #Tìm quân cờ nằm trên đường đi của nhau
                    block_piece = board.locatePiece(check_tile)
                    try: 
                        block_piece.linked_pieces.index(self)
                    except ValueError:
                        block_piece.linked_pieces.append(self)
                    if(block_piece.side != self.side and len(move_vectors) > 1):
                        movable_tile.append(deepcopy(check_tile))
        self.gradePiece()
        return movable_tile

        