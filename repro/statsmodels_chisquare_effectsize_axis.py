"""statsmodels chisquare_effectsize(axis=1) raises for 2-D input (crash, not a wrong value).

The docstring documents `axis` for multi-dimensional input. The normalisation divides by
probs.sum(axis) without keepdims, which cannot broadcast for axis=1. With identical
probability rows the effect size of every row is 0; axis=0 on the transposed input
returns those zeros.

Run: python statsmodels_chisquare_effectsize_axis.py
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
from statsmodels.stats.api import chisquare_effectsize

probs = np.full((3, 4), 0.25)
control = np.asarray(chisquare_effectsize(probs.T, probs.T, axis=0)).tolist()
try:
    es = np.asarray(chisquare_effectsize(probs, probs, axis=1))
    verdict(not np.allclose(es, 0.0), f"axis=1 returned {es.tolist()}; expected three zeros")
except ValueError as e:
    verdict(True, f"axis=1 raised ValueError: {e}; axis=0 on the transposed input gives {control}")
