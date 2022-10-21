import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import libpysal as ps
import json
from pathlib import Path
"""
Objective: Model a keyboard circuit to determine the optimal circuit design
Special: use OOP to model the keyboard circuit
"""
# define keyboard class
class Keyboard:
    def __init__(self, rows, cols, json_file):
        self.json_file = json_file
        # import json file as dict
        with open(json_file) as f:
            self.json_dict = json.load(f)

        self.rows = rows
        self.cols = cols
        self.n = rows * cols
        self.switches = ['SW' + str(i) for i in range(1, self.n+1)]
        self.keyboard = nx.Graph()
        self.keyboard.add_nodes_from(self.switches)


# define population class
class Population:
    def __init__(self, count):
        # size of population
        self.count = count
        # RULES FOR GENERATING INDIVIDUALS
        # initialize keyboard population
        self.population = [Keyboard(12, 10) for i in range(self.count)]