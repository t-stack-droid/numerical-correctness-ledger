"""scipy.special.nctdtridf fails to invert nctdtr and returns its 1e100 sentinel.

nctdtridf(p, nc, t) is documented as the inverse of nctdtr in the degrees of freedom.
For nc = -2.6419 and t = -0.6117, p = 0.97859 is the CDF at df = 7.4207 (the CDF is not
monotone in df here, and p is also attained near df = 0.0304). The library returns
1e100, where the CDF is 0.97883, a residual of 2.5e-4, so it is not a solution. The
script accepts any finite positive df whose CDF, evaluated independently in mpmath
(integral over the chi-square mixing density), matches p to 1e-9. The development branch
returns NaN here.

Run: python scipy_nctdtridf_roundtrip.py
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


df, nc, t = 7.42072530317493, -2.64193262034259, -0.6117344680174117
p = float(nct_cdf(df, nc, t))
back = float(sc.nctdtridf(p, nc, t))
resid = abs(float(nct_cdf(back, nc, t)) - p) if math.isfinite(back) and back > 0 else float("inf")
verdict(not (resid <= 1e-9), f"p = {p!r}; nctdtridf(p, nc, t) = {back!r}, CDF residual {resid:.1e} "
                             f"(df = {df} has residual 0)")
