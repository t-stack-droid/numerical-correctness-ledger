"""scipy.stats.truncate: icdf returns inf (or loses accuracy) in the far tail.

For a standard normal truncated to [10, inf), the median x solves Phi_c(x) = 0.5
Phi_c(10), where Phi_c is the upper tail probability; x = 10.0684... The library forms
F(a) + p * mass on the linear scale, which cancels once the mass is below about 1e-15.

Run: python scipy_truncate_icdf_far_tail.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import mpmath as mp
import scipy.stats as st

mp.mp.dps = 50
tail = lambda z: mp.erfc(z / mp.sqrt(2)) / 2
want = mp.findroot(lambda x: mp.log(tail(x)) - mp.log(tail(10) / 2), 10.07)
got = float(st.truncate(st.Normal(), lb=10, ub=float("inf")).icdf(0.5))
verdict(not abs(got - float(want)) < 1e-9 * float(want),
        f"icdf(0.5) = {got!r}, expected {float(want)!r}")
