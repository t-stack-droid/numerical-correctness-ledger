"""statsmodels nonequivalence_poisson_2indep: statistic from the wrong one-sided test.

The result documents `statistic` as the statistic of the one-sided test with the smaller
p-value. The reference runs the two one-sided score tests with test_poisson_2indep (a
cross-function check within statsmodels): 'smaller' at the lower bound 0.5 and 'larger'
at the upper bound 2. The library reports the statistic of the test with the larger
p-value.

Run: python statsmodels_nonequivalence_poisson_2indep_statistic.py
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

import statsmodels.stats.rates as r

args = (30, 10.0, 20, 12.0)
res = r.nonequivalence_poisson_2indep(*args, 0.5, 2.0, method="score", compare="ratio")
t1 = r.test_poisson_2indep(*args, value=0.5, method="score", compare="ratio", alternative="smaller")
t2 = r.test_poisson_2indep(*args, value=2.0, method="score", compare="ratio", alternative="larger")
want = t1.statistic if t1.pvalue < t2.pvalue else t2.statistic
verdict(not (abs(float(res.statistic) - float(want)) <= 1e-12),
        f"statistic={float(res.statistic)!r}; one-sided tests: lower bound statistic {float(t1.statistic)!r} "
        f"(p {float(t1.pvalue):.4g}), upper bound statistic {float(t2.statistic)!r} (p {float(t2.pvalue):.4g})")
