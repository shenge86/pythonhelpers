# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 19:47:32 2025

@author: sheng
@name: Decisision Tree test
"""
from mlwpy import *

iris = datasets.load_iris()

# standard iris dataset
tts = skms.train_test_split(iris.data, iris.target, test_size=.33, random_state=21)
(iris_train_ftrs, iris_test_ftrs,
 iris_train_tgt, iris_test_tgt) = tts

# one-class variation
useclass = 1
tts_1c = skms.train_test_split(iris.data, iris.target==useclass,
                               test_size=.33, random_state = 21)

(iris_1c_train_ftrs, iris_1c_test_ftrs,
 iris_1c_train_tgt, iris_1c_test_tgt) = tts_1c

#%% tree classifiers
tree_classifiers = {'DTC': tree.DecisionTreeClassifier(max_depth=3)}

fig, ax = plt.subplots(1,1, figsize=(4,3))
for name, mod in tree_classifiers.items():
    # plot_boundary only uses specified columns
    # [0,1] [sepal len/width] to predict and graph
    plot_boundary(ax, iris.data, iris.target, mod, [0,1])
    ax.set_title(name)
plt.tight_layout()