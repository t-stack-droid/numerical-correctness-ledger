# Findings

Each row has a script in `repro/` that exits with status 1 while the defect is present. The expected values are derived independently of the library (closed forms, exact enumeration, mpmath, or brute force), as described in each script. `STATUS.md` records which versions each script was run against and the outcome.

## Wrong results

| Library | Function | What is wrong | Script |
|---|---|---|---|
| scipy | `stats.spearmanr(nan_policy="omit")` | p-value 1.0 for perfectly monotone data (should be 0) | `scipy_spearmanr_omit_pvalue.py` |
| scipy | `stats.estimated_cdf(method="averaged_inverted_cdf")` | identical to `inverted_cdf`; 0.5 instead of 0.375 in the example | `scipy_estimated_cdf_averaged_inverted_cdf.py` |
| scipy | `stats.truncate(...).pdf`, `.logpdf` | 0 and -inf at a finite truncation bound | `scipy_truncate_pdf_at_bound.py` |
| scipy | `stats.truncate(...).icdf` | inf or inaccurate in the far tail | `scipy_truncate_icdf_far_tail.py` |
| scipy | `stats.poisson_means_test` | p-value below 1 when the observed rates are equal | `scipy_poisson_means_test_equal_rates.py` |
| scipy | `stats.skewtest` | Z = 1.01, p = 0.31 for a perfectly symmetric sample (should be 0 and 1) | `scipy_skewtest_symmetric_sample.py` |
| statsmodels | `stats.api.runstest_1samp`, `runstest_2samp` | continuity correction applied in the wrong range (default settings, n < 50) | `statsmodels_runstest_continuity_correction.py` |
| statsmodels | `stats.rates.confint_poisson_2indep(method="sqrtcc", compare="ratio")` | ignores exposures; interval for the count ratio, not the rate ratio | `statsmodels_confint_poisson_2indep_sqrtcc_exposure.py` |
| statsmodels | `stats.rates.nonequivalence_poisson_2indep` | statistic taken from the wrong one-sided test; p-value above 1 | `statsmodels_nonequivalence_poisson_2indep.py` |
| statsmodels | `stats.diagnostic.het_goldfeldquandt` | F degrees of freedom swapped for "increasing" (default) and "decreasing" | `statsmodels_het_goldfeldquandt_df.py` |
| statsmodels | `stats.multitest.fdrcorrection_twostage` | `maxiter=False` or `True` runs the wrong number of stages | `statsmodels_fdrcorrection_twostage_bool_maxiter.py` |
| statsmodels | `genmod.families.Tweedie(eql=False).loglike_obs` | -inf for tiny positive observations (the overflow case was fixed in 0.15.0; underflow was not) | `statsmodels_tweedie_loglike_underflow.py` |
| networkx | `group_betweenness_centrality` | results depend on node labels and are wrong across components; regression in 3.7 | `networkx_group_betweenness_regression.py` |
| mne | `stats.permutation_cluster_1samp_test(n_permutations="all")` | not exact: samples 511 of 512 classes for n = 10, seed-dependent p-values | `mne_permutation_cluster_1samp_all_not_exact.py` |
| mne | `stats.permutation_cluster_1samp_test`, exact one-tailed | observed statistic counted twice, all-flip pattern omitted | `mne_permutation_cluster_1samp_exact_one_tailed.py` |
| mne | `stats.f_mway_rm(correction=True)` | Greenhouse-Geisser epsilon from uncentered cross-products | `mne_f_mway_rm_greenhouse_geisser.py` |
| mne | `stats.fdr_correction` | strict inequality at the boundary contradicts Benjamini-Hochberg and the returned adjusted p-values | `mne_fdr_correction_boundary.py` |

## Crashes

| Library | Function | Script |
|---|---|---|
| statsmodels | `chisquare_effectsize(axis=1)` | `statsmodels_chisquare_effectsize_axis.py` |
| statsmodels | `transform_corr_normal(method="spearman")` with correlations of mixed sign | `statsmodels_transform_corr_normal_spearman.py` |
| statsmodels | `runstest_2samp` with integer arrays containing ties | `statsmodels_runstest_2samp_integer_ties.py` |

## Documentation questions

| Library | Function | Script |
|---|---|---|
| mne | `stats.f_oneway(sigma=...)`: docstring and code describe different regularisations | `mne_f_oneway_sigma_docstring.py` |
