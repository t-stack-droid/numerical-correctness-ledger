"""statsmodels transform_corr_normal(method='spearman') raises for correlations of mixed sign.

The integration grid is built from sorted correlations with 0 prepended, which is not
monotone when negative values are present. Crash, not a wrong value.

Run: python statsmodels_transform_corr_normal_spearman.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from statsmodels.stats.api import transform_corr_normal

try:
    transform_corr_normal(np.array([-0.5, 0.5]), method="spearman", return_var=True)
    verdict(False, "returned a result")
except Exception as e:
    verdict(True, f"raised {type(e).__name__}: {e}")
