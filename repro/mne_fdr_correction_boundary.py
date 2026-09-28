"""mne fdr_correction: strict inequality at the Benjamini-Hochberg boundary.

The docstring says method='indep' implements Benjamini/Hochberg, which rejects the
hypotheses with the i smallest p-values for the largest i such that p_(i) <= i alpha /
m. For p = [0.01, 0.05] and alpha = 0.05: 0.05 <= 2 * 0.05 / 2, so both are rejected,
and the adjusted p-values are [0.02, 0.05]. The library returns those adjusted p-values
but rejects only the first.

Run: python mne_fdr_correction_boundary.py
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

import numpy as np
from mne.stats import fdr_correction

reject, p_adj = fdr_correction([0.01, 0.05], alpha=0.05)
ok = np.asarray(reject).tolist() == [True, True] and np.allclose(p_adj, [0.02, 0.05])
verdict(not ok, f"reject={np.asarray(reject).tolist()}, p_adj={np.asarray(p_adj).tolist()}; "
                "expected reject=[True, True], p_adj=[0.02, 0.05]")
