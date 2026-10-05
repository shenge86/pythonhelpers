# pythonhelpers

## What is this?
These are helpful (hopefully) Python scripts for general usage -- logging, examining and manipulating data. Much of it is attuned for data manipulation with the pandas library (start with `reduceexcel.py`), but the repo has grown to also hold math and physics experiments, machine learning practice, web/media helpers, an image and video collection, and writing.

Most scripts are standalone: run them with `python <script>.py`. Some take command line arguments, some prompt for input, and some have file names hardcoded near the top that you are expected to edit.

## Contents
- [Python scripts](#python-scripts)
  - [CSV, Excel and text manipulation](#csv-excel-and-text-manipulation)
  - [GIS and surface calculations](#gis-and-surface-calculations)
  - [Statistics, curve fitting and covariance](#statistics-curve-fitting-and-covariance)
  - [Math and physics](#math-and-physics)
  - [Optimization and stochastic processes](#optimization-and-stochastic-processes)
  - [Machine learning](#machine-learning)
  - [Web, images and video](#web-images-and-video)
  - [Python language demos and misc](#python-language-demos-and-misc)
- [Shell scripts](#shell-scripts)
- [Folders](#folders)
- [Other files](#other-files)
- [Dependencies](#dependencies)

## Python scripts

### CSV, Excel and text manipulation
| Script | What it does |
| --- | --- |
| `reduceexcel.py` | Command line csv / excel reducer. Reads csv, parquet, msgpack, hdf5 or feather files, keeps chosen columns, and drops rows outside min/max thresholds. Also has importable helpers (`readdata`, `savedata`, `filtercols`, `splitter`, `combinecsv`). Usage: `reduceexcel.py -i <inputfile> -o <outputfile> -n <numberofrows> -m <columnstotake> --mmax <maxcolvalues> --mmin <mincolvalues>` |
| `parsesheet.py` | General Excel parser. Opens a tkinter file picker for a csv/xlsx/xlsm file, asks which sheet to use, then slices out a column range and drops chosen rows. |
| `comparefiles.py` | Compares two csv files column by column, writes the differences and summary statistics to csv. Also computes the distance between lat/lon pairs in the two files using `gis.py`. Usage: `comparefiles.py <file1> <file2> <outfile>` |
| `removempty.py` | Removes rows with any empty cells from a csv file. Usage: `python removempty.py <input.csv> <output.csv>` |
| `split.py` | Interactive. Splits a csv file into one csv per unique value of a column you choose (falls back to sample NOAA data if the file is not found). |
| `splitcsv.py` | Splits a crater csv into separate files by 3 degree longitude bins, after wrapping negative longitudes to 0-360. File names are hardcoded. |
| `limit_parser.py` | Start of a script to filter a csv by limits on certain columns. Currently only loads `input.csv`. |
| `interpolater.py` | Linearly interpolates two columns of a csv against the first column over a fixed range and step (azimuth / elevation data), then saves `<source>_interpolated.csv`. |
| `extract_data.py` | Extracts values from a text file based on identifier words and a delimiter and writes them to csv. Includes a seconds to `hh:mm:ss` converter. |
| `datetimereplacer.py` | Finds dates in a text file with regex and rewrites them in another date format chosen from a menu. Only some of the formats are implemented. |
| `removewords.py` | Deletes a list of words / characters from every line of a text file. |
| `removespacesreplacewithcommas.py` | Rewrites each line of `input.txt` so that the first four fields stay space separated and the rest become comma separated. |
| `wordfrequency.py` | Counts word frequency in `test.txt` using a dict. Heavily commented as a learn-as-we-go example. |
| `wordfrequency_r.py` | Same idea using `collections.Counter`. Usage: `python wordfrequency_r.py <textfile> [topN]` |
| `union_parser.py` | Finds the overlap and union of numeric intervals, including merging an array of start/end times into combined intervals. |

### GIS and surface calculations
The default body radius is 1737400 m (the Moon, as used by LOLA / Kaguya data). Pass a different `R` for other bodies.

| Script | What it does |
| --- | --- |
| `gis.py` | Importable suite of surface functions: `calcDist` (distance between two lat/lons), `calcAzimuth` (bearing), `calcCoord` (destination from a start point, azimuth and distance) and `calcElvangle` (elevation angle accounting for curvature). |
| `bearingvecdistance.py` | Minimal command line calculator of distance and bearing between two points given 4 arguments. |
| `distanceazimuthcalc.py` | Distance and azimuth calculator with interactive prompts for coordinates and radius, and csv input/output. |
| `openqm.py` | Reads a csv with `lat` and `lon` columns and opens the points in LROC QuickMap in your browser. Usage: `openqm.py <file.csv> [numrows]` |

### Statistics, curve fitting and covariance
| Script | What it does |
| --- | --- |
| `covariance.py` | Covariance plotter. Draws confidence (error) ellipses for 2D data and prints the correlation matrix and ellipse parameters. Reads a csv from `covariance/` or generates correlated random data. Flags: `-verbose`, `-testing`, `-saveinput`. Plots are saved to `covariance/`. |
| `covariance_transform.py` | Uses sympy to symbolically transform a 2D covariance matrix from Cartesian to polar via the Jacobian, printing the result as plain text, LaTeX and pretty print. |
| `curvefit.py` | Curve fitting example on Longley's economic regression data (`longley.csv`). Fits linear, quadratic and sine-combo models of population vs employed with `scipy.optimize.curve_fit` and saves the `populationvsemployed_*.png` plots. |
| `binomial.py` | Draws 50 binomial samples and plots their 95% confidence intervals, colored by whether they contain the true mean. Saves `myplot.png`. |

### Math and physics
| Script | What it does |
| --- | --- |
| `algebraequation_solvers.py` | sympy examples: solving an absolute value inequality and finding the inverse of a function. |
| `geometryconvert.py` | Generators that yield the surface areas of spheres and cubes of increasing size. |
| `math/hyperbolic_functions.py` | Plots sinh, cosh and tanh, and compares tanh against its Taylor series approximations (built from Bernoulli numbers) with 1 to 7 terms. |
| `blackholes/eventhorizon.py` | Calculates the Schwarzschild radius for a mass given in solar masses, and the tidal acceleration across an object at a given distance. |
| `ascent/ascent.py` | Solves the optimal ascent trajectory from a flat Moon to a 100 nautical mile circular orbit with `scipy.integrate.solve_bvp`, and plots position, velocity and steering angle. |

### Optimization and stochastic processes
| Script | What it does |
| --- | --- |
| `geneticalgorithm_test.py` | Genetic algorithm tester that searches for the maximum of `sin(pi*x/256)` using 8-bit binary strings and roulette wheel selection. Use `-default` to load a fixed starting population. |
| `pso_test.py` | Particle swarm optimization on a non-convex 2D function. Animates the swarm and saves it as `PSO.gif`. |
| `randomwalk.py` | Simulates a 1D random walk and plots the path over time and a histogram of visited values. |
| `montecarlomarkovchain.py` | Description of the island-hopping politician problem (Metropolis algorithm). Notes only so far, no code yet. |

### Machine learning
| Script | What it does |
| --- | --- |
| `mlwpy.py` | Shared setup module used by the `ml_*.py` scripts via `from mlwpy import *`. Imports numpy, pandas, matplotlib, seaborn and sklearn, sets display options, and defines plotting and helper functions (`plot_boundary`, `plot_separator`, `DLDA`, ...). |
| `ml_iris.py` | k-nearest neighbors classification on the iris dataset: train/test split, fit, predict, accuracy and a confusion matrix heatmap. |
| `ml_tree.py` | Decision tree classifier on iris with a plot of the decision boundary. |
| `ml_testlearners.py` | Fits a linear regression to noisy quadratic data to compare learners. |
| `ml_logisticreg.py` | Builds a table of probability, odds and log-odds as logistic regression practice. |
| `ml_grades.py` | Computes accuracy by hand and with `sklearn.metrics.accuracy_score`. |
| `ml_gradientdescent.py` | Gradient descent for single variable linear regression written from scratch, with plots of cost vs iteration. |

### Web, images and video
| Script | What it does |
| --- | --- |
| `scrap_page.py` | Fetches a web page (or reads a local html file) with BeautifulSoup and saves its text to `html_text.txt`. Usage: `scrap_page.py <url>` |
| `download_video.py` | Downloads an mp4 from a url using requests, falling back to urllib. Usage: `python download_video.py <url>` |
| `playvideo.py` | OpenCV video player that pauses on the last frame. SPACE = pause/play, R = restart, Q = quit. Defaults to `data_vid/rosetta.mp4`. |
| `identifyreceipt.py` | Sends a receipt image to Claude's vision API and extracts the total amount. Needs `pip install anthropic` and the `ANTHROPIC_API_KEY` environment variable. |
| `poetry.py` | Generates random poetry with the wonderwords library and opens a random image from `data_img` to go with it. Use `-load` to reload the words saved in `words.pkl`. |
| `data_img/generate_readme.py` | Regenerates `data_img/README.md`, a gallery of every image in `data_img` grouped by subfolder. Run it after adding or removing images. |

### Python language demos and misc
| Script | What it does |
| --- | --- |
| `decorate.py` | Examples of function and class decorators (uppercase, logging the run time, counting instances). |
| `watch.py` | Process checking functions to import into other scripts: follow a log file like `tail -f`, and report memory usage of the process or of a pandas dataframe. |
| `randomrunscript.py` | Empty placeholder. |

## Shell scripts
| Script | What it does |
| --- | --- |
| `download_images.sh` | Downloads images from Pinterest boards and most image websites. Usage: `./download_images.sh <URL> [output_dir]` |
| `download_linked_images.sh` | Downloads full resolution images from gallery / thumbnail pages by following each thumbnail link. Options for output directory, delay, format and minimum size; run with `-h` for help. |

Both require only curl and python3.

## Folders
| Folder | What it holds |
| --- | --- |
| `ascent/` | The optimal lunar ascent script and its output figure. |
| `blackholes/` | Black hole calculations (event horizon radius and tidal force). |
| `covariance/` | Output plots from `covariance.py` (positive, negative, weak and random correlation cases). Also where that script looks for input csv files. |
| `curvefit/` | More curve fitting experiments and their output plots: `curvefitexample.py` (fits a sum of two Gaussians with `scipy.optimize.minimize` and times it), `curvefitdata.py` (weighted least squares fit of experimental data with y uncertainties), `curvefitdata_odr.py` (same fit with x and y uncertainties using orthogonal distance regression) and `covarianceplot.py` (an earlier version of the covariance ellipse plotter). |
| `math/` | Math function plots (hyperbolic functions and tanh approximations). |
| `notebooks/` | Jupyter notebooks working through deep learning fundamentals, numbered by chapter: supervised learning, shallow and deep networks, loss functions, gradient descent variants (SGD, momentum, Adam), backpropagation and initialization. |
| `data/` | Sample datasets (World Bank GDP data and World Marriage Data 2019). |
| `data_img/` | Image collection organized into subfolders, mostly named `<Name>_<role>` (poet, writer, model, scientist, ...) or by topic (Art, architecture, travel, poetry, ...). See `data_img/README.md` for the full gallery. |
| `data_vid/` | Sample videos, plus `tips.md` with notes on using ffmpeg to cut, combine and crop videos. |
| `writings/` | Writing. `apoapsis/` holds the book *apoapsis: space and silence* as markdown chapters with a pandoc build (`cd writings/apoapsis && pandoc --defaults=build.yaml`), and `apoapsis.md` is the combined text. |

## Other files
| File | What it is |
| --- | --- |
| `longley.csv` | Longley's economic regression data used by `curvefit.py`. |
| `test.txt` | Sample text for the word frequency scripts. |
| `words.pkl` | Saved words from the last `poetry.py` run. |
| `PSO.gif` | Animation produced by `pso_test.py`. |
| `myplot.png` | Plot produced by `binomial.py`. |
| `populationvsemployed_*.png`, `rawdata_populationvsemployed.png` | Plots produced by `curvefit.py`. |

## Dependencies
There is no requirements file. Install what the script you are running needs:

- Core: `numpy`, `pandas`, `matplotlib`, `scipy`
- Symbolic math: `sympy`
- Machine learning: `scikit-learn`, `seaborn`, `patsy`, `ipython`
- Web and media: `requests`, `beautifulsoup4`, `opencv-python`, `pillow`
- Other: `anthropic`, `wonderwords`, `tabulate`, `psutil`, `pytictoc`
- Book build: `pandoc` with XeLaTeX (see the comments in `writings/apoapsis/build.yaml`)
