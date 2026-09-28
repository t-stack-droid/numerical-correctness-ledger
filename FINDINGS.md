# Findings

Each row has a script in `repro/` that exits with status 1 while the discrepancy is present, 0 when its comparison does not reproduce it, and 2 when it cannot run or a precondition fails. The expected values come from analytic references (closed forms, mpmath at high precision), exact enumeration, brute force, cross-function checks (another function of the same library, named in the script), or a property the library documents or must satisfy (an identity or an invariance), as described in each script. `STATUS.md` records which versions each script was run against and the outcome. Each script tests the parameter values it states; a row does not claim more than that.

The column "Versions with the defect" lists the tested releases in which the script reports the defect, and whether it still does on the development branch. Releases tested: scipy 1.16.3, 1.17.0, 1.17.1, 1.18.0, 1.18.1; statsmodels 0.14.6, 0.15.0; networkx 3.4.2, 3.5, 3.6, 3.6.1, 3.7rc0, 3.7; mne 1.11.0, 1.12.1, 1.13.2. Per-version outcomes are in `VERSIONS.md`.

## Wrong results

| Library | Function | What is wrong | Versions with the defect | Script |
|---|---|---|---|---|
| scipy | `stats.spearmanr(nan_policy="omit")` | p-value 1.0 for perfectly monotone data after omission; the asymptotic (t-based) p-value scipy uses is 0 | all tested (1.16.3 to 1.18.1); development: yes | `scipy_spearmanr_omit_pvalue.py` |
| scipy | `stats.truncate(...).icdf` | inf for the median of a standard normal truncated to [10, inf) (expected 10.0684) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_truncate_icdf_far_tail.py` |
| scipy | `stats.poisson_means_test` | two-sided p-value 0.865 instead of 1 when the observed rates are equal (counts 1 and 1, equal exposures); the (0, 0) outcome is dropped | all tested (1.16.3 to 1.18.1); development: yes | `scipy_poisson_means_test_equal_rates.py` |
| scipy | `stats.skewtest` | Z = 1.01, p = 0.31 for a sample with skewness exactly 0 (expected 0 and 1) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_skewtest_symmetric_sample.py` |
| scipy | `stats.barnard_exact` | the docstring example returns 0.034077, but with the tied table [[3, 8], [12, 7]] included the tail probability is at least 0.034109; the returned value equals the maximum with that table left out, and the float64 pooled Wald formula ranks the tie above the observed statistic although they are equal | all tested (1.16.3 to 1.18.1); development: yes | `scipy_barnard_exact_ties.py` |
| scipy | `stats.barnard_exact` | swapping the rows changes the two-sided p-value (0.0055692 vs 0.0051505 for [[14, 9], [5, 19]], pooled=False); by symmetry they are equal (consistent with the tie handling above; the script shows only the asymmetry) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_barnard_exact_row_swap.py` |
| scipy | `stats.boxcox_normmax(method="mle", ymax=...)` | the returned lambda can violate the ymax bound when all data exceed 1 and ymax < log(max(x)); in the example the transform is 35% above ymax | all tested (1.16.3 to 1.18.1); development: yes | `scipy_boxcox_normmax_ymax.py` |
| scipy | `stats.dlaplace.logpmf` | -inf at k = -1000, a = 1 (expected -1000.77) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_dlaplace_logpmf_large_k.py` |
| scipy | `stats.dlaplace.sf` | 0 at k = 10, a = 5 (expected 1.29e-24) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_dlaplace_sf_far_tail.py` |
| scipy | `special.hyperu` | NaN at a = -1.5, b = 0 for x = 0.1, 1 and 5, where the function is finite (-0.365, 0.170, 9.46) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_hyperu_negative_a.py` |
| scipy | `special.nctdtridf` | fails to invert `nctdtr` for an attainable probability: releases return the 1e100 sentinel, the development branch NaN | all tested (1.16.3 to 1.18.1); development: yes | `scipy_nctdtridf_roundtrip.py` |
| scipy | `special.nctdtridf` | for df below 2, 12 of 128 inversions of attainable probabilities return the 1e100 or -1e100 sentinel | all tested (1.16.3 to 1.18.1); development: not reproduced | `scipy_nctdtridf_small_df.py` |
| scipy | `special.obl_rad1`, `special.obl_rad2` | the pair fails its Wronskian identity at the sampled points x = 0.2, 0.5 and 1 (m = n = 0, c = 1): about 0 instead of 1/(x^2 + 1); `obl_rad2` returns values of order 1e-320 there | all tested (1.16.3 to 1.18.1); development: yes | `scipy_obl_rad2_small_x.py` |
| scipy | `special.pro_rad1`, `special.pro_rad2` | the pair's scaled Wronskian is 0.870 at x = 1.5 (0.996 at 1.1, 0.983 at 1.2; 1 at 2 and 4) instead of 1 (m = n = 1, c = 1) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_pro_rad_wronskian.py` |
| statsmodels | `stats.api.runstest_1samp` | with the default correction and n < 50, a deviation of the number of runs from its expectation strictly between -0.5 and 0.5 is shifted by 0.5 instead of set to 0 (z = 0.46, p = 0.65 instead of 0 and 1) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_runstest_continuity_correction.py` |
| statsmodels | `stats.api.runstest_2samp` | the same continuity correction error (z = 0.34, p = 0.74 instead of 0 and 1) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_runstest_2samp_continuity_correction.py` |
| statsmodels | `stats.rates.confint_poisson_2indep(method="sqrtcc", compare="ratio")` | the interval does not change when exposure2 is multiplied by 4, so unequal exposures are ignored | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_confint_poisson_2indep_sqrtcc_exposure.py` |
| statsmodels | `stats.rates.nonequivalence_poisson_2indep` | p-value 1.285, outside [0, 1] | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_nonequivalence_poisson_2indep.py` |
| statsmodels | `stats.rates.nonequivalence_poisson_2indep` | the reported statistic is that of the one-sided test with the larger p-value, although documented as that of the smaller (cross-checked with `test_poisson_2indep`) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_nonequivalence_poisson_2indep_statistic.py` |
| statsmodels | `stats.diagnostic.het_goldfeldquandt` (alternative "increasing", the default) | p-value from F(df1, df2) instead of F(df2, df1): 0.0028 instead of 0.0152 with 10 and 26 degrees of freedom | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_het_goldfeldquandt_df.py` |
| statsmodels | `stats.diagnostic.het_goldfeldquandt(alternative="decreasing")` | the same swap: 0.9972 instead of 0.9848 | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_het_goldfeldquandt_df_decreasing.py` |
| statsmodels | `stats.multitest.fdrcorrection_twostage(maxiter=False)` | runs one stage (as maxiter=0), though documented as two-stage (maxiter=1) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_fdrcorrection_twostage_bool_maxiter.py` |
| statsmodels | `stats.multitest.fdrcorrection_twostage(maxiter=True)` | runs two stages (as maxiter=1), though documented as full iteration (maxiter=-1) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_fdrcorrection_twostage_maxiter_true.py` |
| statsmodels | `genmod.families.Tweedie(eql=False).loglike_obs` | -inf at y = 1e-100 (var_power 1.1), where the log-density is finite (-1832.96) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_tweedie_loglike_underflow.py` |
| statsmodels | `stats.proportion.score_test_proportions_2indep(compare="diff")` with a nonzero `value` | wrong constrained estimate of the proportions under the null (a cubic coefficient uses count2 in place of nobs2): 0.3438 instead of 0.3481 in the example | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_score_test_proportions_2indep_constrained_mle.py` |
| statsmodels | `stats.proportion.confint_proportions_2indep(method="score", compare="diff")` | interval (-0.2871, 0.1335) instead of (-0.2944, 0.1341) for 12/35 vs 18/42, from the constrained estimate above | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_confint_proportions_2indep_score_diff.py` |
| statsmodels | `stats.rates.confint_poisson(0, 1, method="midp-c")` | a nearly collapsed, slightly reversed interval (2.99573228, 2.99573227) instead of (0, 2.99573) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_confint_poisson_midp_zero_count.py` |
| statsmodels | `stats.nonparametric.jonckheere_terpstra` | for completely tied data (null variance exactly 0), group sizes (4, 4, 4) raise the intended error but (5, 4, 6) return p = 0.5 (minor) | 0.15.0; not available in tested releases before 0.15.0; development: yes | `statsmodels_jonckheere_terpstra_fully_tied.py` |
| networkx | `group_betweenness_centrality` | depends on node labels: 0.5 for a star labelled 6, 11, 2, 3 with group {11, 3}; the relabelled star gives the correct 0 | 3.7rc0 to 3.7; development: yes | `networkx_group_betweenness_regression.py` |
| networkx | `group_betweenness_centrality` | on a path plus the isolated node 5, the group {0, 4, 5, 7, 8} gives 5 while {0, 4, 7, 8} gives 3 (brute force 3 for both); relabelling gives 3 | 3.7rc0 to 3.7; development: yes | `networkx_group_betweenness_isolate.py` |
| networkx | `single_source_all_shortest_paths` | the source's own path [0] is listed twice in an undirected example with a zero-weight edge at the source | all tested (3.4.2 to 3.7); development: yes | `networkx_single_source_all_shortest_paths_zero_weight.py` |
| mne | `stats.permutation_cluster_1samp_test(n_permutations="all")` | documented as exact, but p = 1/511 where enumeration of the 512 sign classes gives 1/512 (n = 10, seeds 0 and 1); the null has 511 entries, a one-entry deficit in the rounded absolute-statistic multiset whose missing value differs between the two seeds | all tested (1.11.0 to 1.13.2); development: yes | `mne_permutation_cluster_1samp_all_not_exact.py` |
| mne | `stats.permutation_cluster_1samp_test(n_permutations="all")` | p-values depend on the seed: for the cluster at location 3 of a 10 x 4 example, p = 0.763209 with seed=0 and 0.765166 with seed=1 (exact 0.763672) | all tested (1.11.0 to 1.13.2); development: yes | `mne_permutation_cluster_1samp_all_seed_dependent.py` |
| mne | `stats.permutation_cluster_1samp_test`, exact one-tailed | the 64-entry null distribution has the observed statistic twice and 42 zeros; the 64 sign patterns give it once and 43 zeros (p = 2/64 instead of 1/64 for n = 6) | all tested (1.11.0 to 1.13.2); development: yes | `mne_permutation_cluster_1samp_exact_one_tailed.py` |
| mne | `stats.f_mway_rm(correction=True)` | Greenhouse-Geisser epsilon from uncentered cross-products, so the corrected p-value is wrong; F agrees with an independent computation (the script reports both) | all tested (1.11.0 to 1.13.2); development: yes | `mne_f_mway_rm_greenhouse_geisser.py` |
| mne | `stats.fdr_correction` | at the Benjamini-Hochberg boundary it rejects with a strict inequality: reject [True, False] where the rule and its own adjusted p-values [0.02, 0.05] give [True, True] (a boundary-convention mismatch; no loss of FDR control is shown) | all tested (1.11.0 to 1.13.2); development: yes | `mne_fdr_correction_boundary.py` |

## Accuracy losses

Finite results with far fewer correct digits than the reference, at the sampled parameters stated.

| Library | Function | What is wrong | Versions with the defect | Script |
|---|---|---|---|---|
| scipy | `special.itj0y0` | integral of Y0: absolute error above 1e-12 at 59 of 101 sampled points in [12, 37], largest 4.1e-9 at x = 20 (relative 2.4e-8) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_itj0y0_accuracy.py` |
| scipy | `special.hyperu` | at b = -4.7012, x = 6.9068: relative error 7.1e-8 (a = 1.4836) and 3.0e-10 (a = 2.4836); a = 3.4836 is accurate to about 1e-13 | all tested (1.16.3 to 1.18.1); development: yes | `scipy_hyperu_negative_b_accuracy.py` |
| scipy | `special.y1p_zeros` | real zeros 4, 5 and 6 of Y1' have relative errors 1.4e-9, 2.7e-10 and 6.8e-11 (the first three 7.4e-14 or better) | all tested (1.16.3 to 1.18.1); development: yes | `scipy_y1p_zeros_real_accuracy.py` |

