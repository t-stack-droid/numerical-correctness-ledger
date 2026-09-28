"""scipy.special.nctdtridf fails to invert nctdtr and returns its 1e100 sentinel.

nctdtridf(p, nc, t) is documented as the inverse of nctdtr in the degrees of freedom.
For df = 7.4207, nc = -2.6419, t = -0.6117 the probability p = nctdtr(df, nc, t) is
attained at a finite df by construction, yet the inverse returns 1e100.

Run: python scipy_nctdtridf_roundtrip.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import scipy.special as sc

df, nc, t = 7.42072530317493, -2.64193262034259, -0.6117344680174117
p = float(sc.nctdtr(df, nc, t))
back = float(sc.nctdtridf(p, nc, t))
verdict(abs(back - df) > 1e-6 * df, f"p = nctdtr(df, nc, t) = {p!r}; nctdtridf(p, nc, t) = {back!r}, expected {df!r}")
