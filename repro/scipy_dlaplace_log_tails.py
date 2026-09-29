"""scipy.stats.dlaplace: logcdf and logsf return -inf in the far tails.

dlaplace has pmf tanh(a/2) exp(-a |k|), so P(K <= -k) = P(K >= k) = tanh(a/2) exp(-a k)
/ (1 - exp(-a)) for k >= 1 and the logarithms are exact linear functions of k. For a = 1
the library returns -inf for logcdf(-1000) and logsf(1000), where the values are
-1000.3133 and -1001.3133 (mpmath, 40 digits).

Run: python scipy_dlaplace_log_tails.py
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

import math
import mpmath as mp
import scipy.stats as st

mp.mp.dps = 40
a = mp.mpf(1)
tail = lambda k: mp.tanh(a / 2) * mp.exp(-a * k) / (1 - mp.exp(-a))
want = (float(mp.log(tail(1000))), float(mp.log(tail(1001))))
got = (float(st.dlaplace.logcdf(-1000, 1.0)), float(st.dlaplace.logsf(1000, 1.0)))
bad = [g for g, w in zip(got, want) if not (math.isfinite(g) and abs(g - w) <= 1e-9 * abs(w))]
verdict(bool(bad), f"logcdf(-1000, a=1) = {got[0]!r} (expected {want[0]:.6f}); logsf(1000, a=1) = {got[1]!r} (expected {want[1]:.6f})")
