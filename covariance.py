# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 22:54:37 2023

@author: Shen
@name: Covariance Plotter
@source: 
    https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html
    https://carstenschelp.github.io/2018/09/14/Plot_Confidence_Ellipse_001.html
    https://www.visiondummy.com/2014/04/draw-error-ellipse-representing-covariance-matrix
    
    
    For quick reference, here is the Chi-square probabilities.
    For 2D dataset requiring a 95% confidence interval, i.e. 95% of data will fall into ellipse,
    we will use P(s < 5.991) = 1 - 0.05 = 0.95 
    which on table we look at df=2 and column header of 0.05
    
df	0.995	0.99 	0.975	0.95	    0.90  	0.10 	0.05 	0.025	0.01	    0.005
1	---	    ---	    0.001  	0.004	0.016	2.706	3.841	5.024	6.635	7.879
2	0.010	0.020	0.051	0.103	0.211	4.605	5.991	7.378	9.210	10.597
3	0.072	0.115	0.216	0.352	0.584	6.251	7.815	9.348	11.345	12.838
4	0.207	0.297	0.484	0.711	1.064	7.779	9.488	11.143	13.277	14.860
5	0.412	0.554	0.831	1.145	1.610	9.236	11.070	12.833	15.086	16.750
6	0.676	0.872	1.237	1.635	2.204	10.645	12.592	14.449	16.812	18.548
7	0.989	1.239	1.690	2.167	2.833	12.017	14.067	16.013	18.475	20.278
8	1.344	1.646	2.180	2.733	3.490	13.362	15.507	17.535	20.090	21.955
9	1.735	2.088	2.700	3.325	4.168	14.684	16.919	19.023	21.666	23.589
10	2.156	2.558	3.247	3.940	4.865	15.987	18.307	20.483	23.209	25.188
11	2.603	3.053	3.816	4.575	5.578	17.275	19.675	21.920	24.725	26.757
12	3.074	3.571	4.404	5.226	6.304	18.549	21.026	23.337	26.217	28.300
13	3.565	4.107	5.009	5.892	7.042	19.812	22.362	24.736	27.688	29.819
14	4.075	4.660	5.629	6.571	7.790	21.064	23.685	26.119	29.141	31.319
15	4.601	5.229	6.262	7.261	8.547	22.307	24.996	27.488	30.578	32.801
16	5.142	5.812	6.908	7.962	9.312	23.542	26.296	28.845	32.000	34.267
17	5.697	6.408	7.564	8.672	10.085	24.769	27.587	30.191	33.409	35.718
18	6.265	7.015	8.231	9.390	10.865	25.989	28.869	31.526	34.805	37.156
19	6.844	7.633	8.907	10.117	11.651	27.204	30.144	32.852	36.191	38.582
20	7.434	8.260	9.591	10.851	12.443	28.412	31.410	34.170	37.566	39.997
21	8.034	8.897	10.283	11.591	13.240	29.615	32.671	35.479	38.932	41.401
22	8.643	9.542	10.982	12.338	14.041	30.813	33.924	36.781	40.289	42.796
23	9.260	10.196	11.689	13.091	14.848	32.007	35.172	38.076	41.638	44.181
24	9.886	10.856	12.401	13.848	15.659	33.196	36.415	39.364	42.980	45.559
25	10.520	11.524	13.120	14.611	16.473	34.382	37.652	40.646	44.314	46.928
26	11.160	12.198	13.844	15.379	17.292	35.563	38.885	41.923	45.642	48.290
27	11.808	12.879	14.573	16.151	18.114	36.741	40.113	43.195	46.963	49.645
28	12.461	13.565	15.308	16.928	18.939	37.916	41.337	44.461	48.278	50.993
29	13.121	14.256	16.047	17.708	19.768	39.087	42.557	45.722	49.588	52.336
30	13.787	14.953	16.791	18.493	20.599	40.256	43.773	46.979	50.892	53.672
40	20.707	22.164	24.433	26.509	29.051	51.805	55.758	59.342	63.691	66.766
50	27.991	29.707	32.357	34.764	37.689	63.167	67.505	71.420	76.154	79.490
60	35.534	37.485	40.482	43.188	46.459	74.397	79.082	83.298	88.379	91.952
70	43.275	45.442	48.758	51.739	55.329	85.527	90.531	95.023	100.425	104.215
80	51.172	53.540	57.153	60.391	64.278	96.578	101.879	106.629	112.329	116.321
90	59.196	61.754	65.647	69.126	73.291	107.565	113.145	118.136	124.116	128.299
100	67.328	70.065	74.222	77.929	82.358	118.498	124.342	129.561	135.807	140.169

Can also look at:
    https://www.reid.ai/2012/09/chi-squared-distribution-table-with.html
