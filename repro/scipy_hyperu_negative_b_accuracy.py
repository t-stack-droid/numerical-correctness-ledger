"""scipy.special.hyperu loses accuracy for negative b at the tested points.

Reference values from mpmath.hyperu at 40 digits, at b = -4.7012 and x = 6.9068. The
relative error is 7.1e-8 for a = 1.4836 and 3.0e-10 for a = 2.4836; the control a =
3.4836 is accurate to about 1e-13. Other parameters were not mapped. This is separate
from the NaN returned for a = -1.5, b = 0 (scipy_hyperu_negative_a.py).

Run: python scipy_hyperu_negative_b_accuracy.py
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
import scipy.special as sc

mp.mp.dps = 40
rows, bad = [], False
for a in (1.4836, 2.4836, 3.4836):
    got = float(sc.hyperu(a, -4.7012, 6.9068))
    want = float(mp.hyperu(a, -4.7012, 6.9068))
    err = abs(got - want) / abs(want)
    bad = bad or not err <= 1e-12
    rows.append(f"a={a}: scipy {got!r}, mpmath {want!r}, rel. error {err:.1e}")
verdict(bad, "b = -4.7012, x = 6.9068; " + "; ".join(rows))
