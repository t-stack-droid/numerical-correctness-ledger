"""scipy.stats.barnard_exact: swapping the rows changes the two-sided p-value.

Swapping the rows of the table negates every Wald statistic and maps pi to 1 - pi, so
the two-sided p-value cannot change. For [[14, 9], [5, 19]] with pooled=False the
library returns 0.0055692 and, for the swapped table, 0.0051505; by symmetry they must
be equal. scipy_barnard_exact_ties.py shows how exact ties are lost to float rounding in
this function. This script shows only the asymmetry.

Run: python scipy_barnard_exact_row_swap.py
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

import scipy.stats as st

p1 = float(st.barnard_exact([[14, 9], [5, 19]], pooled=False).pvalue)
p2 = float(st.barnard_exact([[5, 19], [14, 9]], pooled=False).pvalue)
verdict(not (abs(p1 - p2) <= 1e-9), f"two-sided, pooled=False: {p1:.7f} vs {p2:.7f} after swapping rows")
