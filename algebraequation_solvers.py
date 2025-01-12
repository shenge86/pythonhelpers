# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 17:02:17 2023

@author: Shen
"""

from sympy import symbols, Abs, solve_univariate_inequality, Interval, solve, Eq

#%% solve inequality
# Define the variable
x = symbols('x')

# Define the absolute value inequality
inequality = Abs(x - 2) < 5
inequality 

# Solve the inequality
solution = solve_univariate_inequality(inequality, x, relational=False)

# Print the solution
print(solution)

#%%
# # Define the linear inequalities
# inequality1 = Eq(2*x + 3*y, 8)
# inequality2 = Eq(x - y, 1)

# # Solve the system of inequalities
# solution = solve((inequality1, inequality2), (x, y))

# # Print the solution
# print(solution)

#%%
# composition of functions
# Step 1: Define the function and the variable symbol
x, y = symbols('x y')

# Define a function (e.g., f(x) = 2x + 3)
original_function = 2 * x + 3

# Step 2: Use SymPy to find the inverse
# Solve for y in terms of x
inverse_function_expr = solve(Eq(original_function, y), x)

# The inverse function is y = inverse_function_expr
print("Inverse function:", inverse_function_expr)

