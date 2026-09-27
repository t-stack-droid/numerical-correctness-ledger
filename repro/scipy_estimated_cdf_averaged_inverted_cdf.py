"""scipy.stats.estimated_cdf(method='averaged_inverted_cdf') equals method='inverted_cdf'.

The averaged inverted CDF (Hyndman and Fan definition 2) at a data point is the average
of the left and right limits of the empirical CDF: (#{x < y} + #{x <= y}) / (2 n). For x
= [1, 2, 3, 4] and y = 2 that is (1 + 2) / 8 = 0.375; numpy.quantile with the same
method maps 0.375 back to 2.

Run: python scipy_estimated_cdf_averaged_inverted_cdf.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import scipy.stats as st

got = float(st.estimated_cdf([1.0, 2, 3, 4], 2.0, method="averaged_inverted_cdf"))
verdict(abs(got - 0.375) > 1e-12, f"got {got!r}, expected 0.375")
