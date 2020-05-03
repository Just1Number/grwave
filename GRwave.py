#!/usr/bin/env python
"""Simple groundwave example, assuming uniform ground parameters"""
from matplotlib.pyplot import figure, show
import grwave

try:
    import seaborn as sns

    sns.set_context("talk", 1.0)
except ImportError:
    pass


def main():
    wls = {
        "ans" : 315,
        "hscale" : 7.35,
        "ipolrn" : 1,
        "freqMHz": 0.89,
        "sigma": 2e-3,
        "epslon": 4,
        "dmax": 400,
        "dmin": 1,
        "hrr": 3,
        "htt": 100,
        "loglin": 0,
        "dstep": 10,
        "txwatt": 50e3,
    }

    data = grwave.grwave(wls)
    # %%
    d_km = data.index.values.astype(float)

    ax = figure().gca()
    ax.plot(d_km, data["fs"].values)
    # Set to log scale
    ax.set_xscale("log") 
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200, 500])
    ax.set_xlabel("distance [km]")
    ax.set_ylabel("field strength dB(uV/m)")
    ax.axhline(4, color="red", linestyle="--")
    ax.grid(True)
    # ax.set_ylim((0,25))
    show()


if __name__ == "__main__":
    main()
