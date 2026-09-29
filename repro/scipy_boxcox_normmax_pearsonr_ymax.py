"""scipy.stats.boxcox_normmax: ymax is documented as ignored for method='pearsonr', but it changes the result (question).

The docstring says of ymax: "Ignored when ``method='pearsonr'``." For x = 1, 2, 3, 5, 8,
13, 21, 34 the pearsonr estimate is 0.0445 without ymax and 0.0 with ymax = 0.25. The
value 0.0 does not meet the bound either: boxcox(34, 0) = log 34 = 3.53. The script
reads the installed docstring and reports not reproduced if the sentence is gone.

Run: python scipy_boxcox_normmax_pearsonr_ymax.py
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

import inspect
import math
import numpy as np
import scipy.stats as st

x = np.array([1.0, 2, 3, 5, 8, 13, 21, 34])
documented = "Ignored when ``method='pearsonr'``." in (inspect.getdoc(st.boxcox_normmax) or "")
free = float(st.boxcox_normmax(x, method="pearsonr"))
if not math.isfinite(free):
    raise RuntimeError("precondition: the estimate without ymax is finite")
capped = float(st.boxcox_normmax(x, method="pearsonr", ymax=0.25))
verdict(documented and not (abs(free - capped) <= 1e-12),
        f"docstring says ymax is ignored for pearsonr: {documented}; lambda without ymax {free!r}, with ymax=0.25 {capped!r}")
