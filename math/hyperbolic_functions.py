import numpy as np
import scipy.special as sp
import matplotlib.pyplot as plt

# approximation formula for tanh(x) using Taylor series expansion
# tanh(x) = sum_{n=1}^inf (2^(2n) * (2^(2n) - 1) * B_2n / (2n)!) * x^(2n-1)
# where B_2n are Bernoulli numbers
def tanh_approximation(x, n_terms):
    approximation = 0
    bernoulli_numbers = sp.bernoulli(2 * n_terms)
    for n in range(1, n_terms + 1):
        B_2n = bernoulli_numbers[2 * n]
        term = ((2**(2*n) * (2**(2*n) - 1) * B_2n) / sp.factorial(2*n)) * x**(2*n - 1)
        approximation += term
    return approximation

# x coordinates for plotting
x = np.linspace(-np.pi/2, np.pi/2, 100)

sinh_x = np.sinh(x)
cosh_x = np.cosh(x)
deltasquared = np.cosh(x)**2 - np.sinh(x)**2
tanh_x = np.tanh(x)

# approximations to tanh_x for small x using Taylor series expansion
x0 = tanh_approximation(x, 1) # same as x
x1 = tanh_approximation(x, 2) # same as x - x**3 / 3
x2 = tanh_approximation(x, 3) # same as x - x**3 / 3 + 2 * x**5 / 15
x3 = tanh_approximation(x, 4) # same as x - x**3 / 3 + 2 * x**5 / 15 - 17 * x**7 / 315
x4 = tanh_approximation(x, 5) # same as x - x**3 / 3 + 2 * x**5 / 15 - 17 * x**7 / 315 + 62 * x**9 / 2835
x5 = tanh_approximation(x, 6) # same as x - x**3 / 3 + 2 * x**5 / 15 - 17 * x**7 / 315 + 62 * x**9 / 2835 - 1382 * x**11 / 155925
x6 = tanh_approximation(x, 7) # same as x - x**3 / 3 + 2 * x**5 / 15 - 17 * x**7 / 315 + 62 * x**9 / 2835 - 1382 * x**11 / 155925 + 21844 * x**13 / 6081075

fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(x, sinh_x, label="sinh(x)")
ax1.plot(x, cosh_x, label="cosh(x)")
ax1.plot(x, deltasquared, label="cosh²(x) - sinh²(x)")
ax1.plot(x, tanh_x, label="tanh(x)")

ax1.axhline(0, color="black", linewidth=0.5)
ax1.axvline(0, color="black", linewidth=0.5)
ax1.set_title("Hyperbolic Functions")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.legend()
ax1.grid(True)

fig1.savefig("hyperbolic_functions.png", dpi=150)

fig2, ax2 = plt.subplots(figsize=(8, 6))
ax2.plot(x, tanh_x, label="tanh(x)")
ax2.plot(x, x0, label="x")
ax2.plot(x, x1, label="x-x³/3")
ax2.plot(x, x2, label="x-x³/3 + 2x⁵/15")
ax2.plot(x, x3, label="x-x³/3 + 2x⁵/15 - 17x⁷/315")
ax2.plot(x, x4, label="x-x³/3 + 2x⁵/15 - 17x⁷/315 + 62x⁹/2835")
ax2.plot(x, x5, label="x-x³/3 + 2x⁵/15 - 17x⁷/315 + 62x⁹/2835 - 1382x¹¹/155925")
ax2.plot(x, x6, label="x-x³/3 + 2x⁵/15 - 17x⁷/315 + 62x⁹/2835 - 1382x¹¹/155925 + 21844x¹³/6081075")
ax2.set_title("Approximations to tanh(x)")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.legend()
ax2.grid(True)
fig2.savefig("hyperbolic_tangent_approximations.png", dpi=150)

# show all plots at end
plt.show()