## Unexpected exceptions

| Library | Function | Versions with the defect | Script |
|---|---|---|---|
| statsmodels | `chisquare_effectsize(axis=1)` with 3 x 4 input (ValueError) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_chisquare_effectsize_axis.py` |
| statsmodels | `transform_corr_normal(method="spearman", return_var=True)` with correlations of mixed sign (ValueError; return_var=False works) | 0.15.0; not available in tested releases before 0.15.0; development: yes | `statsmodels_transform_corr_normal_spearman.py` |
| statsmodels | `runstest_2samp` with integer arrays containing ties (casting error; the same values as floats work) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_runstest_2samp_integer_ties.py` |
| statsmodels | `confint_proportions_2indep(5, 20, 15, 25, method="score", compare="diff")` (ValueError from NaN in the root finder) | all tested (0.14.6 to 0.15.0); development: yes | `statsmodels_confint_proportions_2indep_score_raise.py` |
| networkx | `generate_random_paths` on a single-node graph (ValueError from NaN probabilities; a source comment says isolated nodes are handled) | all tested (3.4.2 to 3.7); development: yes | `networkx_generate_random_paths_isolated.py` |
| scipy | `stats.kstest(x, "norm", args=(loc, scale))`, TypeError on releases 1.18.0 and 1.18.1 (1.17.1 and the development branch work) | 1.18.0 to 1.18.1; development: not reproduced | `scipy_kstest_norm_args.py` |

