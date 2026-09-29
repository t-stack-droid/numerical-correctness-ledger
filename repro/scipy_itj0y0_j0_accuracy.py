"""scipy.special.itj0y0: the integral of J0 loses accuracy for x between 12 and 37.

itj0y0(x) returns the integrals of J0 and Y0 from 0 to x. The reference uses the closed
form: the integral of J0 from 0 to x equals x J0(x) + (pi x / 2)(J1(x) H0(x) - J0(x)
H1(x)), with H0 and H1 the Struve functions, in mpmath at 40 digits and cross-checked by
quadrature at x = 20. Sampled at x = 12, 12.25, ..., 37 (101 points): the absolute error
exceeds 1e-12 at 55 points and reaches 1.1e-9 at x = 19.75, where the value is 1.015.

Run: python scipy_itj0y0_j0_accuracy.py
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


def int_j0(x):
    x = mp.mpf(x)
    return x * mp.besselj(0, x) + mp.pi * x / 2 * (
        mp.besselj(1, x) * mp.struveh(0, x) - mp.besselj(0, x) * mp.struveh(1, x))


q = mp.quad(lambda t: mp.besselj(0, t), mp.linspace(0, 20, 21))
if not abs(q - int_j0(20)) < mp.mpf(10) ** -25:
    raise RuntimeError("precondition: closed form agrees with quadrature at x = 20")
rows = []
for x in [12 + 0.25 * k for k in range(101)]:
    got, want = float(sc.itj0y0(x)[0]), float(int_j0(x))
    rows.append((abs(got - want), x, want))
bad = [r for r in rows if not r[0] <= 1e-12]
e, x, v = max(bad, key=lambda r: r[0] if r[0] == r[0] else float("inf")) if bad else (0.0, None, 1.0)
verdict(bool(bad), f"absolute error above 1e-12 (or NaN) at {len(bad)} of {len(rows)} sampled points in [12, 37]; "
                   f"largest {e:.1e} at x = {x} (value {v:.4f}, relative error {e / abs(v):.1e})")
