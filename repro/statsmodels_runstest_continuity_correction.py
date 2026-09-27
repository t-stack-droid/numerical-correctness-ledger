"""statsmodels runstest_1samp and runstest_2samp: wrong continuity correction.

With correction=True (the default) and fewer than 50 observations, the code uses `elif
rdemean < 0.5: z = rdemean + 0.5`. The continuity correction moves the deviation towards
0 and should apply only below -0.5 (0 in between). When the number of runs equals its
expectation the statistic must be 0 and the p-value 1.

Run: python statsmodels_runstest_continuity_correction.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from statsmodels.stats.api import runstest_1samp, runstest_2samp

# [1,1,0,1,0,0]: 3 ones, 3 zeros, 4 runs; expected runs 2*3*3/6 + 1 = 4
z1, p1 = runstest_1samp(np.array([1, 1, 0, 1, 0, 0.0]), cutoff=0.5, correction=True)
# combined order x x x y y x y y x y: 6 runs; expected 2*5*5/10 + 1 = 6
z2, p2 = runstest_2samp(np.array([1, 2, 3, 6, 9.0]), np.array([4, 5, 7, 8, 10.0]), correction=True)
verdict(abs(z1) > 1e-12 or abs(z2) > 1e-12,
        f"1samp z={float(z1):.4f} p={float(p1):.4f}; 2samp z={float(z2):.4f} p={float(p2):.4f}; "
        "expected z=0, p=1 in both")