## Documentation and convention questions

The scripts for documentation questions read the installed docstring; the truncate script tests a convention.

| Library | Function | Versions with the defect | Script |
|---|---|---|---|
| mne | `stats.f_oneway(sigma=...)`: docstring and code describe different regularisations | 1.12.1 to 1.13.2; not available in tested releases before 1.12.1; development: yes | `mne_f_oneway_sigma_docstring.py` |
| networkx | `node_degree_xy(nodes=...)`: documented edge selection differs from the code | all tested (3.4.2 to 3.7); development: yes | `networkx_node_degree_xy_nodes_docstring.py` |
| networkx | `edge_current_flow_betweenness_centrality`: a directed graph raises `NetworkXNotImplemented`, documented as `NetworkXError` (not a subclass) | all tested (3.4.2 to 3.7); development: yes | `networkx_edge_current_flow_digraph_exception_docstring.py` |
| networkx | `group_degree_centrality`: S = [1, 1] gives 0.667 and S = {1} gives 0.5; the docstring accepts a list or set and does not say how repeated nodes are treated | all tested (3.4.2 to 3.7); development: yes | `networkx_group_degree_centrality_duplicates.py` |
| scipy | `special.y1p_zeros(complex=True)`: the docstring says the zeros have negative real part; the first zero returned (0.5768 + 0.9040j, a genuine zero) has positive real part | all tested (1.16.3 to 1.18.1); development: yes | `scipy_y1p_zeros_complex_docstring.py` |
| scipy | `stats.truncate(Normal(), lb, ub)`: pdf 0 and logpdf -inf exactly at a finite truncation bound, while `support()` is the closed interval, a truncated Uniform has positive density at its bounds, and `truncnorm` gives phi(lb) / mass | all tested (1.16.3 to 1.18.1); development: yes | `scipy_truncate_pdf_at_bound.py` |

