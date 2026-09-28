# Status

Run on 2026-09-28 with:

- scipy: release 1.18.1, development 2.0.0.dev0
  (release: numpy 2.5.3, mpmath 1.4.1; development: numpy 2.6.0.dev0, mpmath 1.5.0a1)
- statsmodels: release 0.15.0, development 0.15.1.dev84+g15b987752
  (release: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1; development: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1)
- networkx: release 3.7, development 3.7.1rc0.dev0
  (release: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1; development: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1)
- mne: release 1.13.2, development 1.14.0.dev48+gd7ffc6037
  (release: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1; development: numpy 2.5.3, scipy 1.18.1, mpmath 1.4.1)

| Script | Release | Development | Message (release) |
|---|---|---|---|
| `mne_f_mway_rm_greenhouse_geisser.py` | present | present | p = 0.005284954095414777, expected 0.004901544000240323 (epsilon 0.9251) |
| `mne_f_oneway_sigma_docstring.py` | present | present | F = 12.0, documented formula gives 9.0 |
| `mne_fdr_correction_boundary.py` | present | present | reject=[True, False], p_adj=[0.02, 0.05] |
| `mne_permutation_cluster_1samp_all_not_exact.py` | present | present | 'all': len(H0) = 511, p = [0.0019569471624266144]; exact (n_permutations=512): len(H0) = 512, p = [0.001953125] |
| `mne_permutation_cluster_1samp_exact_one_tailed.py` | present | present | observed statistic appears 2 times in the 64-pattern null; expected 1 |
| `networkx_generate_random_paths_isolated.py` | present | present | raised ValueError: probabilities contain NaN |
| `networkx_group_betweenness_regression.py` | present | present | (got, expected) = [(0.5, 0.0), (5.0, 3.0)] |
| `networkx_node_degree_xy_nodes_docstring.py` | present | present | got []; the documented behaviour gives 4 pairs |
| `scipy_dlaplace_log_and_tail.py` | present | present | logpmf(-1000, 1) = -inf (expected -1000.7719368329053); sf(10, 5) = 0.0 (expected 1.2908835202659582e-24) |
| `scipy_hyperu_negative_a.py` | present | present | (x, scipy, mpmath) = [(0.1, nan, -0.3654721946005413), (1.0, nan, 0.17023014757496954), (5.0, nan, 9.463159393834404)] |
| `scipy_nctdtridf_roundtrip.py` | present | present | p = 0.9785864072356195; nctdtridf(p, nc, t) = 1e+100, CDF residual 2.5e-04 (df = 7.42072530317493 solves it) |
| `scipy_poisson_means_test_equal_rates.py` | present | present | pvalue = 0.8646647167633871, expected 1.0 |
| `scipy_skewtest_symmetric_sample.py` | present | present | statistic=1.0108048609177787 pvalue=0.3121098361421897; expected 0 and 1 |
| `scipy_spearmanr_omit_pvalue.py` | present | present | statistic=1.0000000000000002 pvalue=1.0; expected statistic 1 and pvalue 0 |
| `scipy_truncate_icdf_far_tail.py` | present | present | icdf(0.5) = inf, expected 10.06841183608143 |
| `scipy_truncate_pdf_at_bound.py` | present | present | truncated Normal at its bound: pdf 0.0, logpdf -inf; support (2.0, 8.0); truncnorm pdf 2.373215532822906; truncated Uniform pdf at its bound 0.1666666666666666 |
| `statsmodels_chisquare_effectsize_axis.py` | present | present | axis=1 raised ValueError: operands could not be broadcast together with shapes (3,4) (3,) |
| `statsmodels_confint_poisson_2indep_sqrtcc_exposure.py` | present | present | exposure2=10: (0.22451098663306185, 1.0565389600576878); exposure2=40: (0.22451098663306185, 1.0565389600576878); expected the second to be 4 times the first |
| `statsmodels_fdrcorrection_twostage_bool_maxiter.py` | present | present | maxiter=False corrected p [0.06, 0.06, 0.06, 0.45, 1.0], maxiter=1 [0.024, 0.024, 0.024, 0.18, 0.432] |
| `statsmodels_het_goldfeldquandt_df.py` | present | present | pvalue=0.0027834938934368355, expected 0.015219391272578164 (df1=10, df2=26) |
| `statsmodels_nonequivalence_poisson_2indep.py` | present | present | statistic=4.746928831711439 (expected -0.365148371670111), pvalue=1.284999345311911 |
| `statsmodels_runstest_2samp_integer_ties.py` | present | present | raised UFuncTypeError: Cannot cast ufunc 'add' output from dtype('float64') to dtype('int64') with casting rule 'same_kind' |
| `statsmodels_runstest_continuity_correction.py` | present | present | 1samp z=0.4564 p=0.6481; 2samp z=0.3354 p=0.7373; expected z=0, p=1 in both |
| `statsmodels_transform_corr_normal_spearman.py` | present | present | raised ValueError: The values in t must be monotonically increasing or monotonically decreasing; repeated values are allowed. |
| `statsmodels_tweedie_loglike_underflow.py` | present | present | got -inf, expected -1832.9551620564887 |
