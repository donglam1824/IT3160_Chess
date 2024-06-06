import random
import sqlite3

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
    
    def moveToNode(self, old_position, new_position):
        for node in self.current_node.children:
            if(old_position == node.old_position and new_position == node.new_position):
                self.current_node = node
                return

    def findBestMove(self):
        choosen_node : Node =  self.miniMaxing(0, None, self.current_node, True, 3, -float("Inf"), float("Inf"))[1]
        return [choosen_node.old_position, choosen_node.new_position]
    
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