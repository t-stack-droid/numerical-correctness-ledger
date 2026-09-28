"""scipy.stats.dlaplace.logpmf is -inf for large |k|.

The pmf is tanh(a/2) exp(-a|k|), so logpmf(k) = log(tanh(a/2)) - a|k| is finite for
every integer k: -1000.772 at k = -1000, a = 1. The library returns -inf.

Run: python scipy_dlaplace_logpmf_large_k.py
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

import mpmath as mp
import scipy.stats as st

mp.mp.dps = 40
want = float(mp.log(mp.tanh(mp.mpf(1) / 2)) - 1000)
got = float(st.dlaplace.logpmf(-1000, 1.0))
verdict(not (abs(got - want) <= 1e-9 * abs(want)), f"logpmf(-1000, a=1) = {got!r}, expected {want!r}")
