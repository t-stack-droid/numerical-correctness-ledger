"""statsmodels runstest_2samp raises for integer arrays with ties (crash, not a wrong value).

Tie handling adds a float offset to an integer array in place.

Run: python statsmodels_runstest_2samp_integer_ties.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from statsmodels.stats.api import runstest_2samp

try:
    runstest_2samp(np.array([1, 2, 2]), np.array([2, 3, 3]), correction=False)
    verdict(False, "returned a result")
except Exception as e:
    verdict(True, f"raised {type(e).__name__}: {e}")
