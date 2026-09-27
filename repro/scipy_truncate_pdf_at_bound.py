"""scipy.stats.truncate: pdf is 0 (logpdf -inf) at a finite truncation bound.

For a standard normal truncated to [2, 8], the density at x = 2 is phi(2) / (Phi(8) -
Phi(2)) = 2.3732... The truncation bound is inside the support of the truncated
distribution (a point slightly above it gets the correct value).

Run: python scipy_truncate_pdf_at_bound.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import mpmath as mp
import scipy.stats as st

mp.mp.dps = 40
want = mp.npdf(2) / (mp.ncdf(8) - mp.ncdf(2))
got = float(st.truncate(st.Normal(), lb=2, ub=8).pdf(2.0))
verdict(abs(got - float(want)) > 1e-9 * float(want), f"pdf(2) = {got!r}, expected {float(want)!r}")
