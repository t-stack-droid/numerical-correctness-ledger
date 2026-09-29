"""scipy.special.hyperu returns NaN at b = 0 for the sampled negative non-integer a.

The confluent hypergeometric function U(a, b, x) is defined for all real a and b and x >
0 (DLMF 13.2). At b = 0 the library returns NaN for a = -0.5, -1.5, -2.5 and -3.5 at x =
0.1 and 1, and for a = -0.5 and -1.5 also at x = 5; mpmath gives finite values (for
example U(-1.5, 0, 1) = 0.1702...).

Run: python scipy_hyperu_negative_a.py
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
import scipy.special as sc

mp.mp.dps = 40
pts = [(a, x) for a in (-0.5, -1.5, -2.5, -3.5) for x in (0.1, 1.0)] + [(-0.5, 5.0), (-1.5, 5.0)]
rows = [(a, x, float(sc.hyperu(a, 0.0, x)), float(mp.hyperu(a, 0, x))) for a, x in pts]
if not all(math.isfinite(r[3]) for r in rows):
    raise RuntimeError("precondition: the mpmath reference is not finite")
bad = [r for r in rows if not (math.isfinite(r[2]) and abs(r[2] - r[3]) <= 1e-8 * abs(r[3]))]
verdict(bool(bad), f"{len(bad)} of {len(rows)} points wrong; (a, x, scipy, mpmath) at b = 0: {rows}")
