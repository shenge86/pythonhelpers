# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 16:32:59 2025

@author: sheng
@name: test learners
@description:
    
    Chapter 5 of the book
"""

from mlwpy import *
# diabetes = datasets.load_diabetes

#%%
N = 20
ftr = np.linspace(-10, 10, num=N)
tgt = 2*ftr**2 - 3 + np.random.uniform(-2, 2, N)

(train_ftr, test_ftr, train_tgt, test_tgt) = skms.train_test_split(ftr, tgt, test_size=N//2)

display(pd.DataFrame({"ftr": train_ftr,
              "tgt": train_tgt}))

#%%
plt.plot(train_ftr, train_tgt, 'bo') # training set
plt.plot(test_ftr, np.zeros_like(test_ftr), 'r+') # input feature values

# predict a numerical target value from an input
sk_model = linear_model.LinearRegression()
sk_model.fit(train_ftr.reshape(-1,1), train_tgt)
sk_preds = sk_model.predict(test_ftr.reshape(-1,1))
sk_preds[:3]