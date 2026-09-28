"""scipy.special.hyperu returns NaN for negative non-integer a.

The confluent hypergeometric function U(a, b, x) is defined for all real a and b and x >
0 (DLMF 13.2). For a = -1.5, b = 0 the library returns NaN; mpmath gives finite values
(for example U(-1.5, 0, 1) = 0.1702...).

Run: python scipy_hyperu_negative_a.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import math
import mpmath as mp
import scipy.special as sc

mp.mp.dps = 40
rows = [(x, float(sc.hyperu(-1.5, 0.0, x)), float(mp.hyperu(-1.5, 0, x))) for x in (0.1, 1.0, 5.0)]
bad = [r for r in rows if not (math.isfinite(r[1]) and abs(r[1] - r[2]) <= 1e-8 * abs(r[2]))]
verdict(bool(bad), f"(x, scipy, mpmath) = {rows}")
