import sqlite3
from Base.ChessBoard import ChessBoard
from MonteCarlo.Node import Node
from Base.Player import Player
import random, time, csv, pickle
from copy import deepcopy
from operator import attrgetter

root_board = ChessBoard()
child_boards = []
max_simulate_depth = 20
class MonteCarloSearcher:
    reading_file_path = "MonteCarlo/readingfile.txt"
    data_file_path = "MonteCarlo/datafile.bin"
    database_path = "MonteCarlo/database.db"
    def __init__(self):
        self.root = Node(root_board, "White", None, None, [True, True], [True, True])
        self.node_tree = []
        self.expansion(self.root)

    def selection(self):
        "Đi sâu xuống node lá, đường đi ưu tiên các node giá trị cao"
        choosen_node = self.root
        while(choosen_node.children != []):
            max_uct = -float("Inf")
            max_node = None
            for node in choosen_node.children:
                if(node.visited == 0): 
                    return node #Tìm node chưa dc thăm bao h, chọn luôn
                uct_value = node.getUctValue()
                if(max_uct < uct_value):
                    max_uct = uct_value
                    max_node = node
            choosen_node = max_node
        return choosen_node
    
    def expansion(self, node : Node):
        "Mở rộng nhánh con mới"
        if(node.current_side == "White"):
            possible_move = node.board.getPossibleMoveWhite() #Lấy bên Black
        else: possible_move = node.board.getPossibleMoveBlack() # Lấy bên White
        for move in possible_move:
            #move = [piece, move_position]
            copy_board = deepcopy(node.board)
            piece_index = node.board.getAllPieces().index(move[0])
            copy_board.getAllPieces()[piece_index].makeMove(move[1], copy_board)
            new_node = Node(copy_board, Player.getOppositeSide(node.current_side), 
            node, [copy_board.board_display[move[1][0]][move[1][1]], move[1]], True, True)
            node.children.append(new_node)
            self.node_tree.append(new_node)
        return
    
    def simulate(self, node : Node):
        "Đi random nước đi và lấy giá trị cuối cùng"
        #start_time = time.time()
        simulate_board = deepcopy(node.board)
        current_side = node.current_side
        evaluated_side = Player.getOppositeSide(node.current_side)
        for i in range(0, max_simulate_depth):
            if(current_side == "White"):
                possible_move = simulate_board.getPossibleMoveWhite() #Lấy bên Black
            else: possible_move = simulate_board.getPossibleMoveBlack() # Lấy bên White
            #print("get moves" , time.time() - start_time)
            current_side = Player.getOppositeSide(current_side)
            if(len(possible_move) == 0):
                return simulate_board.evaluateBoard(evaluated_side)
            choosen_move = random.choice(possible_move)
            choosen_move[0].makeMove(choosen_move[1], simulate_board)
        return simulate_board.evaluateBoard(evaluated_side)

    def backPropagation(self, value, node : Node):
        "Update ngược lại giá trị các node trên đường đi"
        if(node == None): return
        node.updateState(value)
        self.backPropagation(value ,node.parent)
    
    def runAlgorihm(self, running_time):
        "Chạy thuật toán trong khoảng thời gian (giây)"
        start_time = time.time()
        count = 0
        while(time.time() - start_time < running_time):
            count += 1
            selected_node = self.selection()
            #print("Selection" , time.time() - start_time)
            if(selected_node.visited != 0):
                self.expansion(selected_node)
                #print("Expansion" , time.time() - start_time)
                selected_node = selected_node.children[0]
            value = self.simulate(selected_node)
            #print("Simulate" , time.time() - start_time)
            self.backPropagation(value, selected_node)
            #print("Back Propagate" , time.time() - start_time)
            print(count, "Iteration done, time:",time.time() - start_time)
        self.saveDataToFile()
        print("Data have been save to files")
        return
    
    def saveDataToFile(self):
        open(self.reading_file_path, "+w").close()
        open(self.reading_file_path, "a").write("--- [turn, visited, total] ---\n")
        self.writeReadableTreeData(self.root, 0)
        open(self.data_file_path, "+w").close()
        self.writeBinaryTreeData()
        # Create and connect to the database
        conn = sqlite3.connect(self.database_path)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS Monte_Carlo_Tree')
        cursor.execute('''CREATE TABLE Monte_Carlo_Tree (tree_depth INTERGER, board BLOB, side TEXT, 
                       previous_move BLOB, white_castle_state BLOB, black_castle_state BLOB, visited INTERGER, total REAL)''')
        self.writeSQLiteTreeData(cursor, self.root, 0)
        conn.commit()
        conn.close()



    def writeCSVTreeData(self, node : Node, spacing):
        node_data = []
        tab_space = ""
        for i in range(0, spacing):
            tab_space += "\t"
        node_data.append(tab_space)
        node_data.append(node.board.board_display)
        node_data.extend([node.current_side, node.visited, node.total])
        with open(self.reading_file_path, "a+", newline= '') as file:
            writer = csv.writer(file)
            writer.writerow(node_data)
        if(node.children == []): return
        for child in node.children:
            self.writeReadableTreeData(child, spacing + 1)

    def writeReadableTreeData(self, node : Node, spacing):
        tab_space = ""
        for i in range(0, spacing):
            tab_space += "\t"
        file = open(self.reading_file_path, "a")
        for line in node.board.board_display:
            file.write(tab_space + "{:3} {:3} {:3} {:3} {:3} {:3} {:3} {:3}".format(*line) + "\n")

        file.write(tab_space + "---" + str([node.current_side, node.visited, node.total]) + "---" + "\n\n")
        file.close()
        if(node.children == []): return
        node.children.sort(key= lambda x: x.visited, reverse=True)
        for child in node.children:
            self.writeReadableTreeData(child, spacing + 1)

    def writeBinaryTreeData(self):
        with open(self.data_file_path, "wb") as file:
            pickle.dump(self.root, file)
    
    def writeSQLiteTreeData(self, cursor, node : Node, depth):
        #Saving
        cursor.execute('INSERT INTO Monte_Carlo_Tree (tree_depth, board, side, previous_move, visited, total) VALUES (?, ?, ?, ?, ?, ?)'
                       ,(depth, str(node.board.board_display), node.current_side, str(node.previous_move), node.visited, node.total))
        for child in node.children:
            self.writeSQLiteTreeData(cursor ,child, depth+1)
        


    
            



