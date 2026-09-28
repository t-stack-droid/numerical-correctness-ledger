"""statsmodels het_goldfeldquandt(alternative='decreasing'): F degrees of freedom swapped.

Under the null, fval = mse2 / mse1 is F(df2, df1), so for alternative='decreasing' the
p-value must be P(F(df2, df1) < fval). The code uses F(df1, df2), as in the 'increasing'
branch. Reference: statsmodels OLS fits of the two halves and scipy.stats.f.

Run: python statsmodels_het_goldfeldquandt_df_decreasing.py
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

import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_goldfeldquandt

rs = np.random.RandomState(1)
n = 40
X = np.column_stack([np.ones(n), rs.randn(n)])
y = X @ [1.0, 1.0] + rs.randn(n) * np.linspace(1, 3, n)
_, p, _ = het_goldfeldquandt(y, X, split=12, alternative="decreasing")
r1, r2 = sm.OLS(y[:12], X[:12]).fit(), sm.OLS(y[12:], X[12:]).fit()
want = stats.f.cdf(r2.mse_resid / r1.mse_resid, r2.df_resid, r1.df_resid)
verdict(not (abs(p - want) <= 1e-12), f"pvalue={float(p)!r}, expected {float(want)!r} (df1={r1.df_resid:g}, df2={r2.df_resid:g})")
