"""scipy.stats.poisson_means_test: p-value below 1 when the two observed rates are equal.

When the observed statistic is 0, every outcome is at least as extreme, so the p-value
is 1. The outcome (0, 0) has variance 0, the statistic becomes 0/0 = NaN, the comparison
with NaN is false, and that outcome's probability is dropped (here exp(-2) = 0.1353).

Run: python scipy_poisson_means_test_equal_rates.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import scipy.stats as st

got = float(st.poisson_means_test(1, 1.0, 1, 1.0).pvalue)
verdict(abs(got - 1.0) > 1e-12, f"pvalue = {got!r}, expected 1.0")
