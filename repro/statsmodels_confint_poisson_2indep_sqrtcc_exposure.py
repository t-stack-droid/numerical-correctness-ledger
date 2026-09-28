"""statsmodels confint_poisson_2indep(method='sqrtcc', compare='ratio') ignores exposures.

The rate ratio is (c1/e1)/(c2/e2). With the counts fixed, multiplying e2 by 4 multiplies
the rate ratio by 4, so an interval for it built from the same counts must scale by 4 as
well. The sqrtcc interval does not change, so it is an interval for c1/c2. Example:
counts 10 and 20, exposures 10 and 40 (rate ratio 2); the interval returned excludes 2.

Run: python statsmodels_confint_poisson_2indep_sqrtcc_exposure.py
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

from statsmodels.stats.rates import confint_poisson_2indep

a = confint_poisson_2indep(10, 10, 20, 10, method="sqrtcc", compare="ratio")
b = confint_poisson_2indep(10, 10, 20, 40, method="sqrtcc", compare="ratio")
ok = abs(b[0] - 4 * a[0]) < 1e-9 * abs(4 * a[0]) and abs(b[1] - 4 * a[1]) < 1e-9 * abs(4 * a[1])
verdict(not ok, f"exposure2=10: {tuple(map(float, a))}; exposure2=40: {tuple(map(float, b))}; "
                "expected the second to be 4 times the first")
