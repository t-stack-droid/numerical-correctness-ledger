"""scipy.stats.barnard_exact: a table that ties the observed statistic is left out, so the p-value is too small.

The p-value is the maximum over the nuisance parameter pi of the probability of all
tables whose Wald statistic is at least as extreme as the observed one; the docstring
defines the region with non-strict inequalities. In the docstring example [[7, 12], [8,
3]] (alternative='less'), the table [[3, 8], [12, 7]] has exactly the same statistic,
T^2 = 750/209. The script compares squared statistics as exact fractions, builds the
probability polynomial of the region with the tie included, and evaluates it at a
numerically located maximizer pi*: that value is a lower bound for the correct p-value
and exceeds the library's. It also shows the mechanism: the library's value equals the
maximum with the tied table left out, and the pooled Wald formula evaluated in float64
(as in scipy's source) ranks the tied table above the observed one.

Run: python scipy_barnard_exact_ties.py
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

from fractions import Fraction as Fr
from math import comb

import mpmath as mp
import numpy as np
import scipy.stats as st

mp.mp.dps = 30


def key(x1, x2, c1, c2):
    # signed squared pooled Wald statistic as an exact fraction, ordered like the statistic
    d = Fr(x1, c1) - Fr(x2, c2)
    if d == 0:
        return (0, Fr(0))
    p = Fr(x1 + x2, c1 + c2)
    q = d * d / (p * (1 - p) * (Fr(1, c1) + Fr(1, c2)))
    return (1, q) if d > 0 else (-1, -q)


def maximize(P):
    grid = [mp.mpf(i) / 1000 for i in range(1001)]
    i = max(range(1001), key=lambda i: P(grid[i]))
    lo, hi = grid[max(i - 1, 0)], grid[min(i + 1, 1000)]
    g = (mp.sqrt(5) - 1) / 2
    for _ in range(100):
        m1, m2 = hi - g * (hi - lo), lo + g * (hi - lo)
        lo, hi = (m1, hi) if P(m1) < P(m2) else (lo, m2)
    return (lo + hi) / 2


(a, b), (c, d) = table = [[7, 12], [8, 3]]
c1, c2 = a + c, b + d
obs = key(a, b, c1, c2)
region = [(x1, x2) for x1 in range(c1 + 1) for x2 in range(c2 + 1) if key(x1, x2, c1, c2) <= obs]
tie = (3, 8)
assert tie in region and key(*tie, c1, c2) == obs


def poly(cells):
    A = [0] * (c1 + c2 + 1)
    for x1, x2 in cells:
        A[x1 + x2] += comb(c1, x1) * comb(c2, x2)
    return lambda q: mp.fsum(A[k] * q ** k * (1 - q) ** (c1 + c2 - k) for k in range(len(A)) if A[k])


P_in, P_out = poly(region), poly([r for r in region if r != tie])
q = maximize(P_in)
bound = float(P_in(q))
without_tie = float(P_out(maximize(P_out)))
got = float(st.barnard_exact(table, alternative="less").pvalue)
T = lambda x1, x2: (x1 / c1 - x2 / c2) / np.sqrt(((x1 + x2) / (c1 + c2)) * (1 - (x1 + x2) / (c1 + c2)) * (1 / c1 + 1 / c2))
verdict(not (got >= bound * (1 - 1e-9)),
        f"got {got:.9f}; tail probability with the tie at pi = {float(q):.4f}: {bound:.9f} (lower bound); "
        f"maximum without the tied table: {without_tie:.9f}; float64 statistics: observed {T(a, b)!r}, tie {T(*tie)!r}")
