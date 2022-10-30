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
    def __init__(self, pins, json_file):
        self.keyboard = nx.Graph()
        self.json_file = json_file
        with open(json_file, encoding="utf8") as f:
            self.json_dict = json.load(f)
            #print(type(self.json_dict))
            #print(len(self.json_dict))
            node = 0
            adjy = 0
            skipy = 0
            for i in self.json_dict:
                print("This is a new row!")
                adjx = 0
                skipx = 0
                for j in i:
                    #print(j)
                    if isinstance(j, str):
                        j.rstrip()
                        print(j.rstrip(), "is a str")
                        self.keyboard.add_node('SW' + str(node))
                        self.keyboard.nodes['SW' + str(node)]['coord'] = (adjx + skipx, adjy + skipy)
                        skipx += adjx
                        skipx += 1
                        node += 1
                    elif isinstance(j, dict):
                        #print("This a dict with ", len(j), "items")
                        for key in j:
                            if key == 'x':
                                print("add ", j['x'], " horizontal space")
                                skipx += int(j['x'])
                            elif key == 'y':
                                print("add ", j['y'], " vertical space")
                                skipx += int(j['y'])
                            elif key == 'w':
                                print("add key width by ", j['w'])
                                adjx += int(j['w'])/2
                            elif key == 'h':
                                print("add key height(downwards) by ", j['h'])
                                adjy += int(j['h']) / 2
                            elif key == 'x2' or key == 'y2' or key == 'w2' or key == 'h2':
                                print("uh oh")
                            elif key == 'a' or key == 'f' or key == 'f2' or key == 'p' or key == 's':
                                print("something about font")
                adjy += 1


        # Matrix where rows and cols depend on amount of pins. example 18 pins -> sqrt(18) = 9 -> 9 rows and 9 columns. for uneven amount of pins make columns>rows
        # Note that these cols and rows are NOT defining the keeb cols and rows, this is specifically for the matrix and will always be as square as possible
        self.pins = pins
        if (pins / 2) % 1 == 0:
            pincols = pins / 2
            pinrows = pins / 2
        else:
            pincols = int(pins / 2 - 0.5)
            pinrows = int(pins / 2 + 0.5)

        #These are the matrix/switches
        self.pinrows = pinrows
        self.pincols = pincols
        self.matrix = pinrows * pincols

        self.switches = []



        #self.switches = ['SW' + str(i) for i in range(1, self.n+1)]


        #This is wrong, the nodes come from the json not the matrix, the amount of nodes will always be <= to the amount of switches.
        #self.keyboard.add_nodes_from(self.switches)

    def switches(self, pinrows, pincols):
       for j in range(1, pinrows + 1):
            for k in range(1, pincols + 1):
                #list of all switches and their column and row
                listc = [k + j - 2, k, j]
                self.switches.append(listc)


    def connectswitch(self):
        #this is for randomizing switch
        for i in range(0, node):
            #each switchslot chooses a random switch
            rand = np.random.randint(0, matrix)
            #add switch[rand] to switchslot i
            keeb.nodes['SW' + str(i)]['switch'] = (rand)

        #we also need to be able to swap specific switches.

# define population class
class Population:
    def __init__(self, count):
        # size of population
        self.count = count
        # RULES FOR GENERATING INDIVIDUALS
        # 1. grab copy of switches.
        # 2. grab copy of keyboard.
        # 3. start at first node and randomize one of the item in switches list, continue until every node has one switch.
        # 4. this is now a generated keeb.

        #RULES FOR CROSSOVER
        # 1. randomize where to split the switches, draw a line between first switch and n switch.
        # 2. decide which part will be kept and which will mutate(since kept/locked switches will have different locations on each keeb we'll mutate the other parents gene to fit it)
        # 3. mutate gene to fit the other keyboard.
        # 3.1. lock switches to nodes that will not mutate/will be kept, if switch x is used on parent1 but not parent2 then parent2 will have an equivalent switch y.
        # 3.2. grab all unlocked switches from parent1 and place them as close as possible to their node position on parent1 but on parent2, the node on parent2 might be occupied by a locked switch and therefore will look for a closer unlocked switch, this will be the mutation.
        # 3.3. repeat step 3.2 on parent1 with switches from parent2
        # 3.4. two new children has been generated.

        #RULES FOR FITNESS
        # 1. summarize all unique rows and columns, this pin score is more important than the distance score.
        # 2. sort used switches by row
        # 3. grab all switches with same row and calculate distance score of each row by shortest distance to connect all switches of same row.
        # 3.2. note that the distance is based on the nodes and not switch matrix, we also need an algorithm to find shortest path.
        # 4. do step 2 but with columns instead of rows and add them all together, the smaller the score the better.
        # 5. do some math where fewer pins used(fewer unique rows and columns) is better fitness as well as lower distance score, note that pin score weights more than distance score, this should avoid the algorithm to apply a unique row and column for each switch(giving it a 0 distance score) when amount of pins>=switches.




        # initialize keyboard population
        self.population = [Keyboard(12, 10) for i in range(self.count)]

keeb = Keyboard(18, 'keyboard-layout_1.json')
print(keeb.keyboard)
nx.draw(keeb.keyboard, pos=nx.get_node_attributes(keeb.keyboard, 'coord'))
plt.show()

