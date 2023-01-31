# %% deal with raw data
import pandas as pd
import numpy as np
df = pd.read_csv('examples.csv')
examples = df.to_numpy()
for i in range(examples.shape[-1]):
    if examples[:,i].dtype != str :
        for data in range(len(examples[:,i])):
            examples[data,i] = str(examples[data,i])

# %% tree node
def toLower(array):
    for i in range(len(array)):
        array[i] = array[i].lower()
    return array

class id3_node():
    def __init__(self, node_exp):
        self.leaves = []
        self.node_exp = node_exp
        self.current_attr = None
        self.attr_value = []

    
    def comput_I(self, pos_I, neg_I):
        p_ = (pos_I/(pos_I+neg_I))
        n_ = (neg_I/(pos_I+neg_I))

        if n_ == 0:
            I = - p_*np.log2(p_)
        elif p_ == 0:
            I = - n_*np.log2(n_)
        else:   
            I = - p_*np.log2(p_) - n_*np.log2(n_)
        return I


    def get_gain(self, examples):

        pos_I = float(np.sum(toLower(examples[:,-1]) == 'p'))
        neg_I = float(np.sum(toLower(examples[:,-1]) == 'n'))
        I = self.comput_I(pos_I,neg_I)

        gain_max = 0
        for idx in range(examples.shape[-1]-2):
            current_idx = idx+1
            cur_attr = self.get_attr(examples[:,current_idx])
            E = 0
            for attr in cur_attr:
                cur_exp = examples[toLower(examples[:,current_idx]) == (attr),:]
                pi = np.sum(toLower(cur_exp[:,-1]) == 'p')
                ni = np.sum(toLower(cur_exp[:,-1]) == 'n')
                E = E + ((pi+ni)/(pos_I+neg_I)) * self.comput_I(pi,ni)
            gain = I-E
            if gain > gain_max:
                gain_max = gain
                self.current_attr = current_idx
                self.attr_value = cur_attr
            print('current volum index:'+str(current_idx)+', Gain:'+str(gain))
        return 0

    def set_current_attr(self, root_attr = None):

        if root_attr != None:
            if not ((np.sum((self.node_exp[:,-1] == 'p')+(self.node_exp[:,-1] == 'P')) == self.node_exp.shape[0]) +  (np.sum((self.node_exp[:,-1] == 'n') + (self.node_exp[:,-1] == 'N')) == self.node_exp.shape[0])): 
                self.current_attr = root_attr
                self.attr_value = self.get_attr(self.node_exp[:,self.current_attr])
        else:

            if not ((np.sum((self.node_exp[:,-1] == 'p')+(self.node_exp[:,-1] == 'P')) == self.node_exp.shape[0]) +  (np.sum((self.node_exp[:,-1] == 'n') + (self.node_exp[:,-1] == 'N')) == self.node_exp.shape[0])): 
                self.get_gain(self.node_exp)

        return 0

    def get_attr(self, colum):
        value = []
        for attr in colum:
            if_conflict = False
            for in_attr in value:
                if (in_attr).lower() == (attr).lower():
                    if_conflict = True
            if not if_conflict:
                value.append(attr.lower())
        return value


    def add_node(self, leave):

        self.leaves.append(leave)
        return 0

def add_leave(node):
    if len(node.attr_value)==0:
        return 0
    else:
        for attr in node.attr_value:
            new_node = id3_node(node.node_exp[toLower(node.node_exp[:,node.current_attr]) == attr.lower(),:])
            new_node.set_current_attr()
            node.add_node(new_node)
            add_leave(new_node)

# %% construct root node 
root_node = id3_node(examples)
root_node.set_current_attr()

# %% recursion construct leaves node 
add_leave(root_node)

# %% print attribute of decision tree (Middle order traversal)
def read_node(node):
    if len(node.leaves) == 0:
        return 0
    else:
        for i in range(len(node.leaves)):
            read_node(node.leaves[i])
            print(node.attr_value)
read_node(root_node)
# %%
