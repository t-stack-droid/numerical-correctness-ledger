"""scipy.stats.dlaplace.sf is 0 in the far tail.

For k >= 0, sf(k) = exp(-a(k+1)) / (1 + exp(-a)) (geometric tail of tanh(a/2)
exp(-a|j|)), which is 1.29e-24 at k = 10, a = 5. The library returns 0, consistent with
computing 1 - cdf. At moderate k the values agree to 1e-14.

Run: python scipy_dlaplace_sf_far_tail.py
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
want = float(mp.e ** (-55) / (1 + mp.e ** (-5)))
got = float(st.dlaplace.sf(10, 5.0))
verdict(not (abs(got - want) <= 1e-6 * want), f"sf(10, a=5) = {got!r}, expected {want!r}")
