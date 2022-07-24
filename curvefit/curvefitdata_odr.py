# manage data and fit
import pandas as pd
import numpy as np

# first part with least squares
from scipy.optimize import curve_fit

# second part about ODR
from scipy.odr import ODR, Model, Data, RealData

def f_model(x, a, c):
    return pd.np.log((a + x)**2 / (x - c)**2)

def fxy_model(beta, x):
    a, c = beta
    return pd.np.log((a + x)**2 / (x - c)**2)

###################################################
df = pd.read_csv("donnees_exo9.csv", sep=";")

####### curvefit without x uncertainties
popt, pcov = curve_fit(
    f=f_model,       # model function
    xdata=df["x"],   # x data
    ydata=df["y"],   # y data
    p0=(3, -2),      # initial value of the parameters
    sigma=df["Dy"]   # uncertainties on y
)
a_opt, c_opt = popt

# now add x uncertainties
nval = len(df)
Dx = [np.random.normal(0.3, 0.2) for i in range(nval)]
df["Dx"] = Dx
df.head()

ax = df.plot(
    x="x", y="y",
    kind="line", yerr="Dy", xerr="Dx",
    title="Some experimetal data",
    linestyle="", marker=".",
    capthick=1, ecolor="gray", linewidth=1
)

data = RealData(df.x, df.y, df.Dx, df.Dy)
model = Model(fxy_model)

# fit_type=2 is a least squares approach and consider only y uncertainties.
# fit_type=0 explicit ODR

odr = ODR(data, model, [3, -2])
odr.set_job(fit_type=2)
lsq_output = odr.run()
print("Iteration 1:")
print("------------")
print("   stop reason:", lsq_output.stopreason)
print("        params:", lsq_output.beta)
print("          info:", lsq_output.info)
print("       sd_beta:", lsq_output.sd_beta)
print("sqrt(diag(cov):", np.sqrt(np.diag(lsq_output.cov_beta)))

# if convergence is not reached, run again the algorithm
if lsq_output.info != 1:
    print("\nRestart ODR till convergence is reached")
    i = 1
    while lsq_output.info != 1 and i < 100:
        print("restart", i)
        lsq_output = odr.restart()
        i += 1
    print("   stop reason:", lsq_output.stopreason)
    print("        params:", lsq_output.beta)
    print("          info:", lsq_output.info)
    print("       sd_beta:", lsq_output.sd_beta)
    print("sqrt(diag(cov):", np.sqrt(np.diag(lsq_output.cov_beta)))

##### Now the explicit ODR approach with fit_type=0.
odr = ODR(data, model, [3, -2])
odr.set_job(fit_type=0)
odr_output = odr.run()
print("Iteration 1:")
print("------------")
print("   stop reason:", odr_output.stopreason)
print("        params:", odr_output.beta)
print("          info:", odr_output.info)
print("       sd_beta:", odr_output.sd_beta)
print("sqrt(diag(cov):", np.sqrt(np.diag(odr_output.cov_beta)))

# if convergence is not reached, run again the algorithm
if odr_output.info != 1:
    print("\nRestart ODR till convergence is reached")
    i = 1
    while odr_output.info != 1 and i < 100:
        print("restart", i)
        odr_output = odr.restart()
        i += 1
    print("   stop reason:", odr_output.stopreason)
    print("        params:", odr_output.beta)
    print("          info:", odr_output.info)
    print("       sd_beta:", odr_output.sd_beta)
    print("sqrt(diag(cov):", np.sqrt(np.diag(odr_output.cov_beta)))

a_lsq, c_lsq = lsq_output.beta
print("        ODR(lsq)    curve_fit")
print("------------------------------")
print("a = %12.7f %12.7f" % (a_lsq, a_opt))
print("c = %12.7f %12.7f" % (c_lsq, c_opt))

# Print the results and compare to least square
a_odr, c_odr = odr_output.beta
print("\n        ODR(lsq)    curve_fit     True ODR")
print("--------------------------------------------")
print("a = %12.7f %12.7f %12.7f" % (a_lsq, a_opt, a_odr))
print("c = %12.7f %12.7f %12.7f" % (c_lsq, c_opt, c_odr))

#### plot results
x = np.linspace(0, 20, 200)
ax = df.plot(
    x="x", y="y",
    kind="line", yerr="Dy", xerr="Dx",
    title="Some experimetal data",
    linestyle="", marker=".",
    capthick=1, ecolor="gray", linewidth=1
)
ax.plot(x, f_model(x, a_lsq, c_lsq), linewidth=1, label="least square")
ax.plot(x, f_model(x, a_odr, c_odr), linewidth=1, label="ODR")
ax.legend(fontsize=14, frameon=True)

fig = ax.get_figure()
fig.savefig('experimentdata_bestfits2.png')
