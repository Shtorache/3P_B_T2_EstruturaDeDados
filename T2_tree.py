import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import networkx as nx
import imageio

class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        else:
            if key < root.val:
                root.left = self.insert(root.left, key)
            else:
                root.right = self.insert(root.right, key)
        return root

    def search(self, root, key, path=[]):
        if root is None:
            return path
        path.append(root.val)
        if root.val == key:
            return path
        if key < root.val:
            return self.search(root.left, key, path)
        return self.search(root.right, key, path)

    def build_tree(self, values):
        self.root = Node(values[0])
        for value in values[1:]:
            self.insert(self.root, value)

def plot_search_path(tree, path, filename="tree_search.gif", repetitions=3):
    G = nx.DiGraph()
    pos = {}
    labels = {}

    def add_edges(node, x=0, y=0, level=1):
        if node:
            pos[node.val] = (x, y)
            labels[node.val] = node.val
            if node.left:
                G.add_edge(node.val, node.left.val)
                add_edges(node.left, x - 1 / level, y - 1, level + 1)
            if node.right:
                G.add_edge(node.val, node.right.val)
                add_edges(node.right, x + 1 / level, y - 1, level + 1)

    add_edges(tree.root)

    frames = []

    for i in range(1, len(path) + 1):
        plt.figure(figsize=(10, 8))
        color_map = []
        for node in G.nodes:
            if node in path[:i]:
                color_map.append('yellow')
            else:
                color_map.append('lightblue')
        nx.draw(G, pos, labels=labels, node_color=color_map, with_labels=True, node_size=500, font_size=10, font_weight="bold")
        frame_filename = f"frame_{i}.png"
        plt.savefig(frame_filename)
        plt.close()
        frames.append(imageio.imread(frame_filename))

    frames *= repetitions

    plt.figure(figsize=(10, 8))
    color_map = []
    for node in G.nodes:
        if node == path[-1]:
            color_map.append('green')
        elif node in path:
            color_map.append('yellow')
        else:
            color_map.append('lightblue')
    nx.draw(G, pos, labels=labels, node_color=color_map, with_labels=True, node_size=500, font_size=10, font_weight="bold")
    frame_filename = "frame_final.png"
    plt.savefig(frame_filename)
    plt.close()
    frames.append(imageio.imread(frame_filename))

    imageio.mimsave(filename, frames, duration=7.0)

    for frame_filename in [f"frame_{i}.png" for i in range(1, len(path) + 1)] + ["frame_final.png"]:
        os.remove(frame_filename)

with open('tree.txt', 'r') as file:
    values = list(map(int, file.read().split()))

numero_a_buscar = 6

bst = BinarySearchTree()
bst.build_tree(values)

path = bst.search(bst.root, numero_a_buscar)
plot_search_path(bst, path, repetitions=10)
