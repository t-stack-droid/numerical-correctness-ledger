"""statsmodels Tweedie(eql=False).loglike_obs: -inf for a tiny positive observation.

For 1 < p < 2 the Tweedie density at y > 0 is a compound Poisson-gamma series with
positive terms, so its log is finite. The library evaluates the series on the linear
scale and takes the log afterwards, which underflows to -inf. Reference: the series
summed in mpmath.

Run: python statsmodels_tweedie_loglike_underflow.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import mpmath as mp
import numpy as np
import statsmodels.api as sm

mp.mp.dps = 50
p, y, mu, phi = 1.1, 1e-100, 1.0, 1.0
P, Y, M, F = (mp.mpf(repr(v)) for v in (p, y, mu, phi))
lam = M ** (2 - P) / (F * (2 - P)); alpha = (2 - P) / (P - 1); theta = F * (P - 1) * M ** (P - 1)
y_ = Y
terms = [mp.e ** (-lam) * lam ** n / mp.factorial(n) * y_ ** (n * alpha - 1) * mp.e ** (-y_ / theta)
         / (mp.gamma(n * alpha) * theta ** (n * alpha)) for n in range(1, 60)]
want = float(mp.log(mp.fsum(terms)))
got = float(sm.families.Tweedie(var_power=p, eql=False).loglike_obs(np.array([y]), np.array([mu]), scale=phi)[0])
verdict(not np.isfinite(got) or abs(got - want) > 1e-6 * abs(want), f"got {got!r}, expected {want!r}")
