"""mne f_oneway(sigma=...): documentation and code disagree (question, not a wrong value).

The docstring says sigma * median(MSW) is added to the within-group mean square. The
code adds it to the within-group sum of squares before dividing by the degrees of
freedom. For [1,2,3] vs [4,5,6] with sigma = 0.5: MSB = 13.5, MSW = 1, so the documented
statistic is 13.5 / 1.5 = 9.0; the code gives 13.5 / 1.125 = 12.0.

Run: python mne_f_oneway_sigma_docstring.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from mne.stats import f_oneway

got = float(np.atleast_1d(f_oneway(np.array([1.0, 2, 3]), np.array([4.0, 5, 6]), sigma=0.5))[0])
verdict(abs(got - 9.0) > 1e-9, f"F = {got!r}, documented formula gives 9.0")
