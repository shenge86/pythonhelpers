from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# This presents an example of curve fitting to Longley's Economic Regression Data
# Longley's Economic Regression Data
#
# Description
# A macroeconomic data set which provides a well-known example for a highly collinear regression.
#
# Format
# A data frame with 7 economical variables, observed yearly from 1947 to 1962 (n=16).

# Columns are as follows:
# 0 GNP.deflator: GNP implicit price deflator (1954=100)
# 1 GNP: Gross National Product.
# 2 Unemployed: number of unemployed.
# 3 Armed.Forces: number of people in the armed forces.
# 4 Population: ‘noninstitutionalized’ population ≥ 14 years of age.
# 5 Year: the year (time).
# 6 Employed: number of people employed.
#
# Source
# J. W. Longley (1967) An appraisal of least-squares programs from the point of view of the user. Journal of the American Statistical Association 62, 819–841.
#
# References
# Becker, R. A., Chambers, J. M. and Wilks, A. R. (1988) The New S Language. Wadsworth & Brooks/Cole.

# create objective function
def objective_linear(x,a,b):
    return a*x+b

def objective_quadratic(x,a,b,c):
    return a*x**2 + b*x + c

def objective_sinecombo(x,a,b,c,d):
	return a * np.sin(b - x) + c * x**2 + d

# read in data and convert to 2D numpy array
url = 'https://raw.githubusercontent.com/shenge86/pythonhelpers/master/longley.csv'
df = read_csv(url,header=None)
data = df.values

# choose the input and output variables
x, y = data[:, 4], data[:, -1]
# plot input vs output
plt.scatter(x, y, label='Raw Data')
plt.xlabel('Population')
plt.ylabel('Employed')
plt.legend(loc='lower right')
plt.savefig('rawdata_populationvsemployed.png')

# do linear fit
fit_paramsL, covariances = curve_fit(objective_linear, x, y)
a, b = fit_paramsL
print('Parameter values: ')
print('y = %.5f * x + %.5f' % (a, b))
x_monotonic = np.arange(min(x),max(x),1)
y_fit = objective_linear(x_monotonic,*fit_paramsL)
plt.plot(x_monotonic,y_fit,'--',color='blue',label='Linear Fit')
plt.legend(loc='lower right')
plt.savefig('populationvsemployed_linearfit.png')

# do quadratic fit
fit_paramsQ, covariances = curve_fit(objective_quadratic, x, y)
a, b, c = fit_paramsQ
print('Parameter values: ')
print('y = %.5f * x^2 + %.5f * x + %.5f' % (a, b, c))
y_fit = objective_quadratic(x_monotonic,*fit_paramsQ)
plt.plot(x_monotonic,y_fit,'--',color='red',label='Quadratic Fit')
plt.legend(loc='lower right')
plt.savefig('populationvsemployed_quadratic.png')

# do increasing sine fit
fit_params, covariances = curve_fit(objective_sinecombo, x, y)
a, b, c, d = fit_params
print('Parameter values: ')
print('y = %.5f * sin(%.5f - x) + %.5f * x^2 + %.5f' % (a, b, c, d))
y_fit = objective_sinecombo(x_monotonic,*fit_params)
plt.plot(x_monotonic,y_fit,'--',color='green',label='Sine+Quadratic Fit')
plt.legend(loc='lower right')
plt.savefig('populationvsemployed_all.png')
plt.show()

#%%
# see how far apart everything is
print('Linear model error: ', np.linalg.norm(y-objective_linear(x,*fit_paramsL)))
print('Quadratic model error: ', np.linalg.norm(y-objective_quadratic(x,*fit_paramsQ)))
print('Sine combo model error: ', np.linalg.norm(y-objective_sinecombo(x,*fit_params)))
