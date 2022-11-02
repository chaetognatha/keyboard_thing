import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import libpysal as ps
import json
from pathlib import Path
from numpy.random import default_rng as rng
"""
Objective: Model a keyboard circuit to determine the optimal circuit design
Special: use OOP to model the keyboard circuit
"""
# define keyboard class
class Keyboard:
    def __init__(self, pins, json_file):
        self.keyboard = nx.Graph()
        self.json_file = json_file
        self.connect_list = []
        with open(json_file, encoding="utf8") as f:
            self.json_dict = json.load(f)
            #print(type(self.json_dict))
            #print(len(self.json_dict))
            node = 0
            adjy = 0
            skipy = 0
            my_list = []
            full_list = []
            for i in self.json_dict:
                print("This is a new row!")
                width = 0
                skipx = 0
                for j in i:
                    #print(j)
                    if isinstance(j, str):
                        #print(j.rstrip(), "is a str")
                        self.keyboard.add_node('SW' + str(node))
                        self.keyboard.nodes['SW' + str(node)]['coord'] = (skipx+(width/2), adjy + skipy)
                        this_list = [node,
                                     self.keyboard.nodes['SW' + str(node)]['coord'][0],
                                     self.keyboard.nodes['SW' + str(node)]['coord'][1]]
                        if (node != 0 and
                                self.keyboard.nodes['SW' + str(node-1)]['coord'][1] ==
                                self.keyboard.nodes['SW' + str(node)]['coord'][1]):

                            theweight = np.abs(self.keyboard.nodes['SW' + str(node)]['coord'][0] -
                                               self.keyboard.nodes['SW' + str(node-1)]['coord'][0])
                            self.keyboard.add_edge('SW' + str(node-1), 'SW' + str(node), weight=theweight)

                        if width != 0:
                            skipx += width

                        skipx += 1
                        width = 0
                        #[node, node.x, node.y]
                        my_list.append(this_list)
                        node += 1

                    elif isinstance(j, dict):
                        #print("This a dict with ", len(j), "items")
                        for key in j:
                            if key == 'x':
                                print("add ", j['x'], " horizontal space")
                                skipx += float(j['x'])
                            elif key == 'y':
                                print("add ", j['y'], " vertical space")
                                skipy += float(j['y'])
                            elif key == 'w':
                                print("add key width by ", j['w'])
                                width = float(j['w'])-1
                            elif key == 'h':
                                print("add key height(downwards) by ", j['h'])
                                #adjy += float(j['h']) / 2
                            elif key == 'x2' or key == 'y2' or key == 'w2' or key == 'h2':
                                print("uh oh")
                            elif key == 'a' or key == 'f' or key == 'f2' or key == 'p' or key == 's':
                                print("something about font")
                self.num_nodes = node
                print(self.num_nodes)
                skipy += 1
                full_list.append(my_list.copy())
                #clearing list to reuse
                my_list.clear()
        for i in range(0, len(full_list)-1):
            #print("this is ", full_list[i])
            for j in range(0, len(full_list[i])):
                #print("comparing this node: ", full_list[i][j])
                for k in range(0, len(full_list[i+1])):
                    #print("with ", full_list[i+1][k])
                    if abs(float(full_list[i][j][1])-float(full_list[i+1][k][1])) <= 1.5:
                        #print(full_list[i][j], full_list[i+1][k])
                        self.keyboard.add_edge('SW' + str(int(full_list[i][j][0])),
                                               'SW' + str(int(full_list[i+1][k][0])))
                        theweight = (
                                abs(self.keyboard.nodes['SW' + str(int(full_list[i][j][0]))]['coord'][0] -
                                    self.keyboard.nodes['SW' + str(int(full_list[i+1][k][0]))]['coord'][0]) +
                                abs(self.keyboard.nodes['SW' + str(int(full_list[i][j][0]))]['coord'][1] -
                                    self.keyboard.nodes['SW' + str(int(full_list[i+1][k][0]))]['coord'][1])
                        )
                        self.keyboard.add_edge('SW' + str(int(full_list[i][j][0])),
                                               'SW' + str(int(full_list[i+1][k][0])),
                                               weight=theweight)


        # Matrix where rows and cols depend on amount of pins. example 18 pins -> sqrt(18) = 9 -> 9 rows and 9 columns. for uneven amount of pins make columns>rows
        # Note that these cols and rows are NOT defining the keeb cols and rows, this is specifically for the matrix and will always be as square as possible

        if (pins / 2) % 1 == 0:
            pincols = pins / 2
            pinrows = pins / 2
        else:
            pincols = int(pins / 2 + 0.5)
            pinrows = int(pins / 2 - 0.5)

        #These are the matrix/switches
        self.pinrows = int(pinrows)
        self.pincols = int(pincols)
        self.matrix = int(pinrows * pincols)
        if self.matrix < node:
            print("Pins are too low, maximum matrix: ", self.matrix, " while keyboard requires atleast: ", node)
        else:
            print("Maximum matrix: ", self.matrix, "Matrix required: ", node)

        #creates a dict with every key and each key contains the matrix coordinates
        self.switch_dict = {}
        self.switch_list = []
        self.switch_num = 0
        for mrow in range(1, self.pinrows+1):
            for mcol in range(1, self.pincols + 1):
                self.switch_dict['key' + str(self.switch_num)] = mcol, mrow
                this_switch = [self.switch_num, mcol, mrow]
                self.switch_num += 1
                self.switch_list.append(this_switch)


        #my_dict is used for drawing
        self.my_dict ={}
        for i in full_list:
            for j in i:
                self.my_dict['SW' + str(j[0])] = j[1],j[2]
        '''
                for count, switch in enumerate(self.switch_list):
            print(count)
        print(self.switch_list)
        '''

    def connectswitch(self):

        rand = np.random.choice(self.switch_num, size=self.num_nodes, replace=False)
        #print(rand)
        self.list_of_nodes = []
        for i in range(self.num_nodes):
            pair_list = [i, rand[i]]
            self.list_of_nodes.append(pair_list)
        #list consist of list with format [node, switch]

        #we also need to be able to swap specific switches.

    def rewireswitch(self):
        self.these_switches = []
        self.these_nodes = []
        for slot in self.list_of_nodes:
            self.these_nodes.append(slot[0])
            self.these_switches.append(slot[1])





# define population class
class Population:
    def __init__(self, count):
        # size of population
        self.count = count

        # initialize keyboard population
        self.population = [Keyboard(21, 'keyboard-layout_1.json') for i in range(self.count)]
        print(self.population)


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




keebo = Keyboard(21, 'keyboard-layout_1.json')

all_the_keebs = []
for i in range(10):
    keeb = Keyboard(21, 'keyboard-layout_1.json')
    keeb.connectswitch()
    all_the_keebs.append(keeb)


nx.draw(keebo.keyboard, node_size=50, font_size=10, pos=nx.get_node_attributes(keebo.keyboard, 'coord'), with_labels=True)
labels = {}
for u,v,data in keeb.keyboard.edges(data=True):
    labels[(u,v)] = data['weight']
nx.draw_networkx_edge_labels(keebo.keyboard,
                             pos=keebo.my_dict,
                             label_pos=0.8,
                             edge_labels=labels,
                             font_size=8,
                             )
plt.gca().invert_yaxis()
plt.show()

keebo.connectswitch()
print(keebo.list_of_nodes)
keebo.rewireswitch()
print(keebo.these_nodes)
print(keebo.these_switches)

