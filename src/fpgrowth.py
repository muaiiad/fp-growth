import os
import pandas as pd
from collections import Counter
import itertools

from pandas.core.common import not_none

script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "../data/data.xlsx")

raw = pd.read_excel(data_path)
transactionTable = raw.values.tolist() # converting the data to a 2D list

transactionTable = [ str(row[1]).split(',') for row in raw.values.tolist()]

class FPNode: # change this class if necessary, idk how correct it is 
    def __init__(self, item, count, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {} 
        # children are stored as a hash map (dictionary), it will map from a character to another FP node.
        # in python, all non-primitives are references, so you dont need a pointer or anything like that

    def addchild(self, child):
        if child.item not in self.children:
            self.children[child.item] = child
        else:
            self.children[child.item].count += 1

minimumSupport = 0.5
minimumConfidence = 0.5

# TODO (Step 1): extract the frequent items, put them in this list as tuples, first element represents character, second represents support
# sort in-place by second element in tuple (frequency)
frequent_items = [] # put the result here
item_count = Counter()

for transaction in transactionTable:
    unique_items = set(transaction)
    for item in unique_items:
        item_count[item] += 1

Num_Of_Transaction = len(transactionTable)

for item,count in item_count.items():
    support = item_count[item]/Num_Of_Transaction
    if(support >= minimumSupport):
        frequent_items.append((item, support))

frequent_items.sort(key=lambda x: x[1],reverse=True)

# TODO (Step 2): use frequent_items to re-arrange items in transactionTable
arrangedTable = [] # put the result here
for transaction in transactionTable:

    sorted_items = []
    for pair in frequent_items:
        if pair[0] in transaction:
            sorted_items.append(pair[0])

    if sorted_items:
        arrangedTable.append(sorted_items)


# TODO (Step 3): generate the tree based on arrangedTable
root = FPNode(None, None, None) # this is the root, keep everything None except children
frequent_nodes = {}
# this hash will have a character as a key, and the value will be a list of all references to that character in the tree
# we will use this because we traverse the tree starting from least frequent characters

# TODO (Step 4): traverse the tree starting from least frequent characters (use frequent_items and frequent_nodes to find the starting nodes)
# for each starting node, traverse the tree by going to the parent until you hit the root
# generate the conditional trees (sets of the nodes in the path that leads up to that node) 
conditional_trees = []
for item in reversed(frequent_items):
    if (item[0] not in frequent_nodes):
        print(item[0] + " not found in tree")
        break
    for node in frequent_nodes[item[0]]:
        conditional = []
        temp = node
        frequency = node.count
        while (temp is not root):
            conditional.append(temp.item)
            temp = temp.parent
        for _ in range(0,frequency):
            conditional_trees.append(conditional)
        # if a node has a count > 1, that means that path exists multiple times, this is just a simple way of handling that

# TODO (Step 5): find the frequent patterns from the conditional trees
# note that unlike in the lecture and lab examples, the given conditional trees INCLUDE the node itself, it'll always be the first element
frequent_patterns = [] # put the result here
last_node = conditional_trees[0][0]
node_frequency = Counter()
minimum_support_count = minimumSupport * len(transactionTable)

for path in conditional_trees:

    if (path[0] != last_node):
        accepted_nodes = [last_node]
        for key,value in node_frequency.items():
            if value >= minimum_support_count:
                accepted_nodes.append(key)

        for length in range(2,len(accepted_nodes)+1):
            for combination in (itertools.combinations(accepted_nodes,length)):
                frequent_patterns.append(list(combination))

        last_node = path[0]
        node_frequency.clear()

    for node in path[1:]:
        node_frequency[node] += 1

accepted_nodes = [last_node]
for key,value in node_frequency.items():
    if value >= minimum_support_count:
        accepted_nodes.append(key)

for length in range(2, len(accepted_nodes) + 1):
    for combination in (itertools.combinations(accepted_nodes, length)):
        frequent_patterns.append(list(combination))





# TODO (Step 6): for each frequent pattern, generate all possible subsets, excluding the empty subset and the complete subset:  
#                   - For each subset:  
#                       - Find the complementary subset and calculate association rules.  
#                       - Extract strong rules based on the minimum confidence threshold.
#                   - Calculate lift for every strong rule

strong_rules = [] # put the result here 