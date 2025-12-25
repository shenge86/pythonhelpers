# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 14:15:20 2025

@author: sheng
@name: logistic regression practice
"""
from mlwpy import *
import numpy as np
import pandas as pd

if __name__ == '__main__':
    tail_probs = [0.0, .001, .01, .05, .10, .25, 1.0/3.0]

    lwr_probs = np.array(tail_probs)
    upr_probs = 1 - lwr_probs[::-1]
    cent_prob = np.array([.5])

    probs = np.concatenate([lwr_probs, cent_prob, upr_probs])

    with np.errstate(divide='ignore'):
        odds = probs / (1-probs)
        log_odds = np.log(odds)

    index=['{:4.1f}%'.format(p) for p in np.round(probs,3)*100]

    polo_dict = co.OrderedDict([('Prob (E)', probs),
                                ('Odds(E: not E)', odds),
                                ('Log-Odds', log_odds)])
    
    polo_df = pd.DataFrame(polo_dict, index=index)
    polo_df.index.name='Pct(%)'
    print(polo_df)