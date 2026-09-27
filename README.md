# Numerical correctness ledger

Checks of statistical and scientific Python functions against independently computed answers, and a list of the places where current releases return wrong results.

## What is here

- `FINDINGS.md`: confirmed defects in scipy, statsmodels, networkx and mne, each with a short explanation of the correct value.
- `repro/`: one standalone script per defect. Each imports only the library under test plus numpy, scipy or mpmath, prints what it found, and exits with status 1 while the defect is present.
- `run_all.py`: runs every script against the installed packages and writes a table.
- `STATUS.md`: the latest run against current releases and development versions.

## How the defects were found

A daily job runs about 1,000 checks on 126 functions in scipy, statsmodels, networkx, mne, astropy and numpy. Each check compares a library result with a value computed another way: exact enumeration of small cases, exact rational arithmetic, high-precision arithmetic (mpmath), brute force, or a mathematical identity the function must satisfy (for example, invariance under relabelling or rescaling). The checks were written with the help of AI models. A check that fails is not reported until a second review and a direct recomputation agree that the library, not the check, is wrong; many failing checks turn out to be the check's fault and are discarded.

## Using the scripts

```
pip install scipy statsmodels networkx mne mpmath
python run_all.py
```

or run a single script, for example `python repro/scipy_skewtest_symmetric_sample.py`.

## Scope and limits

The list covers only functions that the checks reach. A function that is not listed has not been shown to be correct. Corrections and counterexamples are welcome through the issue tracker.

This project is not affiliated with the projects whose code it checks.
