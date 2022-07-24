# manage data and fit
import pandas as pd
import numpy as np

# first part with least squares
from scipy.optimize import curve_fit

# style and notebook integration of the plots
import seaborn as sns
# %matplotlib inline
sns.set(style="whitegrid")

#%% START with data
df = pd.read_csv("donnees_exo9.csv", sep=";")
df.head(8) # first 8 lines

ax = df.plot(
    x="x", y="y",
    kind="line", yerr="Dy", title="Some experimental data",
    linestyle="", marker=".",
    capthick=1, ecolor="gray", linewidth=1
)


#%% Now time for some modeling!
def f_model(x, a, c):
    return pd.np.log((a + x)**2 / (x - c)**2)

df["model"] = f_model(df["x"], 3, -2)
df.head(8)

ax = df.plot(
    x="x", y="model",
    kind="line", ax=ax, linewidth=1
)

fig = ax.get_figure()
fig.savefig('experimentdata.png')


#%% CURVE FIT TIME
popt, pcov = curve_fit(
    f=f_model,       # model function
    xdata=df["x"],   # x data
    ydata=df["y"],   # y data
    p0=(3, -2),      # initial value of the parameters
    sigma=df["Dy"]   # uncertainties on y
)

a_opt, c_opt = popt
print("a = ", a_opt)
print("c = ", c_opt)

perr = np.sqrt(np.diag(pcov))
Da, Dc = perr
print("a = %6.2f +/- %4.2f" % (a_opt, Da))
print("c = %6.2f +/- %4.2f" % (c_opt, Dc))
R2 = np.sum((f_model(df.x, a_opt, c_opt) - df.y.mean())**2) / np.sum((df.y - df.y.mean())**2)
print("r^2 = %10.6f" % R2)

# create new model
df["model"] = f_model(df.x, a_opt, c_opt)

ax2 = df.plot(
    x="x", y="y",
    kind="line", yerr="Dy", title="Some experimetal data",
    linestyle="", marker=".",
    capthick=1, ecolor="gray", linewidth=1
)
ax2 = df.plot(
    x="x", y="model (after optimization)",
    kind="line", ax=ax, linewidth=1
)

fig2 = ax2.get_figure()
fig2.savefig('experimentdata_bestfit.png')
