"""statsmodels chisquare_effectsize(axis=1) raises for 2-D input (crash, not a wrong value).

The docstring documents `axis` for multi-dimensional input; the normalisation divides by
probs.sum(axis) without keepdims, which cannot broadcast for axis=1.

Run: python statsmodels_chisquare_effectsize_axis.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from statsmodels.stats.api import chisquare_effectsize

try:
    chisquare_effectsize(np.full((3, 4), 1.0), np.full((3, 4), 2.0), axis=1)
    verdict(False, "axis=1 returned a result")
except Exception as e:
    verdict(True, f"axis=1 raised {type(e).__name__}: {e}")
