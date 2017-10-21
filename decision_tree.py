from csv import reader as rd
from random import random


class DecisionTree:

    def __init__(self, filename, ratio=0.8):
        self.filename = filename
        self.ratio = ratio
        self.dataset = []
        self.training_set = []
        self.test_set = []
        self.root = None
        self.max_depth = 3
        self.min_size = 1

    """
    Opens a CSV file generates training and test sets randomly
    """
    def load_and_parse(self):
        with open(self.filename, 'rb') as data_set:
            lines = rd(data_set)
            data_set = list(lines)
            for x in range(len(data_set) - 1):
                data_set[x][-1] = int(data_set[x][-1])
                for y in range(0, 4, 1):
                    data_set[x][y] = float(data_set[x][y])
                if random() < self.ratio:
                    self.training_set.append(data_set[x])
                else:
                    self.test_set.append(data_set[x])

    """
    Method that checks whether a split is good or bad
    """
    @staticmethod
    def score(groups, classes):
        s = [len(group) for group in groups]
        n = float(sum(s))
        index = 0.0
        for group in groups:
            size = float(len(group))
            if size != 0:
                score = 0.0
                for class_val in classes:
                    p = [row[-1] for row in group].count(class_val) / size
                    score += p * p
                index += (1.0 - score) * (size / n)
        return index

    """
    Splits the dataset in order to make the tree classification.
    The return are two lists with values bellow the given input (bellow)
    and other list with value that are equal or greater (above)
    """
    @staticmethod
    def make_split(index, value, dataset):
        bellow, above = [], []
        for row in dataset:
            if row[index] < value:
                bellow.append(row)
            else:
                above.append(row)
        return bellow, above

    """
    Get a good split for building the decision tree based on the gini index
    """
    def get_split(self, dataset):
        classes = list(set(row[-1] for row in dataset))
        b_index, b_value, b_score, b_groups = 999, 999, 999, None
        for index in range(len(dataset[0])-1): # Except for the class value
            for row in dataset:
                groups = self.make_split(index, row[index], dataset)
                score = self.score(groups, classes)
                if score < b_score:
                    b_index, b_value, b_score, b_groups = index, row[index], score, groups
        return {
            'index': b_index,
            'value': b_value,
            'groups': b_groups
        }

    """
    """
    @staticmethod
    def terminal(group):
        outcomes = [row[-1] for row in group]
        return max(set(outcomes), key=outcomes.count)

    """
    Create child splits for a node or make terminal
    """
    def split(self, node, max_depth, min_size, depth):
        left, right = node['groups']
        del(node['groups'])
        if not left or not right:
            node['left'] = node['right'] = self.terminal(left + right)
            return
        if depth >= max_depth: # Max depth
            node['left'], node['right'] = self.terminal(left), self.terminal(right)
            return
        if len(left) <= min_size: # Left child
            node['left'] = self.terminal(left)
        else: # Right child
            node['left'] = self.get_split(left)
            self.split(node['left'], max_depth, min_size, depth+1) # Recursive call to left
        # process right child
        if len(right) <= min_size:
            node['right'] = self.terminal(right)
        else:
            node['right'] = self.get_split(right)
            self.split(node['right'], max_depth, min_size, depth+1) # Recursive call to right

    """
    Makes splits and actually build the decision tree
    """
    def build_decision_tree(self):
        self.root = self.get_split(self.training_set)
        self.split(self.root, self.max_depth, self.min_size, 1)

    """
    Predicts class of a test point
    """
    def predict_rec(self, node, row):
        if row[node['index']] < node['value']:
            if isinstance(node['left'], dict):
                return self.predict_rec(node['left'], row)
            else:
                return node['left']
        else:
            if isinstance(node['right'], dict):
                return self.predict_rec(node['right'], row)
            else:
                return node['right']

    """
    Wrapper for the recursive predict
    """
    def predict(self, instance):
        return self.predict_rec(self.root, instance)

    """
    Fits the model
    """
    def fit(self):
        self.load_and_parse()
        self.build_decision_tree()


decision_tree = DecisionTree(filename='data_banknote_authentication.csv', ratio=0.75)
decision_tree.fit()
test_points = decision_tree.test_set
correct = 0
for test_point in test_points:
    prediction = decision_tree.predict(test_point)
    expected = test_point[-1]
    if prediction == expected:
        correct += 1
percentage = float(correct) / len(test_points)
print "Accuracy: %.2f%% (%d out of %d)" % (percentage * 100, correct, len(test_points))
