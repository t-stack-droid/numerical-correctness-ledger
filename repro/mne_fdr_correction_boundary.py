"""mne fdr_correction: rejection disagrees with the adjusted p-values at the boundary.

Benjamini-Hochberg rejects p_(i) <= i alpha / m. The code uses a strict inequality, so a
p-value exactly on the boundary is not rejected although its adjusted p-value equals
alpha.

Run: python mne_fdr_correction_boundary.py
Exit status 1 means the defect is present in the installed version, 0 means it is not.
"""
import sys


def verdict(present, message):
    print(("DEFECT PRESENT: " if present else "not reproduced: ") + message)
    sys.exit(1 if present else 0)

import numpy as np
from mne.stats import fdr_correction

reject, p_adj = fdr_correction([0.01, 0.05], alpha=0.05)
verdict(not np.array_equal(reject, p_adj <= 0.05), f"reject={reject.tolist()}, p_adj={p_adj.tolist()}")
