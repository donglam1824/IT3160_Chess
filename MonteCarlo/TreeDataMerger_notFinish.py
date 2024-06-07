from copy import deepcopy
import sqlite3

from MonteCarlo.Node import Node


class TreeDataMerger:

    def mergeTreeData(first_database_path : str, second_database_path : str):
        root_1 = TreeDataMerger.loadTreeData(first_database_path)
        root_2 = TreeDataMerger.loadTreeData(second_database_path)
        merge_tree_root = TreeDataMerger.syncNode(root_1, root_2)

    def syncNode(node_1 : Node, node_2 : Node):
        merge_node = deepcopy(node_1)
        merge_node.visited += node_2.visited
        merge_node.total += node_2.total
            


    def loadTreeData(database_path):
        with sqlite3.connect(database_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Monte_Carlo_Tree')
            tree_data = cursor.fetchall()
        root = Node("White", None, None, None, None) # Tạo nút gốc
        root.visited = tree_data[1][1]
        root.total = tree_data[1][2]
        tree_data.remove(tree_data[0]) #Bỏ các dữ liệu đầu đã sử dụng
        tree_data.remove(tree_data[0])

        node_stack = [root]
        previous_node = root
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
        return root

