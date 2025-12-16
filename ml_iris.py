# -*- coding: utf-8 -*-
"""
Created on Sat Jan 11 19:24:53 2025

@author: Shen
@name: Simple Classification Dataset
@description:
    Practice machine learning classification
    
    Fit estimator on training data 
    and then
    use fit-estimator to predict on test data
    
    Steps are as follows:
        1. Build the model.
        2. Fit the model using training data.
        3. Predict using fit model on testing data.
        4. Evaluate quality of predictions.
"""
from mlwpy import *

#%% load up iris dataset
iris = datasets.load_iris()

iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
# iris dataframe headers are as such:
# sepal length (cm), sepal width (cm), petal length (cm), petal width (cm), target
# classification targets as such:
# 0 = setosa
# 1 = versicolor
# 2 = virginica

# show the 1st 3 and last 3 in ipython console
display(pd.concat([iris_df.head(3),
                   iris_df.tail(3)]))

sns.pairplot(iris_df, hue='target', height=1.5)

print('targets: {}'.format(iris.target_names), iris.target_names[0], sep='\n')
# targets: ['setosa' 'versicolor' 'virginica']
# setosa

#%% simple train-test split
(iris_train_ftrs, iris_test_ftrs,
 iris_train_tgt,  iris_test_tgt) = skms.train_test_split(iris.data, iris.target, test_size=.33, random_state=21)

print('Train features shape (# examples, # features): ', iris_train_ftrs.shape)
print('Test features shape  (# examples, # features): ', iris_test_ftrs.shape)

#%% build a k-NN classification model
# 3 here is a hyperparameter (not trained or manipulated by learning method)
# knn   = neighbors.KNeighborsClassifier(n_neighbors=3)
# fit   = knn.fit(iris_train_ftrs, iris_train_tgt)
# tgt_preds = fit.predict(iris_test_ftrs)


#%% do all in one for this
# K-Nearest Neighbors Method
# Describe similarity between paris of examples.
# Pick several most-similar examples.
# Combine these picks to get single answer.
# Expand neighborhood to get several nearby neighbors protect us from noise in the data.
tgt_preds = (neighbors.KNeighborsClassifier() # default is 5
                      .fit(iris_train_ftrs, iris_train_tgt)
                      .predict(iris_test_ftrs))

# evaluate prediction against held-back testing targets
print('3NN accuracy: ', metrics.accuracy_score(iris_test_tgt, tgt_preds))

# other metric with confusion matrix
cm = metrics.confusion_matrix(iris_test_tgt, tgt_preds)
print('confusion matrix: ', cm, sep='\n')

# just plot it
fig, ax = plt.subplots(1,1, figsize=(4,4))
ax = sns.heatmap(cm, annot=True, square=True,
                 xticklabels=iris.target_names,
                 yticklabels=iris.target_names)
ax.set_xlabel('Predicted')
ax.set_ylabel('Actual')