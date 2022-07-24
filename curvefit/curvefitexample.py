import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from pytictoc import TicToc

t = TicToc()

def g(x, A, μ, σ):
    return A / (σ * math.sqrt(2 * math.pi)) * np.exp(-(x-μ)**2 / (2*σ**2))

def f(x):
    return np.exp(-(x-2)**2) + np.exp(-(x-6)**2/10) + 1/(x**2 + 1)

# A = 100.0 # intensity
# μ = 4.0  # mean
# σ = 4.0 # peak width
n = 500 # Number of data points in signal
# x = np.linspace(-10, 10, n)
# y = g(x, A, μ, σ) + np.random.randn(n)

#%% NOW FOR THE ACTUAL TEST #%%
t.tic() # start clock

def cost(parameters):
    '''Minimize the sum of the squares of the residuals
    between the measured y and the calculated y'''
    g_0 = parameters[:3]
    g_1 = parameters[3:6]
    return np.sum(np.power(g(x, *g_0) + g(x, *g_1) - y, 2)) / len(x)

g_0 = [250.0, 4.0, 5.0]
g_1 = [20.0, -5.0, 1.0]

x = np.linspace(-10, 10, n)
# experimental data in reality would be measured but here we are just
# adding a perturbation around the original function to generate some data
y = g(x, *g_0) + g(x, *g_1) + np.random.randn(n)

initial_guess = [5, 10, 4, 20, -6, 4]
result = optimize.minimize(cost, initial_guess,tol=1e-6)
yfit = g(x,*result.x[0:3]) + g(x,*result.x[3:6])

print('Root of the mean of the squared values of deltas: ', np.sqrt(np.mean((y-yfit)**2)))
print('Using the cost function acutally used to minimize...')
print('Cost function (sum of the squares of the residuals divided by length of data): ', np.sum(np.power(g(x, *g_0) + g(x, *g_1) - y, 2)) / len(x))
print('Calculated best fit parameter values: ', result.x)
print('Calculated deltas: ', result.x - np.concatenate([g_0,g_1]))

fig, ax = plt.subplots()
ax.scatter(x, y, s=1, label='Experimental results')
ax.plot(x, g(x, *g_0),label='g_0 function')
ax.plot(x, g(x, *g_1),label='g_1 function')
ax.plot(x, g(x,*g_0) + g(x,*g_1),label='g_0 + g_1 function')
ax.plot(x, yfit, label='Experimental results fit')
ax.legend()
plt.xlabel('x')
plt.ylabel('y')
fig.savefig('curvefitexample.png')

t.toc()  # stop clock and print elapsed time
np.savetxt('curvefitexample.out', (x,y), delimiter=',') # Save signal to file
