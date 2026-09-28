"""scipy.special.nctdtridf fails to invert nctdtr for degrees of freedom below 2.

For each df in (0.3, 0.7, 1.2, 1.8), nc in (-2, -0.5, 0.5, 2) and t in (-1.5, -0.3, 0.4,
1.7), p is the CDF at the known df (evaluated in mpmath as an integral over the chi-
square mixing density) and is inverted with nctdtridf(p, nc, t), and again through the
symmetry P(T <= t; nc) = 1 - P(T <= -t; -nc). An inversion fails when the output is not
a finite positive number below 1e99 (the library's sentinels are 1e100 and -1e100) or
its CDF misses p by more than 1e-6. On release 1.18.1, 12 of 128 inversions return a
sentinel; the others match p to 3e-9 or better.

Run: python scipy_nctdtridf_small_df.py
Exit status: 1 = the discrepancy was detected in the installed version; 0 = not reproduced by
this comparison; 2 = the script could not run or a precondition failed.
"""
import os
import sys
import traceback


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)


def _could_not_run(exc_type, exc, tb):
    traceback.print_exception(exc_type, exc, tb)
    print(f"could not run: {exc_type.__name__}: {exc}")
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(2)


sys.excepthook = _could_not_run

import itertools
import math
import mpmath as mp
import scipy.special as sc

mp.mp.dps = 30


def nct_cdf(df, nc, t):
    df, nc, t = mp.mpf(df), mp.mpf(nc), mp.mpf(t)
    if df > 1e8:
        return mp.ncdf(t - nc)
    # P(T <= t) = E[Phi(t sqrt(V / df) - nc)], V chi-square(df); substituting V = u**(2 / df)
    # removes the singularity of the chi-square density at 0 for df < 2
    c = 2 / (df * 2 ** (df / 2) * mp.gamma(df / 2))
    g = lambda u: mp.ncdf(t * mp.sqrt(u ** (2 / df) / df) - nc) * mp.exp(-u ** (2 / df) / 2)
    return c * mp.quad(g, [0, 1, 10, 100, mp.inf])


fails, total = [], 0
for df, nc, t in itertools.product((0.3, 0.7, 1.2, 1.8), (-2.0, -0.5, 0.5, 2.0), (-1.5, -0.3, 0.4, 1.7)):
    p = float(nct_cdf(df, nc, t))
    if not 1e-6 < p < 1 - 1e-6:
        continue
    for pp, ncc, tt in ((p, nc, t), (1 - p, -nc, -t)):
        total += 1
        back = float(sc.nctdtridf(pp, ncc, tt))
        ok = math.isfinite(back) and 0 < back < 1e99 and abs(float(nct_cdf(back, ncc, tt)) - pp) <= 1e-6
        if not ok:
            fails.append((df, ncc, tt, back))
verdict(bool(fails), f"{len(fails)} of {total} inversions fail; first (df, nc, t, returned): {fails[:3]}")
