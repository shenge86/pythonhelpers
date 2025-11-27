# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 19:24:53 2025

@author: Shen
@name: Simple Classification Dataset
@description:
    Practice machine learning classification
"""
from mlwpy import *

#%% load up iris dataset
iris = datasets.load_iris()

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
display(pd.concat([iris_df.head(3),
                   iris_df.tail(3)]))

sns.pairplot(iris_df, hue='target', size=1.5)

print('targets: {}'.format(iris.target_names), iris.target_names[0], sep='\n')
# targets: ['setosa' 'versicolor' 'virginica']
# setosa

#%% simple train-test split
(iris_train_ftrs, iris_test_ftrs,
 iris_train_tgt,  iris_test_tgt) = skms.train_test_split(iris.data, iris.target, test_size=.25)

print('Train features shape: ', iris_train_ftrs.shape)
print('Test features shape: ', iris_test_ftrs.shape)

#%% build a k-NN classification model
knn   = neighbors.KNeighborsClassifier(n_neighbors=3)
fit   = knn.fit(iris_train_ftrs, iris_train_tgt)
preds = fit.predict(iris_test_ftrs)

# evaluate prediction against held-back testing targets
print('3NN accuracy: ', metrics.accuracy_score(iris_test_tgt, preds))