import os
import pandas as pd
from collections import Counter
import itertools
from itertools import combinations

from pandas.core.common import not_none


script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "../data/test.xlsx")

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

minimumSupport = 0.3
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

frequent_items.sort(key=lambda x: (-x[1], x[0]))

print("FREQUENT ITEM, SUPPORT\n===============================\n" + str(frequent_items) + "\n===============================")

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
for transaction in arrangedTable:
    current_node = root
    for item in transaction:
        if item in current_node.children:
            child_node = current_node.children[item]
            child_node.count += 1
            
        else:
            child_node = FPNode(item, 1, current_node)
            current_node.children[item] = child_node

     
        if item not in frequent_nodes:
            frequent_nodes[item] = [child_node]
            
        else:
            if all(existing_node is not child_node for existing_node in frequent_nodes[item]):
                frequent_nodes[item].append(child_node)

        current_node = child_node
        

all_paths = {}
for item, node in frequent_nodes.items():
    all_paths[item] = []
    for node in node:
        path = []
        temp = node
        depth = 0
        
        while temp.parent is not None:
            
            path.append(temp.item)
            temp = temp.parent
            depth += 1
        path.reverse() 
        all_paths[item].append((path, depth))

# depth first  from leaves to root
items_order = sorted(all_paths.keys(), key=lambda x: max(d for _, d in all_paths[x]), reverse=True)


print("FP TREE\n===============================")
for item in items_order:
    print(f"Item '{item}':")
    
    for i, (path, _) in enumerate(all_paths[item], start=1):
        
        print(f"  Path #{i}: {' -> '.join(path)}")

print("===============================")

# TODO (Step 4): traverse the tree starting from least frequent characters (use frequent_items and frequent_nodes to find the starting node)
# for each starting node, traverse the tree by going to the parent until you hit the root
# generate the conditional trees (sets of the node in the path that leads up to that node) 
conditional_pattern_base = {}
for item in reversed(frequent_items):
    for node in frequent_nodes[item[0]]:
        if (node is root):
            continue
        frequency = node.count
        temp = node.parent
        conditional = []
        while (temp is not root):
            conditional.append(temp.item)
            temp = temp.parent
        if (node.item not in conditional_pattern_base):
            conditional_pattern_base[node.item] = []
        conditional_pattern_base[node.item].append((conditional, frequency))

print("CONDITIONAL BASE PATTERNS\n===============================")
for key, paths in conditional_pattern_base.items():
    print(f"{key}:")
    for path, freq in paths:
        print(f"  {path}:{freq}")
print("===============================")

# we need to fix step 5 and step 6

# TODO (Step 5): find the frequent patterns from the conditional trees
# note that unlike in the lecture and lab examples, the given conditional trees INCLUDE the node itself, it'll always be the first element

frequent_patterns = []
minimum_support_count = int(minimumSupport * len(transactionTable))

for key, paths in conditional_pattern_base.items():
    accepted_patterns = []
    accepted_nodes = []
    frequent_patterns_set = set()
    node_frequency = Counter()

    print(f"ITEM -> {key}:")

    for path, count in paths:
        for node in path:
            node_frequency[node] += count

    print(f"CONDITIONAL TREE:")

    for node,freq in node_frequency.items():
        if freq >= minimum_support_count:
            accepted_patterns.append((node,freq))
            accepted_nodes.append (node)
            print(f"{node} : {freq}")

    for length in range(1, len(accepted_nodes)+1):
        for combination in combinations(accepted_nodes, length):
            possible_pattern = tuple(sorted(list(combination) + [key]))
            possible_pattern_set = set(combination)
            possible_pattern_support = 0

            for path, count in paths:
                if possible_pattern_set.issubset(set(path)):
                    possible_pattern_support += count

            if possible_pattern_support >= minimum_support_count:
                frequent_patterns_set.add((possible_pattern,possible_pattern_support))

    print("FREQUENT PATTERNS:")

    for frequent_pattern, support in frequent_patterns_set:
        print(f"{list(frequent_pattern)}:{support}")
        frequent_patterns.append((list(frequent_pattern),support))

    print("===============================")
# TODO (Step 6): for each frequent pattern, generate all possible subsets, excluding the empty subset and the complete subset:  
#                   - For each subset:  
#                       - Find the complementary subset and calculate association rules.  
#                       - Extract strong rules based on the minimum confidence threshold.
#                   - Calculate lift for every strong rule

strong_rules = [] # put the result here
for pattern in frequent_patterns:
    items =set (pattern[0])
    if len(items)<2:
        continue
    for i in range (1,len(items)):
     for subset in combinations (items,i):
        subset=set(subset)
        remain=items - subset
        if not remain :
            continue

        support_both=sum(1 for t in transactionTable if items.issubset(t))/len(transactionTable)
        support_left=sum(1 for t in transactionTable if subset.issubset(t))/len(transactionTable)
        support_right= sum(1 for t in transactionTable if remain.issubset(t)) / len(transactionTable)
        if support_left >0 and support_right >0 :
         confidence =(support_both/support_left)
         lift = confidence / support_right
         if confidence>=minimumConfidence:
            strong_rules.append(
                {
                    'Rule':f"{list(subset)}->{list (remain)}",'support':round(support_both,3),'confidence':round(confidence,3)*100,'lift':round(lift,3)
                }
            )
unique_rules = {rule['Rule']: rule for rule in strong_rules}.values()

print(f"{'RULE':40s} {'SUPPORT':10s} {'CONFIDENCE':12s} {'LIFT':10s}")
print("-" * 75)

for rule in unique_rules:
    print(f"{str(rule['Rule']):40s} "
          f"{rule['support']:<10} "
          f"{rule['confidence']:<12} "
          f"{rule['lift']:<10}")
