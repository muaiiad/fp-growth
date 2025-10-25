import pandas as pd
raw = pd.read_excel("data/data.xlsx")
transactionTable = raw.values.tolist() # converting the data to a 2D list


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
            self.children[child.item] += 1

minimumSupport = 0.5
minimumConfidence = 0.5

# TODO (Step 1): extract the frequent items, put them in this list as tuples, first element represents character, second represents support
# sort in-place by second element in tuple (frequency)
frequent_items = [] # put the result here

# TODO (Step 2): use frequent_items to re-arrange items in transactionTable (you can completely replace it if you want)

# TODO (Step 3): generate the tree based on transactionTable
root = FPNode(None, None, None) # this is the root, keep everything None except children
frequent_nodes = {}
# this hash will have a character as a key, and the value will be a list of all references to that character in the tree
# we will use this because we traverse the tree starting from least frequent characters

# TODO (Step 4): traverse the tree starting from least frequent characters (use frequent_items and frequent_nodes to find the starting nodes)
# for each starting node, traverse the tree by going to the parent until you hit the root, then:
# generate the conditional trees (sets of the nodes in the path that leads up to that node) 
# find the frequent patterns

frequent_patterns = [] # put the result here

# TODO (Step 5): for each frequent pattern, generate all possible subsets, excluding the empty subset and the complete subset:  
#                   - For each subset:  
#                       - Find the complementary subset and calculate association rules.  
#                       - Extract strong rules based on the minimum confidence threshold.
#                   - Calculate lift for every strong rule

strong_rules = [] # put the result here 



    


