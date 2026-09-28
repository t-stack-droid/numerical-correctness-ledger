"""scipy.stats.dlaplace: logpmf is -inf for large |k|, and sf is 0 in the far tail.

The pmf is tanh(a/2) exp(-a|k|), so logpmf(k) = log(tanh(a/2)) - a|k| is finite for
every integer k (-1000.77 at k = -1000, a = 1). For k >= 0, sf(k) = exp(-a(k+1)) / (1 +
exp(-a)), which is 1.29e-24 at k = 10, a = 5; the library returns 0 because it computes
1 - cdf.

Run: python scipy_dlaplace_log_and_tail.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import math
import mpmath as mp
import scipy.stats as st

mp.mp.dps = 40
lp_want = float(mp.log(mp.tanh(mp.mpf(1) / 2)) - 1000)
sf_want = float(mp.e ** (-55) / (1 + mp.e ** (-5)))
lp = float(st.dlaplace.logpmf(-1000, 1.0))
sf = float(st.dlaplace.sf(10, 5.0))
bad = not math.isfinite(lp) or abs(lp - lp_want) > 1e-9 * abs(lp_want) or abs(sf - sf_want) > 1e-6 * sf_want
verdict(bad, f"logpmf(-1000, 1) = {lp!r} (expected {lp_want!r}); sf(10, 5) = {sf!r} (expected {sf_want!r})")
