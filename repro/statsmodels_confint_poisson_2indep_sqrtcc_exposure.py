"""statsmodels confint_poisson_2indep(method='sqrtcc', compare='ratio') ignores exposures.

The rate ratio is (c1/e1)/(c2/e2). With the counts fixed, multiplying e2 by 4 multiplies
the ratio, and any confidence interval for it, by 4. The sqrtcc interval does not
change, so it is an interval for c1/c2. Example: counts 10 and 20, exposures 10 and 40
(rate ratio 2); the interval returned excludes 2.

Run: python statsmodels_confint_poisson_2indep_sqrtcc_exposure.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

from statsmodels.stats.rates import confint_poisson_2indep

a = confint_poisson_2indep(10, 10, 20, 10, method="sqrtcc", compare="ratio")
b = confint_poisson_2indep(10, 10, 20, 40, method="sqrtcc", compare="ratio")
ok = abs(b[0] - 4 * a[0]) < 1e-9 * abs(4 * a[0]) and abs(b[1] - 4 * a[1]) < 1e-9 * abs(4 * a[1])
verdict(not ok, f"exposure2=10: {tuple(map(float, a))}; exposure2=40: {tuple(map(float, b))}; "
                "expected the second to be 4 times the first")