"""

import sys, os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from matplotlib.ticker import MultipleLocator

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', verbose=False, testing=False, **kwargs):
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
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)
    
    rotatedeg = 45 # degrees (always true)
    
    ###
    if testing:
        # for testing only for plots; please comment out
        mean_x, mean_y = 0,0
        rotatedeg = 0
        # scale_x, scale_y = 5,5
    ###

    transf = transforms.Affine2D() \
        .rotate_deg(rotatedeg) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    
    # if verbose then print out more info
    if verbose:
        print('Horizontal radius (before scaling): ', ell_radius_x)
        print('Vertical   radius (before scaling): ', ell_radius_y)
        print('Scale (x): ', scale_x)
        print('Scale (y): ', scale_y)
        print('Final radius (x): ', ell_radius_x * scale_x)
        print('Final radius (y): ', ell_radius_y * scale_y)
        print('Mean (x):  ', mean_x)
        print('Mean (y):  ', mean_y)    
    
    return ax.add_patch(ellipse)

#%%
def ellipse_parameters(data, dof=1, nstd=3, verbose=False):
    # Calculate mean and covariance matrix
    mean = np.mean(data, axis=0)
    cov_matrix = np.cov(data, rowvar=False)

    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

    # Sort eigenvalues and eigenvectors in decreasing order
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # calculate scale up for axis depending on degree of freedom and standard deviation desired
    if dof==1:
        scaledup = nstd
    elif dof==2:
        if nstd == 1:
            scaledup = np.sqrt(2.3)
        elif nstd == 2:
            scaledup = np.sqrt(6.18)
        elif nstd == 3:
            scaledup = np.sqrt(11.83)
    elif dof==3:
        if nstd == 1:
            scaledup = np.sqrt(3.53)
        elif nstd == 2:
            scaledup = np.sqrt(8.02)
        elif nstd == 3:
            scaledup = np.sqrt(14.16)

    # Determine ellipse parameters
    semi_major = scaledup * np.sqrt(eigenvalues[0])
    semi_minor = scaledup * np.sqrt(eigenvalues[1])
    angle = np.degrees(np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0]))
    
    if verbose:
        print('Eigenvalue (major): ', eigenvalues[0])
        print('Eigenvalue (minor): ', eigenvalues[1])
        print('Scale factor: ', scaledup)
        print('Semimajor axis: ', semi_major)
        print('Semiminor axis: ', semi_minor)
        print('Angle: ', angle)
    
    return semi_major, semi_minor, angle, mean


#%%
def get_correlated_dataset(n, dependency, mu, scale):
    '''
    Function to generate a correlated dataset of n sets of 2 quantities based on three things:
        1. dependency (correlation matrix 2x2)
        [[1,0],[0,1]] aka identity matrix will be completely uncorrelated data
        2. mu (mean of the data aka additive factor to data)
        This will be added to each set of numbers after everything else
        (0,0) will mean no translation to the data
        3. scale (multiplicative factor to data)
        This will be multiplied to each set of numbers prior to adding mean
        (1,1) will mean no stretching of the data
    '''
    latent = np.random.randn(n, 2)
    dependent = latent.dot(dependency)
    scaled = dependent * scale
    scaled_with_offset = scaled + mu
    # return x and y of the new, correlated dataset
    return scaled_with_offset[:, 0], scaled_with_offset[:, 1]



#%%
if __name__ == '__main__':
    # by default set the runtype argument to be in covariance folder
    runtype = 'covariance/Positive_correlation.csv'
    
    for arg in sys.argv[1:]:
        # print(arg)
        if arg[-3:] in ['txt','csv']:
            print('Reading in data file in the folder covariance.')
            runtype = arg
            
        if arg[0:3] in ['dof']:
            dof = int(arg[3:])
        else:
            dof = 1
        
    if '-verbose' in sys.argv:
        verbose = True
    else:
        verbose = False
        
    if '-testing' in sys.argv:
        testing = True
    else:
        testing = False
        
    print(f'''
          =========INPUT SETTINGS============
          Runtype (file or example): {runtype}
          Degree of freedom assumed: {dof}
          Verbosity                : {verbose}
          Testing                  : {testing}
          ''')
    
    
    # make covariance folder if doesn't exist
    if not os.path.exists('covariance'):
        print('Covariance folder not found. Creating folder named covariance.')
        os.makedirs('covariance')
        
    if runtype[-3:] in ['txt','csv']:
        print('Reading in pre-existing data for analysis.')
        try:
            df = pd.read_csv(runtype)
        except:
            print(f'Successfully read in covariance/{runtype} file!')
            df = pd.read_csv('covariance/'+runtype)
            
        print('Generate the correlation matrix as such...')
        corr_matrix = df.corr().round(2)
        print('Correlation matrix: ')
        print(corr_matrix)

        x = np.array(df.iloc[:,0])
        y = np.array(df.iloc[:,1])        
        print('Mean (x): ', np.mean(x))
        print('Mean (y): ', np.mean(y))
        
        #%% calculate covariance the 'traditional' way
        eigenvalues, eigenvectors = np.linalg.eig(np.cov(x,y))
        
        #%% create the plot using nontraditional way
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.scatter(x, y, s=0.5)
        
        mu = np.mean(x), np.mean(y)
        ax.scatter(mu[0], mu[1], c='red', s=0.5)
        
        print('Error ellipse with std=2')
        confidence_ellipse(x, y, ax, n_std=2, verbose = verbose, testing = testing,
                           label=r'$2\sigma$', edgecolor='fuchsia', linestyle='--')
        
        print('-----------------------------------')
        print('Error ellipse with std=3')
        confidence_ellipse(x, y, ax, n_std=3, verbose=verbose, testing = testing,
                           label=r'$3\sigma$', edgecolor='blue', linestyle=':')
        
        
        print('-----------------------------------')
        #%% create covariance plot the traditional way
        data = df.values

        # Create the ellipse
        semi_major, semi_minor, angle, mean = ellipse_parameters(data,dof=1,nstd=2,verbose=verbose)
        ellipse2sigma = Ellipse(xy=mu, width=semi_major * 2, height=semi_minor * 2, angle=angle, 
                          edgecolor='yellow', facecolor='none', label=r'$2\sigma$ (w/ eigenvalues)')
        plt.gca().add_patch(ellipse2sigma)
        
        # Create the ellipse
        semi_major, semi_minor, angle, mean = ellipse_parameters(data,dof=1,nstd=3,verbose=verbose)
        ellipse3sigma = Ellipse(xy=mu, width=semi_major * 2, height=semi_minor * 2, angle=angle, 
                          edgecolor='red', facecolor='none', label=r'$3\sigma$ (w/ eigenvalues)')
        plt.gca().add_patch(ellipse3sigma)
        
        
        plt.grid(color = 'green', linestyle = '--', linewidth = 0.5)
        ax.set_title('Covariance Ellipse with STDs assuming ')
        ax.legend()
        
        figurename = 'covarianceplot_' + os.path.basename(runtype)
        plt.savefig(f'covariance/{figurename}.png')
        plt.show()
    
    elif runtype in ['example']:
        #%%
        np.random.seed(0)
        
        PARAMETERS = {
            'Positive_correlation': [[0.85, 0.35],
                                     [0.15, -0.65]],
            'Negative_correlation': [[0.9, -0.4],
                                     [0.1, -0.6]],
            'Weak_correlation': [[1, 0],
                                 [0, 1]],
        }
        
        mu = 2, 4
        scale = 3, 5
        
        fig, axs = plt.subplots(1, 3, figsize=(9, 3))
        for ax, (title, dependency) in zip(axs, PARAMETERS.items()):
            x, y = get_correlated_dataset(800, dependency, mu, scale)
            
            # if saveinput is in the command line argument then create multiple data frames
            if '-saveinput' in sys.argv:
                print('Saving the randomly generated data for later ingestion and reuse.')
                data = {'x': x, 'y': y}
                df   = pd.DataFrame(data)
                df.to_csv(f'covariance/{title}.csv',index=False)
            
            ax.scatter(x, y, s=0.5)
        
            ax.axvline(c='grey', lw=1)
            ax.axhline(c='grey', lw=1)
        
            confidence_ellipse(x, y, ax, edgecolor='red')
        
            ax.scatter(mu[0], mu[1], c='red', s=3)
            ax.set_title(title)
        
        plt.show()
    
    elif runtype in ['example2']:
        fig, ax_nstd = plt.subplots(figsize=(6, 6))
        
        dependency_nstd = [[0.8, 0.75],
                           [-0.2, 0.35]]
        mu = 0, 0
        scale = 8, 5
        
        ax_nstd.axvline(c='grey', lw=1)
        ax_nstd.axhline(c='grey', lw=1)
        
        x, y = get_correlated_dataset(500, dependency_nstd, mu, scale)
        ax_nstd.scatter(x, y, s=0.5)
        
        confidence_ellipse(x, y, ax_nstd, n_std=1,
                           label=r'$1\sigma$', edgecolor='firebrick')
        confidence_ellipse(x, y, ax_nstd, n_std=2,
                           label=r'$2\sigma$', edgecolor='fuchsia', linestyle='--')
        confidence_ellipse(x, y, ax_nstd, n_std=3,
                           label=r'$3\sigma$', edgecolor='blue', linestyle=':')
        
        ax_nstd.scatter(mu[0], mu[1], c='red', s=3)
        ax_nstd.set_title('Different standard deviations')
        ax_nstd.legend()
        plt.show()
    
    elif runtype in ['example3']:
        fig, ax_kwargs = plt.subplots(figsize=(6, 6))
        dependency_kwargs = [[-0.8, 0.5],
                             [-0.2, 0.5]]
        mu = 2, -3
        scale = 6, 5
        
        ax_kwargs.axvline(c='grey', lw=1)
        ax_kwargs.axhline(c='grey', lw=1)
        
        x, y = get_correlated_dataset(500, dependency_kwargs, mu, scale)
        # Plot the ellipse with zorder=0 in order to demonstrate
        # its transparency (caused by the use of alpha).
        confidence_ellipse(x, y, ax_kwargs,
                           alpha=0.5, facecolor='pink', edgecolor='purple', zorder=0)
        
        ax_kwargs.scatter(x, y, s=0.5)
        ax_kwargs.scatter(mu[0], mu[1], c='red', s=3)
        ax_kwargs.set_title('Using keyword arguments')
        
        fig.subplots_adjust(hspace=0.25)
        plt.show()