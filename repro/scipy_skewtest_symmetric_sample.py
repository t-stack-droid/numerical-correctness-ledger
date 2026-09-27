"""scipy.stats.skewtest: a perfectly symmetric sample gets Z = 1.01, p = 0.31.

For x = 1..8 the sample skewness is exactly 0. The test statistic Z = delta * log(y /
alpha + sqrt((y / alpha)**2 + 1)) is then log(1) = 0, with no singularity, and p = 1; a
sample perturbed by 1e-9 gives Z of about 4e-10. The code replaces y = 0 by 1 before
this formula.

Run: python scipy_skewtest_symmetric_sample.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
import scipy.stats as st

r = st.skewtest(np.arange(1.0, 9.0))
verdict(abs(float(r.statistic)) > 1e-9,
        f"statistic={float(r.statistic)!r} pvalue={float(r.pvalue)!r}; expected 0 and 1")
