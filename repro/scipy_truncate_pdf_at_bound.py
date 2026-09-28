"""scipy.stats.truncate: a truncated Normal has density 0 at its finite bounds, unlike scipy's other conventions (question).

The density at a single point is a convention, so this is not a wrong value in the
measure sense, but scipy's conventions disagree. support() of truncate(Normal(), lb=2,
ub=8) is the closed interval (2, 8); truncate(Uniform(0, 10), 2, 8) has density 1/6 at
its bounds; and scipy.stats.truncnorm(2, 8), which the truncate docstring uses for
comparison, gives phi(2) / (Phi(8) - Phi(2)) = 2.3732 at x = 2. The truncated Normal
returns pdf 0 and logpdf -inf there, which matters when an observation lies exactly on a
truncation point, for example in a log-likelihood.

Run: python scipy_truncate_pdf_at_bound.py
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
want = float(mp.npdf(2) / (mp.ncdf(8) - mp.ncdf(2)))
X = st.truncate(st.Normal(), lb=2, ub=8)
pdf, logpdf = float(X.pdf(2.0)), float(X.logpdf(2.0))
legacy = float(st.truncnorm(2, 8).pdf(2.0))
unif = float(st.truncate(st.Uniform(a=0.0, b=10.0), lb=2, ub=8).pdf(2.0))
lo, hi = (float(v) for v in X.support())
verdict(not (abs(pdf - want) <= 1e-9 * want) or not math.isfinite(logpdf),
        f"truncated Normal at its bound: pdf {pdf!r}, logpdf {logpdf!r}; support ({lo}, {hi}); "
        f"truncnorm pdf {legacy!r}; truncated Uniform pdf at its bound {unif!r}")