## Corrections

Withdrawn on 2026-09-28 after an independent review of the published claims:

- scipy `stats.estimated_cdf(method="averaged_inverted_cdf")` returning the same values as `inverted_cdf`. Taken as the generalized inverse of the quantile function, estimators 1 and 2 of Hyndman and Fan give the same CDF, so the expected value 0.375 used earlier was not justified.
- networkx `edge_current_flow_betweenness_centrality` normalisation. The normalised values equal 2/[(n-1)(n-2)] times the function's own unnormalised values (1.5, 2, 1.5 on a path of 4 nodes), as documented. The earlier script used the unnormalised values of `edge_betweenness_centrality` (3, 4, 3) instead.
- networkx `find_induced_nodes` on a star graph. The docstring defers the definition of induced nodes to Elidan and Gould (2008), which was not checked here; without it the expected {0, 1, 2} was not justified. (The function returns no induced nodes for any path of length 2.)

Corrected or narrowed on the same date:

- `scipy.special.nctdtridf` was listed as not reproduced on the development branch. The development branch returns NaN for that input, which the earlier script did not detect; scripts now reject NaN results.
- `scipy.stats.truncate` at a truncation bound moved from wrong results to documentation and convention questions.
- mne `permutation_cluster_1samp_test`: the earlier "seed-dependent p-values" note for n_permutations="all" had no script; it now has one, on an example where the p-value changes with the seed (in the original example the p-value does not change with the seed; only the missing value in the null multiset does). The one-tailed row no longer names which sign pattern is missing (it cannot be identified from the null distribution).
- statsmodels Tweedie: the earlier note that an overflow case was fixed in 0.15.0 was removed (not verified here).
- statsmodels `nonequivalence_poisson_2indep`: the p-value above 1 and the statistic from the wrong one-sided test are now separate rows and scripts.
- `scipy.special.hyperu`, `special.itj0y0`, `special.pro_rad1`/`pro_rad2`: rows now state the sampled parameters and errors instead of ranges.
- Scripts that covered two cases (`dlaplace` logpmf and sf, `barnard_exact` ties and row swap, `group_betweenness_centrality` labels and isolated nodes, `het_goldfeldquandt` increasing and decreasing, `fdrcorrection_twostage` False and True, `runstest_1samp` and `runstest_2samp`) were split so each case has its own outcome; `scipy_dlaplace_log_and_tail.py` was replaced by two scripts.
