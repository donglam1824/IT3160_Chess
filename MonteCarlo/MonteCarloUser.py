import random
import sqlite3

from Base.ChessBoard import ChessBoard
from Base.Player import Player
from MonteCarlo.Node import Node
from Minimax.BlackMax import BlackMax
from Minimax.WhiteMax import WhiteMax


class MonteCarloUser: 
    database_path = "MonteCarlo/database.db"
    minimax_white = WhiteMax(3)
    minimax_black = BlackMax(3)

    def __init__(self):
        self.root : Node = None
        self.loadTreeData()
        self.current_node = self.root
        self.current_board = ChessBoard()
    
    def moveToNode(self, old_position, new_position):
        "Di chuyển tới nút"
        for node in self.current_node.children:
            if(old_position == node.old_position and new_position == node.new_position):
                self.current_node = node
                piece = self.current_board.locatePiece(old_position)
                piece.makeMove(new_position, self.current_board)
                if(len(self.current_node.children) == 0):
                    self.expansion(self.current_node)
                return
        print("error, can't find node")
        exit(1)



    def findBestMove(self):
        "Trả về nước đi tốt nhất tìm được, theo [old_position, new_position]"
        if(self.current_node.children[0].visited > 0):
            choosen_node : Node =  self.miniMaxing(0, None, self.current_node, True, 3, -float("Inf"), float("Inf"))[1]
            return [choosen_node.old_position, choosen_node.new_position]
        else:
            if(self.current_node.current_side == "White"):
                best = self.minimax_white.miniMax(0, "", "", True, self.current_board, -float("Inf"), float("Inf"))
                choosen_piece = self.current_board.player_white.chess_pieces[best[1]]
            else:
                best = self.minimax_black.miniMax(0, "", "", True, self.current_board, -float("Inf"), float("Inf"))
                choosen_piece = self.current_board.player_black.chess_pieces[best[1]]
            return [choosen_piece.position, best[2]]

            

    def expansion(self, node : Node):
        "Mở rộng nhánh con mới"
        if(node.current_side == "White"):
            possible_move = self.current_board.getPossibleMoveWhite()
        else: possible_move = self.current_board.getPossibleMoveBlack() 
        for move in possible_move:
            #move = [piece, move_position]
            piece = move[0]
            piece_symbol = self.current_board.board_display[piece.position[0]][piece.position[1]]
            new_node = Node(Player.getOppositeSide(node.current_side), 
                            node, piece_symbol, piece.position, move[1])
            node.children.append(new_node)
        return

    def miniMaxing(self, best_value, best_node, current_node : Node, is_max, depth, alpha : float, beta : float):
        "Lọc qua cây nước đi theo miniMax"
        #Khởi tạo
        if is_max: best_value = -float("Inf")
        else: best_value = float("Inf")
        #Kiểm tra kết thúc hoặc đến đáy
        if(len(current_node.children) == 0 or depth <= 0):
            if(current_node.visited == 0): 
                return [-best_value, current_node]
            return [current_node.total/current_node.visited, current_node]
        #Xem từng nước đi một
        if(is_max == True):
            for node in current_node.children:
                node_value = self.miniMaxing(best_value, best_node, node, not is_max, depth - 1, alpha, beta)[0]
                if(best_value < node_value): 
                    best_value = node_value
                    best_node = node
                    alpha = max(best_value, alpha)
                if(beta <= alpha): break
        else:
            for node in current_node.children:
                node_value = self.miniMaxing(best_value, best_node, node, not is_max, depth - 1, alpha, beta)[0]
                if(best_value > node_value): 
                    best_value = node_value
                    best_node = node
                    alpha = min(best_value, alpha)
                if(beta <= alpha): break
        return [best_value, best_node]
    
    def unvisitNodeHandler(self):
        "Xử lý khi gặp nút chưa gặp"


    def loadTreeData(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Monte_Carlo_Tree')
            tree_data = cursor.fetchall()
        self.root = Node("White", None, None, None, None) # Tạo nút gốc
        self.root.visited = tree_data[1][1]
        self.root.total = tree_data[1][2]
        tree_data.remove(tree_data[0]) #Bỏ các dữ liệu đầu đã sử dụng
        tree_data.remove(tree_data[0])

        node_stack = [self.root]
        previous_node = self.root
        depth_pointer = 1
        for node_data in tree_data:
            #Node_data = [depth, visited, total, current_side, moving_piece, move_info]
            if(depth_pointer < node_data[0]):
                depth_pointer += 1
                node_stack.append(previous_node)
            while(depth_pointer > node_data[0]):
                depth_pointer -= 1
                node_stack.pop()
            parent = node_stack[depth_pointer - 1]
            old_position = [int(node_data[5][0]), int(node_data[5][1])]
            new_position = [int(node_data[5][2]), int(node_data[5][3])]

            new_node = Node(node_data[3], parent, node_data[4], old_position, new_position)
            new_node.visited = node_data[1]
            new_node.total = node_data[2]
            parent.children.append(new_node)
            previous_node = new_node
        return