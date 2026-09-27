"""scipy.stats.spearmanr with nan_policy='omit': p-value 1.0 for perfectly monotone data.

After the pair containing NaN is removed, x = y = [1, 2, 3, 4], so rho = 1 exactly, t =
rho * sqrt((n - 2) / (1 - rho**2)) is infinite and the two-sided p-value is 0. The
library computes rho slightly above 1, the variance ratio becomes negative and is
clipped to 0, so t = 0 and p = 1.

Run: python scipy_spearmanr_omit_pvalue.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
import scipy.stats as st

r = st.spearmanr([1.0, 2, 3, 4, 5], [1.0, 2, 3, 4, np.nan], nan_policy="omit")
verdict(not (r.pvalue < 1e-12),
        f"statistic={float(r.statistic)!r} pvalue={float(r.pvalue)!r}; expected statistic 1 and pvalue 0")
