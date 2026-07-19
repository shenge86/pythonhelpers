"""
@author: Shen Ge
@name: Geometry Converter
@description:
Converts geometric shapes etc.
"""
import numpy as np

def genspherearea(N):
    for i in range(N):
        yield 4*np.pi*i**2

def gencubearea(N):
    for i in range(N):
        yield 6*i**2

if __name__ == '__main__':
    N=5
    xsphere = genspherearea(N)

    for i in genspherearea(N):
        print(i, end= ': ')

    print('\n')
    print('-----------------')
    print('\n')

    xcube = gencubearea(N)
    for i in gencubearea(N):
        print(i, end= ': ')

    x = gencubearea(3)
    next(x)
    next(x)
    next(x)
    next(x)
    next(x)
