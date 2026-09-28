# Versions

Outcome of each script in `repro/` on earlier releases and on the development branch ("defect": the script reports the defect; "-": not reproduced; "n/a": the function or option does not exist in that tested version). Run on 2026-09-28. For networkx releases before 3.7 the test environments had no numpy or scipy; those scripts ran with numpy and scipy from the networkx 3.7 environment on the import path. `STATUS.md` has the current release and development results with each script's message.

## scipy

| Script | 1.16.3 | 1.17.0 | 1.17.1 | 1.18.0 | 1.18.1 | development |
|---|---|---|---|---|---|---|
| `scipy_barnard_exact_row_swap.py` | defect | defect | defect | defect | defect | defect |
| `scipy_barnard_exact_ties.py` | defect | defect | defect | defect | defect | defect |
| `scipy_boxcox_normmax_ymax.py` | defect | defect | defect | defect | defect | defect |
| `scipy_dlaplace_logpmf_large_k.py` | defect | defect | defect | defect | defect | defect |
| `scipy_dlaplace_sf_far_tail.py` | defect | defect | defect | defect | defect | defect |
| `scipy_hyperu_negative_a.py` | defect | defect | defect | defect | defect | defect |
| `scipy_hyperu_negative_b_accuracy.py` | defect | defect | defect | defect | defect | defect |
| `scipy_itj0y0_accuracy.py` | defect | defect | defect | defect | defect | defect |
| `scipy_kstest_norm_args.py` | - | - | - | defect | defect | - |
| `scipy_nctdtridf_roundtrip.py` | defect | defect | defect | defect | defect | defect |
| `scipy_nctdtridf_small_df.py` | defect | defect | defect | defect | defect | - |
| `scipy_obl_rad2_small_x.py` | defect | defect | defect | defect | defect | defect |
| `scipy_poisson_means_test_equal_rates.py` | defect | defect | defect | defect | defect | defect |
| `scipy_pro_rad_wronskian.py` | defect | defect | defect | defect | defect | defect |
| `scipy_skewtest_symmetric_sample.py` | defect | defect | defect | defect | defect | defect |
| `scipy_spearmanr_omit_pvalue.py` | defect | defect | defect | defect | defect | defect |
| `scipy_truncate_icdf_far_tail.py` | defect | defect | defect | defect | defect | defect |
| `scipy_truncate_pdf_at_bound.py` | defect | defect | defect | defect | defect | defect |
| `scipy_y1p_zeros_complex_docstring.py` | defect | defect | defect | defect | defect | defect |
| `scipy_y1p_zeros_real_accuracy.py` | defect | defect | defect | defect | defect | defect |

## statsmodels

| Script | 0.14.6 | 0.15.0 | development |
|---|---|---|---|
| `statsmodels_chisquare_effectsize_axis.py` | defect | defect | defect |
| `statsmodels_confint_poisson_2indep_sqrtcc_exposure.py` | defect | defect | defect |
| `statsmodels_confint_poisson_midp_zero_count.py` | defect | defect | defect |
| `statsmodels_confint_proportions_2indep_score_diff.py` | defect | defect | defect |
| `statsmodels_confint_proportions_2indep_score_raise.py` | defect | defect | defect |
| `statsmodels_fdrcorrection_twostage_bool_maxiter.py` | defect | defect | defect |
| `statsmodels_fdrcorrection_twostage_maxiter_true.py` | defect | defect | defect |
| `statsmodels_het_goldfeldquandt_df.py` | defect | defect | defect |
| `statsmodels_het_goldfeldquandt_df_decreasing.py` | defect | defect | defect |
| `statsmodels_jonckheere_terpstra_fully_tied.py` | n/a | defect | defect |
| `statsmodels_nonequivalence_poisson_2indep.py` | defect | defect | defect |
| `statsmodels_nonequivalence_poisson_2indep_statistic.py` | defect | defect | defect |
| `statsmodels_runstest_2samp_continuity_correction.py` | defect | defect | defect |
| `statsmodels_runstest_2samp_integer_ties.py` | defect | defect | defect |
| `statsmodels_runstest_continuity_correction.py` | defect | defect | defect |
| `statsmodels_score_test_proportions_2indep_constrained_mle.py` | defect | defect | defect |
| `statsmodels_transform_corr_normal_spearman.py` | n/a | defect | defect |
| `statsmodels_tweedie_loglike_underflow.py` | defect | defect | defect |

## networkx

| Script | 3.4.2 | 3.5 | 3.6 | 3.6.1 | 3.7rc0 | 3.7 | development |
|---|---|---|---|---|---|---|---|
| `networkx_edge_current_flow_digraph_exception_docstring.py` | defect | defect | defect | defect | defect | defect | defect |
| `networkx_generate_random_paths_isolated.py` | defect | defect | defect | defect | defect | defect | defect |
| `networkx_group_betweenness_isolate.py` | - | - | - | - | defect | defect | defect |
| `networkx_group_betweenness_regression.py` | - | - | - | - | defect | defect | defect |
| `networkx_group_degree_centrality_duplicates.py` | defect | defect | defect | defect | defect | defect | defect |
| `networkx_node_degree_xy_nodes_docstring.py` | defect | defect | defect | defect | defect | defect | defect |
| `networkx_single_source_all_shortest_paths_zero_weight.py` | defect | defect | defect | defect | defect | defect | defect |

## mne

| Script | 1.11.0 | 1.12.1 | 1.13.2 | development |
|---|---|---|---|---|
| `mne_f_mway_rm_greenhouse_geisser.py` | defect | defect | defect | defect |
| `mne_f_oneway_sigma_docstring.py` | n/a | defect | defect | defect |
| `mne_fdr_correction_boundary.py` | defect | defect | defect | defect |
| `mne_permutation_cluster_1samp_all_not_exact.py` | defect | defect | defect | defect |
| `mne_permutation_cluster_1samp_all_seed_dependent.py` | defect | defect | defect | defect |
| `mne_permutation_cluster_1samp_exact_one_tailed.py` | defect | defect | defect | defect |
