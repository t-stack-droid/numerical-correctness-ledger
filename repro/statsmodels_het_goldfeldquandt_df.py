"""statsmodels het_goldfeldquandt: F degrees of freedom swapped for one-sided alternatives.

The statistic is fval = mse2 / mse1, which under the null is F(df2, df1). For
alternative='increasing' (the default) the p-value must be P(F(df2, df1) > fval); the
code uses F(df1, df2). The two-sided branch and the recorded df_fval use (df2, df1). The
error is invisible when both halves have the same size.

Run: python statsmodels_het_goldfeldquandt_df.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import het_goldfeldquandt

rs = np.random.RandomState(1)
n = 40
X = np.column_stack([np.ones(n), rs.randn(n)])
y = X @ [1.0, 1.0] + rs.randn(n) * np.linspace(1, 3, n)
f, p, _ = het_goldfeldquandt(y, X, split=12, alternative="increasing")
r1, r2 = sm.OLS(y[:12], X[:12]).fit(), sm.OLS(y[12:], X[12:]).fit()
want = stats.f.sf(r2.mse_resid / r1.mse_resid, r2.df_resid, r1.df_resid)
verdict(abs(p - want) > 1e-12, f"pvalue={float(p)!r}, expected {float(want)!r} (df1={r1.df_resid:g}, df2={r2.df_resid:g})")
