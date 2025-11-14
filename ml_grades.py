# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 05:35:23 2025

@author: sheng
@name: Testing with grades
"""
from mlwpy import *

answer_key = np.array([True, True, False, True])
student_answers = np.array([True, True, True, True])


correct = answer_key == student_answers
num_correct = correct.sum()
print('manual accuracy: ', num_correct / len(answer_key))

print('sklearn accuracy: ', metrics.accuracy_score(answer_key, student_answers))
