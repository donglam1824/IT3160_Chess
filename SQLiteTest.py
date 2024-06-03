import sqlite3

class TreeNode:
    def __init__(self, value, id=None):
        self.id = id
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

# Create and connect to the database
conn = sqlite3.connect('tree.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (id INTEGER PRIMARY KEY, value TEXT, parent_id INTEGER)''')
conn.commit()

def save_node(node, parent_id=None):
    cursor.execute('INSERT INTO nodes (value, parent_id) VALUES (?, ?)', ('OK', parent_id))
    node.id = cursor.lastrowid
    for child in node.children:
        save_node(child, node.id)

def load_node(node_id):
    cursor.execute('SELECT id, value FROM nodes WHERE id = ?', (node_id,))
    id, value = cursor.fetchone()
    node = TreeNode(value, id)
    cursor.execute('SELECT id FROM nodes WHERE parent_id = ?', (node_id,))
    for child_id, in cursor.fetchall():
        node.add_child(load_node(child_id))
    return node

# Save to database
root = TreeNode('root')
root.add_child(TreeNode('chi1'))
root.add_child(TreeNode('child2'))
save_node(root)
conn.commit()

# Load from database
root = load_node(1)
conn.close()