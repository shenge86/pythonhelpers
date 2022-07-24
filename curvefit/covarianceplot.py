###############
# @name: covariance plotter
# plots error variances and covariances
# for a set of data
#
# Remember that covariance measures PRECISION of data and not accuracy!!!
# For how far off we are from the truth (which we can use based on a trusted model),
# please use the separate error calculator.

# To generate the 'truth', we can either use trusted dynamics models propagated
# (if dealing with kinematics) or we might have done a curve fit on trusted empirical data.
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms


def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.

    Parameters
    ----------
    x, y : array-like, shape (n, )
        Input data.

    ax : matplotlib.axes.Axes
        The axes object to draw the ellipse into.

    n_std : float
        The number of standard deviations to determine the ellipse's radiuses.

    **kwargs
        Forwarded to `~matplotlib.patches.Ellipse`

    Returns
    -------
    matplotlib.patches.Ellipse
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])

    # Using a special case to obtain the eigenvalues of this
    # two-dimensionl dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the stdandard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    # scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the stdandard deviation of y ...
    # scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    # print out some useful info:
    print('Variance (first variable): ', cov[0,0])
    print('Variance (second variable): ', cov[1,1])
    print('Covariance (cross terms): ', cov[0,1])
    print('Mean (first variable): ', mean_x)
    print('Mean (second variable): ', mean_y)

    print('''
    Unless your covariance is already determined by a frame with its x axis as the best linear fit line,
    we must do coordinate transformation to plot the ellipse properly!
    Must find principal components frame.
    ''')
    # which is the new modified axis along the direction of the line of best linear fit
    # as well as the perpendicular axis to the line of best fit
    # this is equivalent to finding square root of eigenvalues for new semimajor & semiminor axis lengths
    # and finding geometry of angle based on eigenvector
    lambdas, vecs = np.linalg.eig(cov)
    eigvec0 = vecs[:,0]
    scale_x = n_std * np.sqrt(lambdas[0])
    scale_y = n_std * np.sqrt(lambdas[1])
    # rotation calculator
    # angle of 0 or 90 means zero correlation between the two variables
    # angle of 0 degrees means vertical    (changes in y have major effect)
    # angle of 90 degrees means horizontal (changes in x have major effect)
    theta = np.rad2deg(np.arctan2(eigvec0[1],eigvec0[0]))

    print('Ellipse scale x: ', scale_x)
    print('Ellipse scale y: ', scale_y)
    print('Rotation angle (deg): ', theta)

    # transform by shifting center of ellipse to mean xy coordinate
    # and rotating by angle appropriately
    transf = transforms.Affine2D() \
        .rotate_deg(theta+45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def get_correlated_dataset(n, dependency, mu, scale):
    """
    Creates a random two-dimesional dataset with the specified two-dimensional mean (mu) and dimensions (scale).
    The correlation can be controlled by the param 'dependency', a 2x2 matrix.
    DO NOT USE IF YOU HAVE ACTUAL DATA!
    """
    latent = np.random.randn(n, 2)
    dependent = latent.dot(dependency)
    scaled = dependent * scale
    scaled_with_offset = scaled + mu
    # return x and y of the new, correlated dataset
    return scaled_with_offset[:, 0], scaled_with_offset[:, 1]

#%%%%%%%%%%%%
if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except:
        filename = input('Enter csv data file with delimiter: ')

    try:
        df = pd.read_csv(filename)
    except:
        print('Could not find or read in csv. Using default!')
        filename = "donnees_exo9.csv"
        df = pd.read_csv(filename, sep=";")
        # df = pd.read_csv("dataexample.csv", sep=",")

    # calculate covariance matrix
    # variance = sum((value - mean of sample)**2)/(total number of samples - 1)
    varx_manual = sum((df.x-df.mean().x)**2)/(len(df.x)-1)
    vary_manual = sum((df.y-df.mean().y)**2)/(len(df.y)-1)

    varx = df.var().x
    vary = df.var().y

    # calculate covariance
    varxy_manual = sum((df.x-df.mean().x)*(df.y-df.mean().y))/(len(df.x)-1)

    # autogenerate covariance matrix
    covmatrix = df.loc[:,['x','y']].cov().to_numpy()

    print("Covariance matrix from pandas:\n", covmatrix)

    #%%%%%%%%%% plot it
    fig, ax = plt.subplots()
    ax.scatter(df.x,df.y,s=0.5)
    ax.axvline(c='grey', lw=1)
    ax.axhline(c='grey', lw=1)

    stdeviation = 3.0
    confidence_ellipse(df.x, df.y, ax, n_std=stdeviation, edgecolor='red')
    ax.scatter(df.mean().x,df.mean().y,c='red',s=3)
    ax.set_title(f'Confidence Ellipse with Standard Deviation {stdeviation}')

    fig.savefig(f'{filename}_covariance.png')
