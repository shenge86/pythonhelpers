# -*- coding: utf-8 -*-
"""
Created on Sun Jul  6 23:06:06 2025

@author: Shen
@name: Covariance Transform
@description:
    
    Describes Cartesian -> Polar transform for 2D
    if given covariance matrix in Cartesian.
"""
import sympy
from sympy import Matrix, simplify, latex, pprint

theta = sympy.symbols('theta')
x, y, r = sympy.symbols('x y r')

# original sigmas
sigma_x  = sympy.symbols('sigma_x')
sigma_y  = sympy.symbols('sigma_y')
sigma_xy = sympy.symbols('sigma_xy')

# covariance matrix in Cartesian defined symbolically
cov_cartesian = Matrix([[sigma_x, sigma_xy], [sigma_xy, sigma_y]])

# Jacobian matrix. We had to take derivatives by hand
Jacobian = Matrix([[sympy.cos(theta), -r*sympy.sin(theta)],[sympy.sin(theta),r*sympy.cos(theta)]])
Jacobian_transpose = Jacobian.T

# COV_POLAR = JACOBIAN * COV_CARTESIAN * JACOBIAN_TRANSPOSE
result1 = Jacobian * cov_cartesian
result1 = result1.applyfunc(simplify)
result2 = result1 * Jacobian_transpose
result2 = result2.applyfunc(simplify)

print(result2)

latex_code = latex(result2)
print(latex_code)

pprint(result2)