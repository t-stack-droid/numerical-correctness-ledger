"""mne f_oneway(sigma=...): documentation and code disagree (question, not a wrong value).

The docstring says sigma is 'added to the within-group mean square' ('relative', the
default, multiplies sigma by the median within-group mean square). The code adds it to
the within-group sum of squares before dividing by the degrees of freedom. For [1,2,3]
vs [4,5,6] with sigma = 0.5: MSB = 13.5, MSW = 1, so the documented statistic is 13.5 /
1.5 = 9.0; the code gives 13.5 / 1.125 = 12.0. sigma = 0 (the default) is unaffected.
The script reads the installed docstring.

Run: python mne_f_oneway_sigma_docstring.py
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
import numpy as np
from mne.stats import f_oneway

documented = "added to the within-group mean square" in " ".join(inspect.getdoc(f_oneway).split())
got = float(np.atleast_1d(f_oneway(np.array([1.0, 2, 3]), np.array([4.0, 5, 6]), sigma=0.5))[0])
verdict(documented and not (abs(got - 9.0) <= 1e-9),
        f"F = {got!r}; the documented formula gives 9.0; docstring wording present: {documented}")
