"""scipy.stats.kstest(x, 'norm', args=(loc, scale)) raises TypeError.

The string 'norm' is dispatched to scipy.special.ndtr for speed, but the distribution
parameters in args are passed on to ndtr, which accepts no location or scale. The
documented call is equivalent to passing scipy.stats.norm.cdf, which works: for the
sample [2.0] with loc 2 and scale 3 the statistic is 0.5 and the p-value 1. Seen on
releases 1.18.0 and 1.18.1; 1.17.1 and the development branch work.

Run: python scipy_kstest_norm_args.py
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

import scipy.stats as st

ref = st.kstest([2.0], st.norm.cdf, args=(2.0, 3.0))
try:
    r = st.kstest([2.0], "norm", args=(2.0, 3.0))
    ok = abs(float(r.statistic) - 0.5) <= 1e-12 and abs(float(r.pvalue) - 1.0) <= 1e-12
    verdict(not ok, f"statistic {float(r.statistic)!r}, pvalue {float(r.pvalue)!r}; expected 0.5 and 1")
except TypeError as e:
    verdict(True, f"raised TypeError: {e}; the callable form gives statistic {float(ref.statistic)}, p {float(ref.pvalue)}")
