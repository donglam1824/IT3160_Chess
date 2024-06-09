import sqlite3
from Base.ChessBoard import ChessBoard
from MonteCarlo.Node import Node
from Base.Player import Player
import random, time

max_simulate_depth = 20

class MonteCarloSearcher:
    database_path = "MonteCarlo/database.db"
    database_backup_path = "MonteCarlo/database_backup.db"
    simulate_board = ChessBoard()

    def __init__(self):
        self.root = None
        self.total_time = 0

    def makeNewTree(self):
        self.root = Node("White", None, None, None, None)
        self.total_time = 0
        self.expansion(self.root)

    def selection(self):
        "Đi sâu xuống node lá, đường đi ưu tiên các node giá trị cao"
        choosen_node = self.root
        self.simulate_board = ChessBoard()
        while(choosen_node.children != []):
            max_uct = -float("Inf")
            max_node = None
            for node in choosen_node.children:
                if(node.visited == 0):
                    node.makeMoveToNode(self.simulate_board)
                    return node #Tìm node chưa dc thăm bao h, chọn luôn
                uct_value = node.getUctValue(self.simulate_board.game_state)
                if(max_uct < uct_value):
                    max_uct = uct_value
                    max_node = node
            choosen_node = max_node
            choosen_node.makeMoveToNode(self.simulate_board)
        return choosen_node
    
    def expansion(self, node : Node):
        "Mở rộng nhánh con mới"
        if(node.current_side == "White"):
            possible_move = self.simulate_board.getPossibleMoveWhite()
        else: possible_move = self.simulate_board.getPossibleMoveBlack() 
        for move in possible_move:
            #move = [piece, move_position]
            piece = move[0]
            piece_symbol = self.simulate_board.board_display[piece.position[0]][piece.position[1]]
            new_node = Node(Player.getOppositeSide(node.current_side), 
                            node, piece_symbol, piece.position, move[1])
            node.children.append(new_node)
        return
    
    def simulate(self, current_side):
        "Đi random nước đi và lấy giá trị cuối cùng"
        #start_time = time.time()
        evaluated_side = Player.getOppositeSide(current_side)
        for i in range(0, max_simulate_depth):
            if(current_side == "White"):
                possible_move = self.simulate_board.getPossibleMoveWhite() #Lấy bên Black
            else: possible_move = self.simulate_board.getPossibleMoveBlack() # Lấy bên White
            #print("get moves" , time.time() - start_time)
            if(len(possible_move) == 0):
                if(current_side == evaluated_side):
                    bonus = -5*(20-i) #Game thắng càng gần thì càng dc nhiều điểm hơn
                else: bonus = 5*(20-i)
                return self.simulate_board.evaluateBoard(evaluated_side) + bonus
            current_side = Player.getOppositeSide(current_side)
            choosen_move = random.choice(possible_move)
            choosen_move[0].makeMove(choosen_move[1], self.simulate_board)
        return self.simulate_board.evaluateBoard(evaluated_side)

    def backPropagation(self, value, node : Node, decaying_factor = 0.9):
        "Update ngược lại giá trị các node trên đường đi"
        if(node == None): return
        node.updateState(value)
        value = value * decaying_factor #Giảm dần value khi càng lên cao hơn
        self.backPropagation(value ,node.parent, decaying_factor)
    
    def runAlgorihm(self, running_time):
        "Chạy thuật toán trong khoảng thời gian (giây)"
        start_time = time.perf_counter()
        while(time.perf_counter() - start_time < running_time):
            selected_node = self.selection()
            if(selected_node.visited != 0):
                self.expansion(selected_node)
                if(len(selected_node.children) == 0):
                    #Hết nc đi để expand, tức là game kết thúc
                    print("Reach terminal state")
                    self.backPropagation(200, selected_node, 0.4)
                    continue
                selected_node = selected_node.children[0]
            value = self.simulate(selected_node.current_side)
            self.backPropagation(value, selected_node)
            if(self.root.visited%10 == 0):
                print( "Iteration: ", self.root.visited,", time:",self.total_time + time.perf_counter() - start_time)
        self.total_time += time.perf_counter() - start_time
        self.saveDataToFile()

        print("Data have been save to files")
        return
    
    def saveDataToFile(self):
        #Create and connect to the database
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Monte_Carlo_Tree')
        cursor.execute('''CREATE TABLE Monte_Carlo_Tree (tree_depth INTERGER, visited INTERGER, total REAL, side TEXT,
                       symbol TEXT, move TEXT)''')
        cursor.execute('INSERT INTO Monte_Carlo_Tree (tree_depth) VALUES (?)', (self.total_time,))
        self.writeSQLiteTreeData(cursor, self.root, 0)
        conn.commit()
        conn.close()
    
    def writeSQLiteTreeData(self, cursor, node : Node, depth):
        "Lưu data để máy sử dụng"
        if(node.old_position != None):
            move = str(node.old_position[0]) + str(node.old_position[1]) + str(node.new_position[0]) + str(node.new_position[1])
        else: move = None
        cursor.execute('INSERT INTO Monte_Carlo_Tree (tree_depth, visited, total, side, symbol, move) VALUES (?, ?, ?, ?, ?, ?)'
                       ,(depth, node.visited, node.total, node.current_side, node.moving_piece, move))
        for child in node.children:
            self.writeSQLiteTreeData(cursor ,child, depth+1)
    
    def loadTreeData(self):
        with sqlite3.connect(self.database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Monte_Carlo_Tree')
            tree_data = cursor.fetchall()
        self.total_time = tree_data[0][0] # Tích hợp lại tổng thời gian
        self.root = Node("White", None, None, None, None) # Tạo nút gốc
        self.root.visited = tree_data[1][1]
        self.root.total = tree_data[1][2]
        tree_data.remove(tree_data[0]) #Bỏ các dữ liệu đầu đã sử dụng
        tree_data.remove(tree_data[0])
        print("Read file successfully ,Loading data")

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
        print("Data load successfully")
        return
    

            
    


        
        


    
            



