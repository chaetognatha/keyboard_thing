import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import libpysal as ps
"""
Objective: Model a keyboard circuit to determine the optimal circuit design
Special: use OOP to model the keyboard circuit
"""
# define keyboard class
class Keyboard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.n = rows * cols
        self.switches = ['SW' + str(i) for i in range(1, self.n+1)]
        self.keyboard = nx.Graph()
        self.keyboard.add_nodes_from(self.switches)
        for i in range(1, self.rows+1):
            for j in range(1, self.cols+1):
                self.keyboard.nodes['SW' + str((i-1)*self.cols + j)]['coord'] = (i, j)
        self.end_node = 'SW' + str(self.n)

#define population class