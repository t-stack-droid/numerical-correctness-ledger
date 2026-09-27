"""statsmodels nonequivalence_poisson_2indep: statistic from the wrong test, p-value above 1.

The result documents `statistic` as the statistic of the one-sided test with the smaller
p-value. The code picks the other one. The returned p-value also exceeds 1.

Run: python statsmodels_nonequivalence_poisson_2indep.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import statsmodels.stats.rates as r

args = (30, 10.0, 20, 12.0)
res = r.nonequivalence_poisson_2indep(*args, 0.5, 2.0, method="score", compare="ratio")
t1 = r.test_poisson_2indep(*args, value=0.5, method="score", compare="ratio", alternative="smaller")
t2 = r.test_poisson_2indep(*args, value=2.0, method="score", compare="ratio", alternative="larger")
want = t1.statistic if t1.pvalue < t2.pvalue else t2.statistic
bad = abs(float(res.statistic) - float(want)) > 1e-12 or float(res.pvalue) > 1
verdict(bad, f"statistic={float(res.statistic)!r} (expected {float(want)!r}), pvalue={float(res.pvalue)!r}")
