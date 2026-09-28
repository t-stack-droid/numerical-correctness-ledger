"""scipy.special.y1p_zeros(complex=True): the first zero returned has positive real part.

The docstring says complex=True returns the complex zeros with negative real part and
positive imaginary part. The first value returned, 0.5768 + 0.9040j, has positive real
part and is a genuine zero of Y1' (the script checks the residual in mpmath), so the
documentation, not the value, looks wrong. The script reads the installed docstring.

Run: python scipy_y1p_zeros_complex_docstring.py
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
import mpmath as mp
import scipy.special as sc

mp.mp.dps = 40
z, _ = sc.y1p_zeros(3, complex=True)
z0 = complex(z[0])
resid = abs(complex(mp.bessely(0, z0) - mp.bessely(1, z0) / z0))
claims = "negative real part" in " ".join(inspect.getdoc(sc.y1p_zeros).split())
verdict(claims and z0.real > 0 and resid < 1e-12,
        f"first complex zero {z0:.6f}, |Y1'| there {resid:.0e}; docstring states negative real part: {claims}")
